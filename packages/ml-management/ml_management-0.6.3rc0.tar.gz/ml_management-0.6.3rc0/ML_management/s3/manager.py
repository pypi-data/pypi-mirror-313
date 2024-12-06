"""S3 Manager for operations with s3 data."""
import asyncio
import os
import posixpath
import random
import threading
from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import Any, AsyncGenerator, Coroutine, List, Optional, Union

import aioboto3
import boto3
from aiofiles import os as aos
from botocore.awsrequest import AWSRequest, AWSResponse
from botocore.exceptions import ClientError
from tqdm.autonotebook import tqdm

from ML_management import variables
from ML_management.mlmanagement.load_api import _untar_folder
from ML_management.mlmanagement.log_api import _tar_folder
from ML_management.mlmanagement.visibility_options import VisibilityOptions
from ML_management.s3.utils import get_upload_paths
from ML_management.session import AuthSession

MAX_OBJECTS_PER_PAGE = 50
MAX_TASKS_NUMBER = 50
MAX_DELETE_CONCURRENT_REQUESTS = 100


class S3BucketNotFoundError(Exception):
    """Define Bucket Not Found Exception."""

    def __init__(self, bucket: str):
        self.bucket = bucket
        self.message = f'Bucket "{bucket}" does not exist'
        super().__init__(self.message)

    def __reduce__(self):
        """Define reduce method to make exception picklable."""
        return (S3BucketNotFoundError, (self.bucket,))


class S3ObjectNotFoundError(Exception):
    """Define Version Not Found Exception."""

    def __init__(self, path: str, bucket: str):
        self.path = path
        self.bucket = bucket
        self.message = f'Object "{path}" is not found in "{bucket}" bucket'
        super().__init__(self.message)

    def __reduce__(self):
        """Define reduce method to make exception picklable."""
        return (S3ObjectNotFoundError, (self.path, self.bucket))


class FileIsNotTarError(Exception):
    """Define exception when tar is expected but not given."""

    def __init__(self, filename: str):
        self.filename = filename
        self.message = f"Expected tar file, but file {self.filename} does not have '.tar' extension"
        super().__init__(self.message)

    def __reduce__(self):
        """Define reduce method to make exception picklable."""
        return (FileIsNotTarError, (self.filename,))


class AmbiguousFileChoiceError(Exception):
    """Define exception when there is not exactly one file in bucket to choice."""

    def __init__(self, number_of_files: int):
        self.number_of_files = number_of_files
        if not number_of_files:
            appendix = " bucket is empty"
        else:
            appendix = "there is more than one file in bucket. Specify one file name"
        self.message = f"Expected one tar file in bucket, but {appendix}."
        super().__init__(self.message)

    def __reduce__(self):
        """Define reduce method to make exception picklable."""
        return (AmbiguousFileChoiceError, (self.number_of_files,))


