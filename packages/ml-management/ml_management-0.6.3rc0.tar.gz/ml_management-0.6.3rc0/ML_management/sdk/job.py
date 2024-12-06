import json
import posixpath
import sys
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import quote

import numpy as np
import pandas as pd
import websocket
from matplotlib import pyplot as plt
from sgqlc.operation import Operation

from ML_management.collectors.collector_pattern_to_methods_map import collector_method_schema_name
from ML_management.graphql import schema
from ML_management.graphql.schema import ExecutionJob, Param
from ML_management.graphql.send_graphql_request import send_graphql_request
from ML_management.sdk.model import get_latest_model_version
from ML_management.sdk.parameters import AnyDatasetLoaderForm, AnyModelForm, DatasetLoaderForm, ModelForm
from ML_management.session import AuthSession
from ML_management.variables import get_server_url, get_server_websocket_url


def job_by_name(name: str) -> ExecutionJob:
    """
    Return Job object by name.

    Parameters
    ----------
    name: str
        Name of the job.

    Returns
    -------
    Job
        Instance of the Job class.
    """
    op = Operation(schema.Query)

    base_query = op.job_from_name(name=name)
    base_query.name()
    base_query.periodic_type()
    base_query.status()
    base_query.registration_timestamp()
    base_query.start_timestamp()
    base_query.end_timestamp()
    base_query.build_job()
    base_query.exception()

    job = send_graphql_request(op, json_response=False)

    return job.job_from_name


def job_metric_by_name(name: str) -> pd.DataFrame:
    """
    Job's most recent logged metrics.

    Parameters
    ----------
    name: str
        Name of the job.

    Returns
    -------
    pd.DataFrame
        Pandas dataframe with latest metrics.
    """
    op = Operation(schema.Query)

    op.job_from_name(name=name).latest_metrics()
    json_data = send_graphql_request(op)

    json_data = json_data["jobFromName"]["latestMetrics"]

    return pd.DataFrame([json_data])


def available_metrics(job_name: str) -> List[str]:
    """
    List logged types of logged metrics in given job.

    Parameters
    ----------
    job_name: str
        Name of the job.

    Returns
    -------
    List[str]
        List with names of metrics.
    """
    op = Operation(schema.Query)
    base = op.job_from_name(name=job_name)
    base.available_metrics()
    job = send_graphql_request(op, False)

    return job.job_from_name.available_metrics


def list_params_job(job_name: str) -> List[Param]:
    """
    List logged params in given job.

    Parameters
    ----------
    job_name: str
        Name of the job.

    Returns
    -------
    List[Param]
        List of params.
    """
    op = Operation(schema.Query)
    base = op.job_from_name(name=job_name)
    base.list_params()
    job = send_graphql_request(op, False)

    return job.job_from_name.list_params


def metric_history(
    job_name: str, metric_name: str, x_axis: str = "step", make_graph: bool = True, **kwargs
) -> Tuple[List[float], List[float]]:
    """
    Lists history of given metric in given job and plots graph of metric's change over time.

    Parameters
    ----------
    job_name: str
        Name of the job.
    metric_name: str
        Name of the metric.
    x_axis: str
        Witch value use as x axis for graph or as return value. Possible options: "time", "step"
    make_graph: bool
        If to build graph of metric over time.
    kwargs: Any
        Any additional key arguments for plt.plot.

    Returns
    -------
    Tuple(List[float], List[float])
        First list with provided x axis of logged metric.
        Second list with values of metrics.
        Also plots graph using provided x axis and metric's values as y axis.
    """
    op = Operation(schema.Query)
    base = op.job_from_name(name=job_name)
    base.metric_history(metric=metric_name)
    job = send_graphql_request(op, False)
    metrics = job.job_from_name.metric_history
    metric_values = [metric.value for metric in metrics]
    x_values = []
    if x_axis != "step" and x_axis != "time":
        raise ValueError("x_axis value must be step or time")
    if x_axis == "step":
        x_values = [metric.step for metric in metrics]
        if np.nonzero(x_values)[0].size == 0:
            metrics = sorted(metrics, key=lambda x: x.timestamp)
            x_values = [step[0] for step in enumerate(metrics)]
        else:
            metrics = sorted(metrics, key=lambda x: x.step)
    elif x_axis == "time":
        metrics = sorted(metrics, key=lambda x: x.timestamp)
        start_timestamp = metrics[0].timestamp
        x_values = [(metric.timestamp - start_timestamp) / 1000 for metric in metrics]

    if make_graph:
        plt.grid()
        plt.xlabel("seconds" if x_axis == "time" else "step")
        plt.ylabel(metric_name)
        plt.plot(x_values, metric_values, marker=".", **kwargs)

    return x_values, metric_values


def get_logs(job_name: str, stream: bool = True, file_name: Optional[str] = None) -> None:
    """
    Stream logs of the execution job by job name.

    Parameters
    ----------
    job_name: str
        Name of the execution job whose logs we want to view.
    stream: bool = True
        Stream logs or dump all available at the moment.
    file_name: Optional[str] = None
        Name of the file where to save logs. Default: None. If None prints logs to the output.
    """
    _get_logs(job_type=JobType.execution, stream=stream, file_name=file_name, params={"job_id": job_name})


