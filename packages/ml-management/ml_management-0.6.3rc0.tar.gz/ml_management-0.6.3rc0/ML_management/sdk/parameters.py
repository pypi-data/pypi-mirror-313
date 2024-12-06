"""Module with pydantics model representing parameters of sdk functions."""

from typing import List, Literal, Optional

from pydantic import BaseModel, PositiveInt

from ML_management.dataset_loader.dataset_loader_pattern_to_methods_map import DatasetLoaderMethodName
from ML_management.executor import BaseExecutor
from ML_management.model.model_type_to_methods_map import ModelMethodName


class ModelMethodParams(BaseModel):
    """Class for parameters for one model method.

    Attributes
    ----------
    method: ModelMethodName
        method of model.
    params: dict
        parameters for method.
        Example::

            {key1: value1, key2: value2}

    """

    method: ModelMethodName
    params: dict

    def serialize(self) -> dict:
        return {self.method.value: self.params}


class DatasetLoaderMethodParams(BaseModel):
    """Class for parameters for one dataset loader method.

    Attributes
    ----------
    method: DatasetLoaderMethodName
        method of dataset loader.
    params: dict
        parameters for method.
        Example::

            {key1: value1, key2: value2}

    """

    method: DatasetLoaderMethodName = DatasetLoaderMethodName.get_dataset
    params: dict

    def serialize(self) -> dict:
        return {self.method.value: self.params}


class ModelVersionChoice(BaseModel):
    """Class for model version choice in add_ml_job.

    Attributes
    ----------
    name: str
        Name of the model to interact with.
    version: Optional[int] = None
        Version of the model to interact with.
        Default: None, "latest" version is used.
    choice_criteria: {"latest", "initial"}
        Criteria to choose the model to interact with. Required if model_version is not specified. Default: "latest"
        If "best": according to the optimal_min value, minimum (or maximum) value for the selected metric_name is taken.
    """

    name: str
    version: Optional[PositiveInt] = None
    choice_criteria: Literal["latest", "initial"] = "latest"

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "choice_criteria": self.choice_criteria,
        }


class ModelForm(BaseModel):
    """Class for single model parameters for add_ml_job function.

    Attributes
    ----------
    model_version_choice: ModelVersionChoice
        parameters that determine which model to use.
    params: List[ModelMethodParams] = []
        List of ModelMethodParams with parameters of model methods.
        Example::

            [
                ModelMethodParams(method=ModelMethodName.evaluate_function, params={key1: value1, key2: value2}),
                ModelMethodParams(method=ModelMethodName.finetune_function, params={key1: value1, key2: value2})
            ]

        Default: [].
    new_model_name: Optional[str] = None
        Name of the model to save in case new model is to be created as a result of job execution.
        (regulated by executor.upload_model_mode).
        Default: None.
    new_model_description: Optional[str] = None
        Description of the new model name.
        Default: None.
    prepare_new_model_inference: bool = False
        Start preparing the environment for the inference of the new model.
        Default: False.
    """

    model_version_choice: ModelVersionChoice
    params: List[ModelMethodParams] = []
    new_model_name: Optional[str] = None
    new_model_description: Optional[str] = None
    prepare_new_model_inference: bool = False

    def serialize(self) -> List[dict]:
        return [
            {
                "role": BaseExecutor.DEFAULT_ROLE,
                "model": self.model_version_choice.serialize(),
                "params": [method_params.serialize() for method_params in self.params],
                "new_model_name": self.new_model_name,
                "prepare_new_model_inference": self.prepare_new_model_inference,
                "description": self.new_model_description,
            }
        ]


class ModelWithRole(ModelForm):
    """Class for one role model with parameters for add_ml_job function.

    Same as ModelForm except parameter role: str is required.

    Attributes
    ----------
    model_version_choice: ModelVersionChoice
        parameters that determine which model to use.
    params: List[ModelMethodParams] = []
        List of ModelMethodParams with parameters of model methods.
        Example::

            [
                ModelMethodParams(method=ModelMethodName.evaluate_function, params={key1: value1, key2: value2}),
                ModelMethodParams(method=ModelMethodName.finetune_function, params={key1: value1, key2: value2})
            ]

        Default: [].
    new_model_name: Optional[str] = None
        Name of the model to save in case new model is to be created as a result of job execution.
        (regulated by executor.upload_model_mode).
        Default: None.
    new_model_description: Optional[str] = None
        Description of the new model name.
        Default: None.
    prepare_new_model_inference: bool = False
        Start preparing the environment for the inference of the new model.
        Default: False.
    role: str
        Role of the model.
    """

    role: str

    def serialize(self) -> List[dict]:
        result = super().serialize()
        result[0]["role"] = self.role
        return result


