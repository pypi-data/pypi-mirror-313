import importlib
import os
import os.path
import subprocess
import sys
import tarfile
import tempfile
import threading
import traceback
from pathlib import Path
from typing import Optional

import yaml

from ML_management.base_exceptions import MLMClientError
from ML_management.mlmanagement.log_api import _raise_error
from ML_management.mlmanagement.model_type import ModelType
from ML_management.session import AuthSession
from ML_management.variables import (
    CONFIG_KEY_ARTIFACTS,
    DATA,
    FLAVOR_NAME,
    LEGACY_DATA,
    MLCONFIG,
    MLMODEL_FILE_NAME,
    get_log_service_url,
)


def download_artifacts_by_name_version(
    name: str, version: Optional[int], model_type: ModelType, path: str, dst_path: Optional[str] = None
) -> str:
    """Download an artifact by name and version to a local directory, and return a local path for it."""
    url = get_log_service_url("download_artifacts_by_name_version")
    params = {
        "path": os.path.normpath(path) if path else path,
        "name": name,
        "version": version,
        "model_type": model_type.value,
    }
    return _request_download_artifacts(url, params, dst_path)


def download_job_artifacts(job_id: str, path: str = "", dst_path: Optional[str] = None) -> str:
    """Download an artifact file or directory from a job to a local directory, and return a local path for it."""
    url = get_log_service_url("download_job_artifacts")
    params = {"path": os.path.normpath(path) if path else path, "job_name": job_id}
    return _request_download_artifacts(url, params, dst_path)


def _load_model_type(
    name: str,
    version: Optional[int],
    model_type: ModelType,
    install_requirements: bool = False,
    dst_path: Optional[str] = None,
    kwargs_for_init=None,
):
    """Load model from local path."""
    local_path = download_artifacts_by_name_version(
        name=name, version=version, model_type=model_type, path="", dst_path=dst_path
    )
    if install_requirements:
        _set_model_version_requirements(local_path)
    loaded_model = _load_model_src(local_path, kwargs_for_init)
    return loaded_model


def load_dataset(
    name: str,
    version: Optional[int] = None,
    install_requirements: bool = False,
    dst_path: Optional[str] = None,
    kwargs_for_init: Optional[dict] = None,
):
    """Download all model's files for loading model locally.

    Parameters
    ==========
    name: str
        Name of the dataset.
    version: Optional[int] = None
        Version of the dataset. Default: None, "latest" version is used.
    install_requirements: bool = False
        Whether to install dataset requirements. Default: False.
    dst_path: Optional[str]: None
        Destination path. Default: None.
    kwargs_for_init: Optional[dict]: None
        Kwargs for __init__ function of dataset loader when it would be loaded.
    Returns
    =======
    DatasetLoaderPattern
        The object of the dataset to use.
    """
    return _load_model_type(name, version, ModelType.DATASET_LOADER, install_requirements, dst_path, kwargs_for_init)


def _set_model_version_requirements(local_path) -> None:
    """Installing requirements of the model locally."""
    with open(os.path.join(local_path, "requirements.txt")) as req:
        requirements = list(
            filter(
                lambda x: "ml-management" not in x.lower() and "mlflow" not in x.lower() and len(x),
                req.read().split("\n"),
            )
        )
    try:
        if requirements:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--no-cache-dir", "--default-timeout=100", *requirements]
            )

    except Exception:
        print(traceback.format_exc())


def load_model(
    name: str,
    version: Optional[int] = None,
    install_requirements: bool = False,
    dst_path: Optional[str] = None,
    kwargs_for_init=None,
):
    """Download all model's files for loading model locally.

    Parameters
    ==========
    name: str
        Name of the model.
    version: Optional[int] = None
        Version of the model. Default: None, "latest" version is used.
    install_requirements: bool = False
        Whether to install model requirements. Default: False.
    dst_path: Optional[str]: None
        Destination path. Default: None.
    kwargs_for_init: Optional[dict]: None
        Kwargs for __init__ function of model when it would be loaded.
    Returns
    =======
    Model
        The object of the model to use.
    """
    return _load_model_type(name, version, ModelType.MODEL, install_requirements, dst_path, kwargs_for_init)


def load_executor(
    name: str,
    version: Optional[int] = None,
    install_requirements: bool = False,
    dst_path: Optional[str] = None,
):
    """Download all model's files for loading model locally.

    Parameters
    ==========
    name: str
        Name of the executor.
    version: Optional[int] = None
        Version of the executor. Default: None, "latest" version is used.
    install_requirements: bool = False
        Whether to install executor requirements. Default: False.
    dst_path: Optional[str]: None
        Destination path. Default: None.
    Returns
    =======
    BaseExecutor
        The object of the executor to use.
    """
    return _load_model_type(name, version, ModelType.EXECUTOR, install_requirements, dst_path)


def _untar_folder(buff, to_folder):
    try:
        with tarfile.open(mode="r|", fileobj=buff) as tar:
            tar.extractall(to_folder)
    except Exception as err:
        raise MLMClientError("Some error during untar the content.") from err


def _request_download_artifacts(url, params: dict, dst_path: Optional[str] = None):
    path = params["path"]
    with AuthSession().get(url=url, params=params, stream=True) as response:
        _raise_error(response)
        untar = response.headers.get("untar") == "True"
        if dst_path is None:
            dst_path = tempfile.mkdtemp()
        dst_path = os.path.abspath(os.path.normpath(dst_path))
        local_path = os.path.normpath(os.path.join(dst_path, os.path.normpath(path)))
        if untar:
            r, w = os.pipe()
            with open(r, "rb") as buff:
                try:
                    thread = threading.Thread(target=_untar_folder, args=(buff, local_path))
                    thread.start()
                except Exception as err:
                    os.close(r)
                    os.close(w)
                    raise err

                with open(w, "wb") as wfd:
                    for chunk in response.iter_raw():
                        wfd.write(chunk)
                thread.join()
                return local_path
        else:
            dirs = os.path.dirname(local_path)
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            with open(local_path, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
            return local_path


def _load_model_src(local_path: str, kwargs_for_init: Optional[dict]):
    if not kwargs_for_init:
        kwargs_for_init = {}
    config_path = os.path.join(local_path, MLCONFIG)
    if os.path.exists(config_path):
        with open(config_path) as file:
            conf = yaml.safe_load(file)

        load_model_path = os.path.join(local_path, conf["load_model_path"])

    elif os.path.exists(os.path.join(local_path, MLMODEL_FILE_NAME)):
        with open(os.path.join(local_path, MLMODEL_FILE_NAME)) as file:
            conf = yaml.safe_load(file)

        # legacy data entity code path for backward compatibility
        code_data_path = (
            conf["flavors"][FLAVOR_NAME][DATA]
            if DATA in conf["flavors"][FLAVOR_NAME]
            else conf["flavors"][FLAVOR_NAME][LEGACY_DATA]
        )
        load_model_path = os.path.join(local_path, code_data_path)

    else:
        raise RuntimeError("MLConfig does not exist.")

    from ML_management.mlmanagement.utils import INIT_FUNCTION_NAME  # circular import

    parts = Path(load_model_path).parts
    if str(Path(*parts[:2])) not in sys.path:
        sys.path.append(str(Path(*parts[:2])))
    python_model = getattr(importlib.import_module(".".join(parts[2:])), INIT_FUNCTION_NAME)(**kwargs_for_init)
    artifacts = Path(load_model_path) / CONFIG_KEY_ARTIFACTS
    if not artifacts.exists():
        artifacts.mkdir()

    python_model.artifacts = str(artifacts)

    return python_model