def cancel_job(job_name: str) -> bool:
    """
    Cancel running or planned execution job.

    Parameters
    ----------
    job_name: str
        Name of the job to cancel.
    """
    op = Operation(schema.Mutation)
    op.cancel_job(job_name=job_name)
    return send_graphql_request(op)["cancelJob"]


class JobType(str, Enum):
    """Enum job type."""

    build = "build"
    execution = "execution"
    venv = "venv"


def get_build_logs(
    model_name: str, model_version: Optional[int] = None, stream: bool = True, file_name: Optional[str] = None
) -> None:
    """
    Stream logs of the build job by model name and version.

    Parameters
    ----------
    model_name: str
        The name of the model whose docker image creation logs you want to view.
    model_version: Optional[int] = None
        The version of the model whose docker image creation logs you want to view.
        Default: None, "latest" version is used.
    stream: bool = True
        Stream logs or dump all available at the moment.
    file_name: Optional[str] = None
        Name of the file where to save logs. Default: None. If None prints logs to the output.
    """
    if model_version is None:
        model_version = get_latest_model_version(model_name).version

    _get_logs(
        job_type=JobType.build,
        stream=stream,
        file_name=file_name,
        params={"model_name": model_name, "model_version": model_version},
    )


def get_venv_build_logs(
    model_name: str, model_version: Optional[int] = None, stream: bool = True, file_name: Optional[str] = None
) -> None:
    """
    Stream logs of the venv archive creating job by model name and version.

    Parameters
    ----------
    model_name: str
        The name of the model whose venv archive creation logs you want to view.
    model_version: Optional[int] = None
        The version of the model whose venv archive creation logs you want to view.
        Default: None, "latest" version is used.
    stream: bool = True
        Stream logs or dump all available at the moment.
    file_name: Optional[str] = None
        Name of the file where to save logs. Default: None. If None prints logs to the output.
    """
    if model_version is None:
        model_version = get_latest_model_version(model_name).version

    _get_logs(
        job_type=JobType.venv,
        stream=stream,
        file_name=file_name,
        params={"model_name": model_name, "model_version": model_version},
    )


def _get_logs(job_type: JobType, params: Dict[str, Any], stream: bool = True, file_name: Optional[str] = None) -> None:
    url = _get_logs_url(params=params, stream=stream, job_type=job_type)
    if stream:
        ws = None
        file = sys.stdout
        try:
            ws = AuthSession().instantiate_websocket_connection(url)
            if file_name:
                file = open(file_name, "w")
            while True:
                data = ws.recv()
                if not data:
                    return
                data = json.loads(data)
                if "status" not in data or data["status"] != "OK":
                    raise RuntimeError("Internal Server Error")
                print("\n".join(data["logs"]), file=file)
        except KeyboardInterrupt:
            pass
        except websocket._exceptions.WebSocketBadStatusException:
            possible_reasons_msg = (
                "Model with that name and version does not exist or does not have build job"
                if job_type is not JobType.execution
                else "Job with that name does not exist"
            )
            print(
                "<Connection refused. Check your query parameters, they may be incorrect.>\n"
                "<Possible reasons:>\n"
                f"<{possible_reasons_msg}>"
            )
        except Exception as err:
            print(err)
        finally:
            if ws is not None:
                ws.close()
            if file_name:
                file.close()
        return

    with AuthSession().get(url, stream=True) as resp:
        if file_name:
            with open(file_name, "a") as f:
                for line in resp.iter_lines():
                    if line:
                        f.writelines([line, "\n"])
        else:
            for line in resp.iter_lines():
                if line:
                    print(line)


def _get_logs_url(params: Dict[str, Any], job_type: JobType, stream: bool = True) -> str:
    server_url = get_server_websocket_url() if stream else get_server_url()
    url_base = posixpath.join(server_url, "logs-api")
    url_encoded_params = "&".join(f"{quote(str(key))}={quote(str(value))}" for key, value in params.items())
    local_path = f"{f'stream/{job_type.value}' if stream else f'filedump/{job_type.value}'}?{url_encoded_params}"
    return posixpath.join(url_base, local_path)


