"""S3 Collector for downloading files and folders."""
import asyncio
from typing import List, Optional, Union

from ML_management.collectors.collector_pattern import CollectorPattern
from ML_management.s3 import S3Manager


class S3Collector(CollectorPattern):
    """Collector for S3 paths using ML_management.s3.manager.S3Manager."""

    @staticmethod
    def get_json_schema():
        """Return json schema."""
        return {
            "type": "object",
            "properties": {
                "bucket": {"type": "string"},
                "untar_data": {"type": "boolean", "default": False},
                "remote_paths": {"type": ["array", None], "items": {"type": "string"}, "default": None},
            },
            "required": ["bucket"],
            "additionalProperties": False,
        }

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
        :param local_path: Local path to save data to.  Defaults to "s3_data".

        :type bucket: string
        :param bucket: Bucket containing requested files.

        :type remote_paths: list(string)
        :param remote_paths: List of paths relative to passed bucket.  Each path
            can represent either a single file, or a folder.  If a path represents
            a folder (should end with a slash), then all contents of a folder are recursively downloaded.

        :type verbose: bool
        :param verbose: Whether to disable the entire progressbar wrapper.
        """
        return S3Manager().set_data(
            local_path=local_path, bucket=bucket, untar_data=untar_data, remote_paths=remote_paths, verbose=verbose
        )