class S3Manager:
    """Manager for operations with s3 objects."""

    def __init__(self) -> None:
        """Init creds."""
        self.default_url = variables.get_s3_gateway_url()
        self.default_access_key_id, self.default_secret_access_key = variables.get_s3_credentials()
        self.session = AuthSession()

    def list_buckets(self) -> List[str]:
        """Get list names of available buckets."""
        with self.session.get(posixpath.join(self.default_url, "list-buckets")) as response:
            buckets_info: list[dict[str, str]] = response.json()["buckets"]
            return [bucket["name"] for bucket in buckets_info]

    def create_bucket(self, name: str, visibility: VisibilityOptions) -> None:
        """Create new bucket with specified name and visibility."""
        with self.session.post(
            posixpath.join(self.default_url, "create-bucket"), json={"name": name, "visibility": visibility.value}
        ) as response:
            if response.status_code != HTTPStatus.CREATED:
                raise RuntimeError(f"Failed to create bucket: {response.text}")

    def update_bucket_visibility(self, bucket: str, new_visibility: VisibilityOptions) -> None:
        """Update bucket visibility."""
        if bucket not in self.list_buckets():
            raise S3BucketNotFoundError(bucket)
        with self.session.post(
            posixpath.join(self.default_url, "update-bucket-auth", bucket),
            json={"visibility": new_visibility.value},
        ) as response:
            response.raise_for_status()

    def delete_bucket(self, bucket: str) -> None:
        """Delete bucket, this function is for synchronous code only.

        If you want delete bucket inside async application, use `delete_bucket_async`
        """
        self.delete_by_prefix(bucket=bucket, prefix="")
        s3_client = self._get_sync_boto_client()
        s3_client.delete_bucket(Bucket=bucket)

    async def delete_bucket_async(self, bucket: str) -> None:
        """Delete bucket, for usage in async applications."""
        await self.delete_by_prefix(bucket=bucket, prefix="")
        async with self._get_async_boto_client() as s3_client:
            await s3_client.delete_bucket(Bucket=bucket)

    def delete_by_prefix(self, bucket: str, prefix: str) -> Optional[asyncio.Task]:
        """Delete all objects with specified prefix in key.

        Parameters
        ----------
        bucket_name: str
            name of bucket you want to delete directory from.
        prefix: str
            path to your objects or dir

            Example::

            |    Directories structure:
            |    ├───dockerfile
            |    ├───a.py
            |    ├───dir1
            |            ├───empty.txt
            |            └───dir2
            |                    ├───new.txt
            |                    ├───x.png
            |                    └───ipsum
            |                            └───y.png
            |    To delete dir1    use prefix="dir1"
            |    To delete dir2    use prefix="dir1/dir2"
            |    To delete new.txt use prefix="dir1/dir2/new.txt"
        """
        try:
            if asyncio.get_event_loop().is_running():
                return asyncio.create_task(self._delete_objects(bucket_name=bucket, prefix=prefix))
            asyncio.get_event_loop().close()
        except Exception:
            pass
        asyncio.run(self._delete_objects(bucket_name=bucket, prefix=prefix))

    def upload(
        self,
        local_path: str,
        bucket: str,
        upload_as_tar: bool = False,
        new_bucket_visibility: VisibilityOptions = VisibilityOptions.PRIVATE,
        verbose: bool = True,
    ) -> Optional[asyncio.Task]:
        """
        Upload directory to bucket.

        Parameters
        ----------
        local_path: str
            path to directory with files you want to upload.
        bucket: str
            name of bucket you want to upload to.
        upload_as_tar: bool = False
            If the option is set to True, the files will be uploaded as a single tar archive. Default: False
        verbose: bool = True
            If the option is set to True and upload_as_tar set to False,
            a progress bar with the number of uploaded files will be displayed.

        Returns
        -------
        Optional[asyncio.Task].
            If the files uploading to the bucket is started inside an asynchronous application,
            the method will schedule the task in the running event loop and
            return instance of asyncio.Task for further process monitoring by the application
        """
        if upload_as_tar:
            self._upload_as_tar(local_path=local_path, bucket=bucket, new_bucket_visibility=new_bucket_visibility)
            return

        # in case of asyncio.run() was called previously in code, it closed event loop
        # and get_event_loop() will raise exception:
        # RuntimeError: There is no current event loop in thread <THREAD_NAME>
        try:
            if asyncio.get_event_loop().is_running():
                return asyncio.create_task(
                    self._async_upload_files(
                        local_path=local_path,
                        bucket=bucket,
                        new_bucket_visibility=new_bucket_visibility,
                        verbose=verbose,
                    )
                )
            asyncio.get_event_loop().close()
        except Exception:
            pass
        asyncio.run(
            self._async_upload_files(
                local_path=local_path, bucket=bucket, new_bucket_visibility=new_bucket_visibility, verbose=verbose
            )
        )

    def set_data(
        self,
        *,
        local_path: str = "s3_data",
        bucket: str,
        untar_data: bool = False,
        remote_paths: Optional[List[str]] = None,
        verbose: bool = True,
    ) -> Union[asyncio.Task, str]:
        """
        Set data.

        :type local_path: string
        :param local_path: Local path to save data to.  Defaults to /s3_data/.

        :type bucket: string
        :param bucket: Bucket containing requested files.

        :type remote_paths: list(string)
        :param remote_paths: List of paths relative to passed bucket.  Each path
            can represent either a single file, or a folder.  If a path represents
            a folder (should end with a slash), then all contents of a folder are recursively downloaded.

        :type verbose: bool
        :param verbose: Whether to disable the entire progressbar wrapper.
        """
        if bucket not in self.list_buckets():
            raise S3BucketNotFoundError(bucket)
        if untar_data:
            return self._download_data_tar(
                local_path=local_path,
                bucket=bucket,
                remote_paths=remote_paths,
            )

        try:
            if asyncio.get_event_loop().is_running():
                return asyncio.create_task(
                    self._download_files(
                        local_path=local_path,
                        bucket=bucket,
                        remote_paths=remote_paths,
                        verbose=verbose,
                    )
                )
            asyncio.get_event_loop().close()
        except Exception:
            pass
        return asyncio.run(
            self._download_files(
                local_path=local_path,
                bucket=bucket,
                remote_paths=remote_paths,
                verbose=verbose,
            )
        )

    def _upload_as_tar(self, local_path: str, bucket: str, new_bucket_visibility: VisibilityOptions) -> None:
        local_path = os.path.normpath(local_path)
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Path: {local_path} does not exist")

        r, w = os.pipe()

        try:
            thread = threading.Thread(target=_tar_folder, args=(w, local_path), daemon=True)
            thread.start()
        except Exception as err:
            os.close(r)
            os.close(w)
            raise err

        s3_client = self._get_sync_boto_client()
        buckets = self.list_buckets()
        if bucket not in buckets:
            self.create_bucket(name=bucket, visibility=new_bucket_visibility)
        try:
            with open(r, "rb") as fileobj:
                s3_client.upload_fileobj(Fileobj=fileobj, Bucket=bucket, Key=f"{os.path.basename(local_path)}.tar")
        finally:
            thread.join()

    async def _async_upload_files(
        self, local_path: str, bucket: str, new_bucket_visibility: VisibilityOptions, verbose: bool = True
    ):
        local_path = os.path.normpath(local_path)
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Path: {local_path} does not exist")

        async with self._get_async_boto_client() as s3_client:
            buckets = self.list_buckets()
            if bucket not in buckets:
                self.create_bucket(name=bucket, visibility=new_bucket_visibility)

            upload_paths = get_upload_paths(local_path)
            total_tasks = len(upload_paths)

            with tqdm(
                total=total_tasks,
                disable=not verbose,
                unit="Files",
                unit_scale=True,
                unit_divisor=1024,
            ) as pbar:
                current_task_num = 0
                while current_task_num < total_tasks:
                    tasks: list[asyncio.Task] = []
                    for path in upload_paths[current_task_num : current_task_num + MAX_TASKS_NUMBER]:
                        tasks.append(
                            asyncio.create_task(
                                s3_client.upload_file(Filename=path.local_path, Bucket=bucket, Key=path.storage_path)
                            )
                        )
                    await asyncio.gather(*tasks)
                    pbar.update(len(tasks))
                    current_task_num += MAX_TASKS_NUMBER

    def _download_data_tar(
        self,
        *,
        local_path: str = "s3_data",
        bucket: str,
        remote_paths: Optional[List[str]] = None,
    ) -> str:
        remote_paths = remote_paths if remote_paths else None
        if remote_paths is not None and len(remote_paths) != 1:
            raise RuntimeError(f"Expected one tar object, but {len(remote_paths)} were given.")

        s3_client = self._get_sync_boto_client()
        if remote_paths is not None:
            tar_name = remote_paths[0]
            if not tar_name.endswith(".tar"):
                raise FileIsNotTarError("Expected tar file, but file does not have '.tar' extension")
            return self._download_tar(
                local_path=local_path, s3_client=s3_client, tar_name=remote_paths[0], bucket=bucket
            )

        try:
            # check that there is only one file in bucket
            # If there is more than 1 file, raise exception about ambiguous choice
            paginator = s3_client.get_paginator("list_objects_v2")
            page_iterator = paginator.paginate(Bucket=bucket, Prefix="", PaginationConfig={"MaxItems": 2})
            first_page = next(iter(page_iterator))
            files = first_page.get("Contents", [])
            if len(files) != 1:
                raise AmbiguousFileChoiceError(number_of_files=len(files))
            tar_name: str = files[0]["Key"]
            if not tar_name.endswith(".tar"):
                raise FileIsNotTarError("Expected tar file, but file does not have '.tar' extension")
        except ClientError as err:
            if err.response["Error"]["Code"] == "NoSuchBucket":
                raise S3BucketNotFoundError(bucket=bucket) from None
            else:
                raise

        return self._download_tar(local_path=local_path, s3_client=s3_client, tar_name=tar_name, bucket=bucket)

    def _download_tar(self, local_path: str, tar_name: str, bucket: str, s3_client) -> str:
        r, w = os.pipe()
        with open(r, "rb") as buff:
            try:
                thread = threading.Thread(target=_untar_folder, args=(buff, local_path), daemon=True)
                thread.start()
            except Exception as err:
                os.close(r)
                os.close(w)
                raise err

            try:
                with open(w, "wb") as fileobj:
                    s3_client.download_fileobj(Fileobj=fileobj, Bucket=bucket, Key=tar_name)
            except ClientError as err:
                if err.response["Error"]["Code"] == "404":
                    raise S3ObjectNotFoundError(path=tar_name, bucket=bucket) from None
                raise
            finally:
                thread.join()

            return os.path.join(local_path, tar_name[:-4])

    async def _download_files(
        self,
        *,
        local_path: str = "s3_data",
        bucket: str,
        remote_paths: Optional[List[str]] = None,
        verbose: bool = True,
    ) -> str:
        async def get_objects_number(paginator, remote_path: str = "") -> int:
            total_objects = 0

            page_iterator = paginator.paginate(
                Bucket=bucket,
                Prefix=remote_path,
            )
            async for page in page_iterator:
                if page["KeyCount"] != 0:
                    total_objects += page["KeyCount"]
                    continue
                if remote_path == "":
                    return 0
                raise S3ObjectNotFoundError(path=remote_path, bucket=bucket)

            return total_objects

        remote_paths = remote_paths if remote_paths else [""]
        async with self._get_async_boto_client() as s3_client:
            total_tasks = 0
            try:
                paginator = s3_client.get_paginator("list_objects_v2")
                for remote_path in remote_paths:
                    total_tasks += await get_objects_number(paginator, remote_path)
            except ClientError as err:
                raise RuntimeError("Can not get number of objects in bucket") from err

            with tqdm(
                total=total_tasks,
                unit="Files",
                unit_scale=True,
                unit_divisor=1024,
                disable=not verbose,
            ) as pbar:
                for remote_path in remote_paths:
                    page_iterator = paginator.paginate(
                        Bucket=bucket, Prefix=remote_path, PaginationConfig={"PageSize": MAX_OBJECTS_PER_PAGE}
                    )
                    async for page in page_iterator:
                        tasks: list[Coroutine] = []
                        for obj in page.get("Contents", []):
                            file_path = obj.get("Key")

                            local_dir_path = os.path.join(local_path, posixpath.dirname(file_path))
                            local_file_path = os.path.join(local_path, file_path)
                            tasks.append(
                                self._download_one_object(
                                    bucket=bucket,
                                    key=file_path,
                                    local_dir_path=local_dir_path,
                                    local_file_path=local_file_path,
                                    s3_client=s3_client,
                                )
                            )
                        await asyncio.gather(*tasks)
                        pbar.update(len(tasks))

        return local_path

    async def _delete_objects(self, bucket_name: str, prefix="") -> None:
        if bucket_name not in self.list_buckets():
            raise S3BucketNotFoundError(bucket_name)
        async with self._get_async_boto_client() as s3_client:
            paginator = s3_client.get_paginator("list_objects_v2")
            page_iterator = paginator.paginate(
                Bucket=bucket_name, Prefix=prefix, PaginationConfig={"PageSize": MAX_DELETE_CONCURRENT_REQUESTS}
            )
            async for page in page_iterator:
                tasks: list[Coroutine] = []
                for obj in page.get("Contents", []):
                    object_key = obj.get("Key")
                    tasks.append(self._delete_one_object(bucket=bucket_name, key=object_key, s3_client=s3_client))
                await asyncio.gather(*tasks)

    # arguments to callback are passed like kwargs, so kwargs must be present in signature
    def _add_auth_cookies(self, request: AWSRequest, **kwargs) -> None:  # noqa
        request.headers.add_header("Cookie", self.session._get_cookie_header())

    # arguments to callback are passed like kwargs, so kwargs must be present in signature
    def _update_auth_cookies(self, http_response: AWSResponse, **kwargs) -> None:  # noqa
        cookie_header = http_response.headers.get("set-cookie")
        if cookie_header is None:
            return
        cookies: list[str] = cookie_header.split("; ")
        for cookie in cookies:
            if "kc-access" not in cookie:
                continue
            _, new_access_token = cookie.split("=", maxsplit=1)
            self.session.cookies["kc-access"] = new_access_token
            break

    async def _download_one_object(self, bucket: str, key: str, local_dir_path: str, local_file_path: str, s3_client):
        if not await aos.path.exists(local_dir_path):
            await aos.makedirs(local_dir_path, exist_ok=True)
        await s3_client.download_file(Bucket=bucket, Key=key, Filename=local_file_path)

    async def _delete_one_object(self, bucket: str, key: str, s3_client, retries: int = 3):
        # do retries if there are some network troubles, cause bucket and dir deleting depends on it,
        # if object was deleted earlier, s3_client.delete_object has no effect
        while retries > 0:
            try:
                await s3_client.delete_object(Bucket=bucket, Key=key)
                break
            except Exception:
                retries -= 1
                if retries == 0:
                    raise
                await asyncio.sleep(random.randint(1, 9) * 1e-4)

    def _get_sync_boto_client(self):
        s3_client = boto3.client(
            service_name="s3",
            use_ssl=True,
            endpoint_url=posixpath.join(self.default_url, "s3/"),
            aws_access_key_id=self.default_access_key_id,
            aws_secret_access_key=self.default_secret_access_key,
        )
        event_system = s3_client.meta.events
        event_system.register("before-sign.s3.*", self._add_auth_cookies)
        event_system.register("after-call.s3.*", self._update_auth_cookies)
        return s3_client

    @asynccontextmanager
    async def _get_async_boto_client(self) -> AsyncGenerator[Any, None]:
        session = aioboto3.Session(
            aws_access_key_id=self.default_access_key_id, aws_secret_access_key=self.default_secret_access_key
        )
        async with session.client(
            "s3", use_ssl=True, endpoint_url=posixpath.join(self.default_url, "s3/")
        ) as s3_client:
            event_system = s3_client.meta.events
            event_system.register("before-sign.s3.*", self._add_auth_cookies)
            event_system.register("after-call.s3.*", self._update_auth_cookies)
            yield s3_client
