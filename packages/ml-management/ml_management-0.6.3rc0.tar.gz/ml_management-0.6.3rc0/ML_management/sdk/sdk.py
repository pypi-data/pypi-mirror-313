"""SDK for client library."""
import json
from typing import Dict, List

import pandas as pd
from jsf import JSF


def _to_datetime(df: pd.DataFrame, column_names: List[str]) -> pd.DataFrame:
    """
    Convert df's columns to datetime.

    Parameters
    ----------
    df: pd.DataFrame
        pd.DataFrame in which the columns will be converted.
    column_names: List[str]
        Column names to be converted.

    Returns
    -------
    pd.DataFrame
        Pandas dataframe with converted columns.
    """
    for column_name in column_names:
        df[column_name] = pd.to_datetime(df[column_name], unit="s")

    return df


def _generate_fake_schema(json_schema: dict) -> dict:
    if "required" not in json_schema.keys():
        return {}

    required_properties = {key: json_schema["properties"][key] for key in json_schema["required"]}
    json_schema["properties"] = required_properties

    faker = JSF(json_schema)
    fake_json = faker.generate()
    return fake_json


def _print_params_by_schema(json_schema: Dict, schema_type: str) -> None:
    """Print entity JSON Schema and example with required params."""
    properties_and_required_dict = {key: json_schema[key] for key in ("properties", "required") if key in json_schema}

    json_formatted_str = json.dumps(properties_and_required_dict, indent=2)

    print(f"{schema_type} json-schema:")

    print(json_formatted_str)

    print(f"{schema_type} parameters example:")

    fake_json = _generate_fake_schema(json_schema)

    print(fake_json)