class AnyModelForm(BaseModel):
    """Class for definition of arbitrary number of models used in job with their roles.

    Attributes
    ----------
    models: List[ModelWithRole]

        Example (Both instances of ModelWithRole and usual list of dicts may be used)::

            [
                ModelWithRole(
                    role="role_one",
                    model_version_choice=ModelVersionChoice(
                        name="model_1_name",
                        version=1,  # Optional. Default: latest version
                    )
                    params=[
                        ModelMethodParams(
                            method=ModelMethodName.evaluate_function,
                            params={key1: value1, key2: value2}
                        ),
                        ModelMethodParams(
                            method=ModelMethodName.finetune_function,
                            params={key1: value1, key2: value2}
                        )
                    ]
                    new_model_name="some_name"  # Optional. Default: None
                    new_model_description="some_description" # Optional. Default: None
                ),
                ModelWithRole(
                    role="role_two",
                    model_version_choice=ModelVersionChoice(name="model_2_name"),
                    params=[
                        ModelMethodParams(
                            method=ModelMethodName.evaluate_function,
                            params={key1: value1, key2: value2}
                        ),
                        ModelMethodParams(
                            method=ModelMethodName.finetune_function,
                            params={key1: value1, key2: value2}
                        )
                    ]
                )
            ]

    """

    models: List[ModelWithRole]

    def serialize(self) -> List[dict]:
        if len(self.models) == 0:
            return self.models

        result = self.models[0].serialize()
        for model in self.models[1:]:
            result.extend(model.serialize())
        return result


class DatasetLoaderForm(BaseModel):
    """Class for single dataset loader parameters for add_ml_job function.

    Attributes
    ----------
    name: str
        Name of the DatasetLoader that the model will use.
    version: Optional[int] = None
        Version of the DatasetLoader that the model will interact with.
        Default: None, "latest" version is used.
    params: List[DatasetLoaderMethodParams] = []
        List of DatasetLoaderMethodParams with parameters of model methods.
        Example::

            [
                DatasetLoaderMethodParams(
                    # by default params are set for DatasetLoaderMethodName.get_dataset method
                    params={key1: value1, key2: value2}
                ),
                DatasetLoaderMethodParams(
                    method=DatasetLoaderMethodName.<some_method>,
                    params={key1: value1, key2: value2}
                )
            ]

        Default: [].
    collector_name: {"s3", }
        Name of the collector to interact with. Default: "s3"
    collector_params: dict
        Dictionary of collector parameters.
        Example::

            {"bucket": "mnist"}

    """

    name: str
    params: List[DatasetLoaderMethodParams] = []
    collector_params: dict
    version: Optional[PositiveInt] = None
    collector_name: str = "s3"

    def serialize(self) -> List[dict]:
        return [
            {
                "role": BaseExecutor.DEFAULT_ROLE,
                "data_params": {
                    "collector_name": self.collector_name,
                    "collector_params": self.collector_params,
                    "dataset_loader_name": self.name,
                    "dataset_loader_version": self.version,
                    "dataset_loader_params": [method_params.serialize() for method_params in self.params],
                },
            }
        ]


class DatasetLoaderWithRole(DatasetLoaderForm):
    """Class for one role dataset loader with parameters for add_ml_job function.

    Same as DatasetLoaderForm except parameter role: str is required.

    Attributes
    ----------
    name: str
        Name of the DatasetLoader that the model will use.
    version: Optional[int] = None
        Version of the DatasetLoader that the model will interact with.
        Default: None, "latest" version is used.
    params: List[DatasetLoaderMethodParams] = []
        List of DatasetLoaderMethodParams with parameters of model methods.
        Example::

            [
                DatasetLoaderMethodParams(
                    # by default params are set for DatasetLoaderMethodName.get_dataset method
                    params={key1: value1, key2: value2}
                ),
                DatasetLoaderMethodParams(
                    method=DatasetLoaderMethodName.<some_method>,
                    params={key1: value1, key2: value2}
                )
            ]

        Default: [].
    collector_name: {"s3", }
        Name of the collector to interact with.
        Default: "s3"
    collector_params: dict
        Dictionary of collector parameters.
        Example::

            {"bucket": "mnist"}

    role: str
        Role of the DatasetLoader.
    """

    role: str

    def serialize(self) -> List[dict]:
        result = super().serialize()
        result[0]["role"] = self.role
        return result


class AnyDatasetLoaderForm(BaseModel):
    """Class for definition of arbitrary number of dataset_loaders used in job with their roles.

    Attributes
    ----------
    datasetloaders: List[DatasetLoaderWithRole]

        Example (Both instances of DatasetLoaderWithRole and usual list of dicts may be used)::

            [
                DatasetLoaderWithRole(
                    role="data1",
                    name="multiple_two_datasets",
                    version=1,  # Optional. Default: latest version
                    params=[
                        DatasetLoaderMethodParams(
                            # by default params are set for DatasetLoaderMethodName.get_dataset method
                            params={key1: value1, key2: value2}
                        ),
                        DatasetLoaderMethodParams(
                            method=DatasetLoaderMethodName.get_dataset,  # or other method
                            params={key1: value1, key2: value2}
                        )
                    ],
                    collector_name="s3",
                    collector_params={"bucket": "mnist"}
                ),
                DatasetLoaderWithRole(
                    role="data2",
                    name="multiple_two_datasets",
                    collector_name="s3",
                    collector_params={"bucket": "mnist"}
                )
            ]

    """

    dataset_loaders: List[DatasetLoaderWithRole]

    def serialize(self) -> List[dict]:
        if len(self.dataset_loaders) == 0:
            return []

        result = self.dataset_loaders[0].serialize()
        for model in self.dataset_loaders[1:]:
            result.extend(model.serialize())
        return result
