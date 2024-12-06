"""Common variables."""
import os
import posixpath
from typing import Optional, Tuple

server_url = None
s3_url = None
s3_username = "PLACEHOLDER"
s3_password = "PLACEHOLDER"
mlm_login = None
mlm_password = None

job_run_id = None

CONFIG_KEY_ARTIFACTS = "artifacts"
DEFAULT_EXPERIMENT = "Default"
MLCONFIG = "MLConfig.yaml"
MLMODEL_FILE_NAME = "MLmodel"
DATA = "entity_code_data"
LEGACY_DATA = "data"
FLAVOR_NAME = "python_function"
CONDA_SIZE_LIMIT = 50000
INFERENCE_CONFIG_LIMIT = 50000


EXPERIMENT_NAME_FOR_EXECUTOR = "executors"
EXPERIMENT_NAME_FOR_DATASET_LOADER = "dataset_loaders"
FILENAME_FOR_INFERENCE_CONFIG = "predict_config.json"
SERVER_META = posixpath.join("bff", "meta.json")


def get_server_ml_api() -> str:
    """Get server '/api' endpoint URL."""
    return posixpath.join(get_server_url(), "api")


def get_log_service_url(function_name: str) -> str:
    """Get server '/log-object' endpoint URL for log_model, log_artifact, download_artifacts functions."""
    log_object_url = os.environ.get("log_object_url")
    base_url = log_object_url if log_object_url is not None else get_server_url()
    return posixpath.join(base_url, "log-object", function_name.replace("_", "-"))


def get_server_url() -> str:
    """
    Get server URL.

    If you set the URL using 'mlmanagement.set_server_url' function,
    it takes precedence over the URL from the environment variable 'server_url'
    """
    return os.environ.get("server_url", "https://local.tai-dev.intra.ispras.ru") if not server_url else server_url


def get_s3_gateway_url() -> str:
    """
    Get s3 URL.

    If you set the URL using 'mlmanagement.set_s3_url' function,
    it takes precedence over the URL from the environment variable 'S3_URL'
    """
    return os.environ.get("S3_URL", get_server_url()) if not s3_url else s3_url


def get_s3_credentials() -> Tuple[str, str]:
    """Get s3 credentials."""
    return s3_username, s3_password


def get_mlm_credentials() -> Tuple[Optional[str], Optional[str]]:
    """
    Get mlm credentials.

    If you set the URL using 'mlmanagement.set_mlm_credentials' function,
    it takes precedence over the URL from the environment variables 'MLM_LOGIN' and 'MLM_PASSWORD'.
    Environment variables 'login' and 'password' have last priority.
    """
    login = (
        (os.getenv("login") if not os.getenv("MLM_LOGIN") else os.getenv("MLM_LOGIN")) if not mlm_login else mlm_login
    )
    password = (
        (os.getenv("password") if not os.getenv("MLM_PASSWORD") else os.getenv("MLM_PASSWORD"))
        if not mlm_password
        else mlm_password
    )

    return login, password


def get_server_websocket_url() -> str:
    """Get the current websocket server URL."""
    url = get_server_url()
    splitted_url = url.split("/")
    splitted_url[0] = "wss:" if "https" in url else "ws:"
    return "/".join(splitted_url)
