import os
from typing import Optional, Union

import mlflow

from databricks.rag_eval import context
from databricks.rag_eval.mlflow import mlflow_utils
from databricks.rag_eval.monitoring import entities


def _get_managed_evals_client():
    return context.get_context().build_managed_evals_client()


def _parse_monitoring_config(
    monitoring_config: Union[dict, entities.MonitoringConfig],
) -> entities.MonitoringConfig:
    assert monitoring_config is not None, "monitoring_config is required"
    monitoring_config = entities.MonitoringConfig.from_dict(monitoring_config)

    # Validate sampling.
    assert isinstance(
        monitoring_config.sample, (int, float)
    ), "monitoring_config.sample must be a number"
    assert (
        0 <= monitoring_config.sample <= 1
    ), "monitoring_config.sample must be between 0 and 1"

    # Validate periodic monitoring.
    assert (
        monitoring_config.periodic is not None
    ), "monitoring_config.periodic is required"
    assert isinstance(
        monitoring_config.periodic.interval, int
    ), "monitoring_config.periodic.interval must be an integer"
    assert monitoring_config.periodic.unit in [
        "HOURS",
        "DAYS",
        "WEEKS",
    ], "monitoring_config.periodic.unit must be one of 'HOURS', 'DAYS', 'WEEKS'"

    # Validate paused.
    assert monitoring_config.paused is None or isinstance(
        monitoring_config.paused, bool
    ), "monitoring_config.paused must be a boolean"

    # Validate metrics.
    assert monitoring_config.metrics is None or (
        isinstance(monitoring_config.metrics, list)
    ), "monitoring_config.metrics must be a list of strings"
    return monitoring_config


@context.eval_context
def create_monitor(
    endpoint_name: str,
    *,
    monitoring_config: Union[dict, entities.MonitoringConfig],
    experiment_id: Optional[str] = None,
) -> entities.Monitor:
    """
    Create a monitor for a serving endpoint.

    Args:
        endpoint_name: The name of the serving endpoint.
        monitoring_config: The monitoring configuration.
        experiment_id: The experiment ID to log the monitoring results. Defaults to the experiment
            used to log the model that is serving the provided `endpoint_name`.
    Returns:
        The monitor for the serving endpoint.
    """
    monitoring_config = _parse_monitoring_config(monitoring_config)

    if experiment_id is None:
        # Infer the experiment ID and the workspace path from the current environment.
        experiment = mlflow_utils.infer_experiment_from_endpoint(endpoint_name)
    else:
        experiment = mlflow.get_experiment(experiment_id)

    workspace_path = os.path.dirname(experiment.name)
    return _get_managed_evals_client().create_monitor(
        endpoint_name=endpoint_name,
        monitoring_config=monitoring_config,
        experiment_id=experiment.experiment_id,
        workspace_path=workspace_path,
    )


@context.eval_context
def update_monitor(
    endpoint_name: str,
    *,
    monitoring_config: Union[dict, entities.MonitoringConfig],
) -> entities.Monitor:
    """
    Partially update a monitor for a serving endpoint.

    Top-level fields specified in 'monitoring_config' are completely replaced. Partially updating
    nested fields is not supported.

    Allowed:
        update_monitor(endpoint_name, monitoring_config={"sample": 0.5})

    Not allowed:
        update_monitor(endpoint_name, monitoring_config={"periodic": {"interval": 3}})

    Args:
        endpoint_name: The name of the serving endpoint.
        monitoring_config: The configuration change, using upsert semantics.
    Returns:
        The updated monitor for the serving endpoint.
    """
    assert monitoring_config is not None, "monitoring_config is required"
    monitoring_config = entities.MonitoringConfig.from_dict(monitoring_config)
    # Do not allow partial updates for nested fields.
    if monitoring_config.periodic:
        assert (
            monitoring_config.periodic.interval is not None
            and monitoring_config.periodic.unit is not None
        ), "Partial update for periodic monitoring is not supported."

    return _get_managed_evals_client().update_monitor(
        endpoint_name=endpoint_name,
        monitoring_config=monitoring_config,
    )


@context.eval_context
def delete_monitor(endpoint_name: str) -> None:
    """
    Deletes a monitor for a serving endpoint.

    Args:
        endpoint_name: The name of the serving endpoint.
    """
    return _get_managed_evals_client().delete_monitor(endpoint_name=endpoint_name)
