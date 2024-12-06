"""Functions for internal usage."""
import json
import os
import re
from typing import Dict, List, Optional

from pydantic import BaseModel, validator

from ML_management.variables import FILENAME_FOR_INFERENCE_CONFIG

INIT_FUNCTION_NAME = "get_object"

model_name_pattern = re.compile("(([A-Za-z0-9][A-Za-z0-9_]*)?[A-Za-z0-9])+")

valid_data_types = [
    "bool",
    "uint8",
    "uint16",
    "uint32",
    "uint64",
    "int8",
    "int16",
    "int32",
    "int64",
    "float16",
    "float32",
    "float64",
]


class InferenceParams(BaseModel):
    name: str
    data_type: str
    dims: List[int]

    @validator("data_type")
    @classmethod
    def data_type_check(cls, value):
        assert value in valid_data_types, (
            f"{FILENAME_FOR_INFERENCE_CONFIG}: Every object in 'input' or 'output' list "
            f"should have one of the following data types: {valid_data_types}"
        )


class PredictConfig(BaseModel):
    cfg: Dict[str, List[InferenceParams]]

    @validator("cfg")
    @classmethod
    def cfg_check(cls, value):
        assert (
            "input" in value and "output" in value
        ), f"File {FILENAME_FOR_INFERENCE_CONFIG} should contain both 'input' and 'output' keys"


def is_model_name_valid(name: str):
    return model_name_pattern.fullmatch(name) is not None


def validate_predict_config(path: Optional[str]):
    if path is None or not os.path.isfile(path):
        raise RuntimeError(
            f"File {FILENAME_FOR_INFERENCE_CONFIG} was not found in artifacts. "
            "It is required, when create_venv_pack=True"
        )

    with open(path) as f:
        try:
            data = json.load(f)
        except Exception as err:
            raise RuntimeError(f"File {FILENAME_FOR_INFERENCE_CONFIG} should be valid json.") from err

    PredictConfig(cfg=data)