def add_ml_job(
    job_executor_name: str,
    executor_params: dict,
    models_pattern: Union[ModelForm, AnyModelForm],
    data_pattern: Union[DatasetLoaderForm, AnyDatasetLoaderForm],
    gpu: bool = False,
    job_executor_version: Optional[int] = None,
    experiment_name: str = "Default",
    cron_expression: Optional[str] = None,
    periodic_type: str = "ONCE",
    job_name: Optional[str] = None,
    additional_system_packages: Optional[List[str]] = None,
) -> str:
    """
    Create execution job.

    Parameters
    ----------
    job_executor_name: str
        Name of the executor that will execute the job.
    executor_params: Dict[str, ...]
        Dictionary of executor parameters.
        Example::

            {
                'executor_param1': 'value1',
                'executor_param2': 'value2',
                'executor_param3': 'value3',
                ...
            }

    models_pattern: Union[ModelForm, AnyModelForm]
        Necessary information for using the models.
    data_pattern: Union[DatasetLoaderForm, AnyDatasetLoaderForm]
        Necessary information for using the datasets.
    gpu: bool = False
        Whether to use GPU for this job or not. Default: False
    job_executor_version: Optional[int] = None
        Version of the executor that will execute the job. Default: None, "latest" version is used.
    experiment_name: str = "Default"
        Name of the experiment. Default: "Default"
    cron_expression: str = None
        Cron expression for periodic or deferred jobs. Default: None
    periodic_type: {"ONCE", "PERIODIC"}
        Frequency of the task. Default: "ONCE"
    additional_system_packages: Optional[List[str]] = None
        List of system libraries for Debian family distributions that need to be installed in the job. Default: None

    Returns
    -------
    str
        Name of the Job.
    """
    if not isinstance(models_pattern, ModelForm) and not isinstance(models_pattern, AnyModelForm):
        raise TypeError("Parameter models must have type ModelForm or AnyModelForm.")
    if not isinstance(data_pattern, DatasetLoaderForm) and not isinstance(data_pattern, AnyDatasetLoaderForm):
        raise TypeError("Parameter data_pattern must have type DatasetLoaderForm or AnyDatasetLoaderForm.")
    models = models_pattern.serialize()
    data_params = data_pattern.serialize()
    list_role_data_params = []
    for data_param_role in data_params:
        op = Operation(schema.Query)
        data_inner_params: dict = data_param_role["data_params"]
        dataset_loader_name = data_inner_params["dataset_loader_name"]
        dataset_loader_version = data_inner_params.get("dataset_loader_version", None)
        dataset_loader_version_choice = schema.ObjectVersionOptionalInput(
            name=dataset_loader_name, version=dataset_loader_version
        )

        collector_name = data_inner_params["collector_name"]

        collector_method_params = schema.MethodParamsInput(
            method_name=collector_method_schema_name, method_params=json.dumps(data_inner_params["collector_params"])
        )

        list_dataset_loader_method_params = []
        for item in data_inner_params["dataset_loader_params"]:
            for key in item:
                list_dataset_loader_method_params.append(
                    schema.MethodParamsInput(method_name=key, method_params=json.dumps(item[key]))
                )

        current_dataset_loader_params = schema.DataParamsInput(
            dataset_loader_version_choice=dataset_loader_version_choice,
            collector_name=collector_name,
            list_dataset_loader_method_params=list_dataset_loader_method_params,
            collector_method_params=collector_method_params,
        )

        list_role_data_params.append(
            schema.RoleDataParamsInput(role=data_param_role["role"], data_params=current_dataset_loader_params)
        )

    op = Operation(schema.Query)
    _executor_version = schema.ObjectVersionOptionalInput(name=job_executor_name, version=job_executor_version)

    executor_version_choice = schema.ObjectVersionOptionalInput(name=job_executor_name, version=job_executor_version)

    executor_model_schema = op.executor_version_from_name_version(executor_version=_executor_version)
    executor_model_schema.executor_method_schema_name()

    executor_version_obj = send_graphql_request(op, json_response=False)
    executor_method_schema = executor_version_obj.executor_version_from_name_version.executor_method_schema_name

    executor_method_params = schema.MethodParamsInput(
        method_name=executor_method_schema, method_params=json.dumps(executor_params)
    )

    list_role_model_params = []

    for model in models:
        choice_criteria = model["model"].get("choice_criteria", "latest")
        version = model["model"].get("version")

        model_version_choice = schema.ModelVersionChoice(
            name=model["model"]["name"],
            version=version,
            choice_criteria=choice_criteria,
        )

        model_methods_params = []

        for item in model["params"]:
            for key in item:
                model_methods_params.append(
                    schema.MethodParamsInput(method_name=key, method_params=json.dumps(item[key]))
                )

        new_model_name = model.get("new_model_name")
        new_model_description = model.get("description")
        prepare_new_model_inference = model.get("prepare_new_model_inference", False)

        current_model_params = schema.ModelParamsInput(
            model_version_choice=model_version_choice,
            list_model_method_params=model_methods_params,
            new_model_name=new_model_name,
            prepare_new_model_inference=prepare_new_model_inference,
            description=new_model_description,
        )

        model_role = schema.RoleModelParamsInput(role=model["role"], model_params=current_model_params)

        list_role_model_params.append(model_role)

    executor_params = schema.ExecutorParamsInput(
        executor_method_params=executor_method_params,
        executor_version_choice=executor_version_choice,
    )

    op = Operation(schema.Mutation)
    mutation = op.add_ml_job(
        form=schema.JobParameters(
            executor_params=executor_params,
            list_role_model_params=list_role_model_params,
            list_role_data_params=list_role_data_params,
            experiment_name=experiment_name,
            cron_expression=cron_expression,
            periodic_type=periodic_type,
            gpu=gpu,
            additional_system_packages=additional_system_packages,
            job_name=job_name,
        )
    )

    mutation.name()

    job = send_graphql_request(op, json_response=False)

    return job.add_ml_job.name
