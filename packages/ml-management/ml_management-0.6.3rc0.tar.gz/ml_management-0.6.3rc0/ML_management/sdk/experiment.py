from sgqlc.operation import Operation

from ML_management.graphql import schema
from ML_management.graphql.schema import Experiment
from ML_management.graphql.send_graphql_request import send_graphql_request


def set_experiment_description(experiment_id: int, description: str) -> Experiment:
    """
    Set experiment description.

    Parameters
    ----------
    experiment_id: int
        Id of an experiment.
    description: str
        Description of an experiment.

    Returns
    -------
    Experiment
        Instance of a experiment with meta information.
    """
    op = Operation(schema.Mutation)
    set_description = op.set_experiment_description(experiment_id=experiment_id, description=description)
    set_description.name()
    set_description.description()

    experiment = send_graphql_request(op=op)
    return experiment["setExperimentDescription"]


def set_experiment_tag(experiment_id: int, key: str, value: str) -> Experiment:
    """
    Set experiment tag.

    Parameters
    ----------
    experiment_id: int
        Id of an experiment.
    key: str
        Key of a tag.
    value: str
        Value of a tag.

    Returns
    -------
    Experiment
        Instance of an experiment with meta information.
    """
    op = Operation(schema.Mutation)
    set_experiment_tags = op.set_experiment_tag(experiment_id=experiment_id, key=key, value=value)
    set_experiment_tags.name()
    set_experiment_tags.tags()

    experiment = send_graphql_request(op=op)
    return experiment["setExperimentTag"]


def delete_experiment_tag(experiment_id: int, key: str) -> Experiment:
    """
    Delete experiment tag.

    Parameters
    ----------
    experiment_id: int
        Id of an experiment.
    key: str
        Key of a tag to delete.

    Returns
    -------
    Experiment
        Instance of an experiment with meta information.
    """
    op = Operation(schema.Mutation)
    set_experiment_tags = op.delete_experiment_tag(experiment_id=experiment_id, key=key)
    set_experiment_tags.name()
    set_experiment_tags.tags()

    experiment = send_graphql_request(op=op)
    return experiment["deleteExperimentTag"]


def get_experiment_by_name(experiment_name: str) -> Experiment:
    """
    Get experiment by its name.

    Parameters
    ----------
    experiment_name: str
        Name of an experiment.

    Returns
    -------
    Experiment
        Instance of an experiment with meta information.
    """
    op = Operation(schema.Query)
    experiment_from_name = op.experiment_from_name(name=experiment_name)
    experiment_from_name.name()
    experiment_from_name.tags()
    experiment_from_name.description()
    experiment_from_name.experiment_id()

    experiment = send_graphql_request(op=op)
    return experiment["experimentFromName"]


def get_experiment_by_id(experiment_id: int) -> Experiment:
    """
    Get experiment by it's id.

    Parameters
    ----------
    experiment_id: int
        Id of an experiment.

    Returns
    -------
    Experiment
        Instance of an experiment with meta information.
    """
    op = Operation(schema.Query)
    experiment_from_name = op.experiment_from_id(experiment_id=experiment_id)
    experiment_from_name.name()
    experiment_from_name.tags()
    experiment_from_name.description()
    experiment_from_name.experiment_id()

    experiment = send_graphql_request(op=op)
    return experiment["experimentFromId"]
