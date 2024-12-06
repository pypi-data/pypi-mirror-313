import logging
import uuid
from typing import Dict, List, Optional

# Agents SDK
from mlflow import set_registry_uri

from databricks.agents.client.rest_client import (
    delete_chain as rest_delete_chain,
)
from databricks.agents.client.rest_client import (
    deploy_chain as rest_deploy_chain,
)
from databricks.agents.client.rest_client import (
    list_chain_deployments as rest_list_chain_deployments,
)
from databricks.agents.feedback import _FEEDBACK_MODEL_NAME, log_feedback_model
from databricks.agents.sdk_utils.deployments import _get_deployments
from databricks.agents.sdk_utils.entities import Deployment
from databricks.agents.utils.mlflow_utils import (
    _check_model_is_rag_compatible,
    _get_latest_model_version,
    get_workspace_url,
)
from databricks.agents.utils.uc import (
    _check_model_name,
    _get_catalog_and_schema,
    _sanitize_model_name,
)
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors.platform import (
    BadRequest,
    InvalidParameterValue,
    PermissionDenied,
    ResourceConflict,
    ResourceDoesNotExist,
)
from databricks.sdk.service.serving import (
    AutoCaptureConfigInput,
    EndpointCoreConfigInput,
    EndpointCoreConfigOutput,
    EndpointPendingConfig,
    EndpointTag,
    Route,
    ServedEntityInput,
    ServedEntityOutput,
    ServedModelInputWorkloadSize,
    TrafficConfig,
)

_logger = logging.getLogger("agents")

__DEPLOY_ENV_VARS_WITH_STATIC_VALUES = {
    "ENABLE_LANGCHAIN_STREAMING": "true",
    "ENABLE_MLFLOW_TRACING": "true",
    "RETURN_REQUEST_ID_IN_RESPONSE": "true",
}
_MODEL_SERVING_HOST_URL_ENV_VAR = "DB_MODEL_SERVING_HOST_URL"


__DEPLOY_ENV_VARS_WITH_DYNAMIC_VALUES = {
    # Returned value from get_workspace_info_from_dbutils is a tuple of (host_url, token)
    # The environment variable should only contain the host_url, format https://<host_or_fqdn>
    "DB_MODEL_SERVING_HOST_URL": lambda: get_workspace_url(),
}

_MAX_ENDPOINT_NAME_LEN = 63
_MAX_SERVED_ENTITY_NAME_LEN = 63


def _validate_environment_vars(environment_vars: Dict[str, str]) -> None:
    # If environment_vars is not a dictionary, raise an error
    if not isinstance(environment_vars, dict):
        raise ValueError("Argument 'environment_vars' must be a dictionary.")

    errors = []
    for key, value in environment_vars.items():
        # Environment variable names must be uppercase and can only contain letters, numbers, or underscores
        if not isinstance(key, str) or not key.isupper() or not key.isidentifier():
            errors.append(
                f"Environment variable ({key}) is not a valid identifier. Allowed characters are uppercase letters, numbers or underscores. An environment variable cannot start with a number."
            )

        # Environment variable values must be strings
        if not isinstance(value, str):
            errors.append(
                f"Invalid environment variable. Both key ({key}) and value ({value}) must be strings."
            )

        # Environment variable values cannot override default values for Agents
        if (
            key in __DEPLOY_ENV_VARS_WITH_STATIC_VALUES
            and value != __DEPLOY_ENV_VARS_WITH_STATIC_VALUES[key]
        ):
            errors.append(
                f"Environment variable ({key}) cannot be set to value ({value})."
            )

    if len(errors) > 0:
        raise ValueError("\n".join(errors))


def get_deployments(
    model_name: str, model_version: Optional[int] = None
) -> List[Deployment]:
    """
    Get chain deployments metadata.

    Args:
        model_name: Name of the UC registered model
        model_version: (Optional) Version numbers for specific agents.

    Returns:
        All deployments for the UC registered model.
    """
    return _get_deployments(model_name, model_version)


def _create_served_model_input(
    model_name,
    version,
    model_input_name,
    scale_to_zero,
    environment_vars,
    instance_profile_arn=None,
    workload_size=ServedModelInputWorkloadSize.SMALL,
):
    return ServedEntityInput(
        name=_sanitize_model_name(model_input_name),
        entity_name=model_name,
        entity_version=version,
        workload_size=workload_size.value,
        scale_to_zero_enabled=scale_to_zero,
        environment_vars=environment_vars,
        instance_profile_arn=instance_profile_arn,
    )


def _create_endpoint_name(model_name):
    prefix = "agents_"
    truncated_model_name = model_name[: _MAX_ENDPOINT_NAME_LEN - len(prefix)]
    sanitized_truncated_model_name = _sanitize_model_name(truncated_model_name)
    return f"agents_{sanitized_truncated_model_name}"


def _create_served_model_name(model_name, version):
    model_version_suffix = f"_{version}"
    truncated_model_name = model_name[
        : _MAX_SERVED_ENTITY_NAME_LEN - len(model_version_suffix)
    ]
    sanitized_truncated_model_name = _sanitize_model_name(truncated_model_name)
    return f"{sanitized_truncated_model_name}{model_version_suffix}"


def _create_feedback_model_name(model_name: str) -> str:
    catalog_name, schema_name = _get_catalog_and_schema(model_name)
    return f"{catalog_name}.{schema_name}.{_FEEDBACK_MODEL_NAME}"


def _set_up_feedback_model_permissions(feedback_uc_model_name: str) -> None:
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.getOrCreate()
    spark.sql(f"GRANT EXECUTE ON FUNCTION {feedback_uc_model_name} TO `account users`;")


def _create_feedback_model(
    feedback_uc_model_name: str, scale_to_zero: bool
) -> ServedEntityInput:
    set_registry_uri("databricks-uc")

    # only create the feedback model if it doesn't already exist in this catalog.schema
    feedback_model_version = str(_get_latest_model_version(feedback_uc_model_name))
    if feedback_model_version == "0":
        # also adds to UC with version '1'
        log_feedback_model(feedback_uc_model_name)
        feedback_model_version = str(_get_latest_model_version(feedback_uc_model_name))
        _set_up_feedback_model_permissions(feedback_uc_model_name)
    return _create_served_model_input(
        feedback_uc_model_name,
        feedback_model_version,
        _FEEDBACK_MODEL_NAME,
        scale_to_zero,
        environment_vars=None,
    )


def _create_feedback_model_config(
    uc_model_name: str,
    pending_config: EndpointPendingConfig,
    scale_to_zero: bool = False,
) -> EndpointCoreConfigOutput:
    """
    Parse pending_config to get additional information about the feedback model in order to
    return a config as if the endpoint was successfully deployed with only the feedback model.
    This way we can reuse the update functions that are written for normal endpoint updates.
    """
    feedback_models = []
    feedback_routes = []
    feedback_uc_model_name = _create_feedback_model_name(uc_model_name)

    # Try to find a feedback in pending configs
    found_feedback_model = False
    for model in pending_config.served_entities:
        if model.name == _FEEDBACK_MODEL_NAME:
            found_feedback_model = True
            feedback_models = [
                _create_served_model_input(
                    model_name=feedback_uc_model_name,
                    version=model.entity_version,
                    model_input_name=_FEEDBACK_MODEL_NAME,
                    scale_to_zero=model.scale_to_zero_enabled,
                    environment_vars=None,
                )
            ]
            feedback_routes = [
                Route(served_model_name=_FEEDBACK_MODEL_NAME, traffic_percentage=0)
            ]
            break

    # If pending configs does not have a feedback model, create a new one
    if not found_feedback_model:
        feedback_models = [
            _create_feedback_model(feedback_uc_model_name, scale_to_zero),
        ]
        feedback_routes = [
            Route(
                served_model_name=_FEEDBACK_MODEL_NAME,
                traffic_percentage=0,
            ),
        ]

    return EndpointCoreConfigOutput(
        served_entities=feedback_models,
        traffic_config=TrafficConfig(routes=feedback_routes),
        auto_capture_config=pending_config.auto_capture_config,
    )


def _construct_table_name(catalog_name, schema_name, model_name):
    w = WorkspaceClient()
    # remove catalog and schema from model_name and add agents- prefix
    base_name = model_name.split(".")[2]
    suffix = ""

    # try to append suffix
    for index in range(20):
        if index != 0:
            suffix = f"_{index}"

        table_name = f"{base_name[:63 - len(suffix)]}{suffix}"

        full_name = f"{catalog_name}.{schema_name}.{table_name}_payload"
        if not w.tables.exists(full_name=full_name).table_exists:
            return table_name

    # last attempt - append uuid and truncate to 63 characters (max length for table_name_prefix)
    # unlikely to have conflict unless base_name is long
    if len(base_name) > 59:
        return f"{base_name[:59]}_{uuid.uuid4().hex}"[:63]
    return f"{base_name}_{uuid.uuid4().hex}"[:63]


def _create_new_endpoint_config(
    model_name,
    version,
    endpoint_name,
    scale_to_zero=False,
    environment_vars=None,
    instance_profile_arn=None,
    workload_size=None,
):
    catalog_name, schema_name = _get_catalog_and_schema(model_name)

    served_model_name = _create_served_model_name(model_name, version)
    feedback_uc_model_name = _create_feedback_model_name(model_name)

    table_name = _construct_table_name(catalog_name, schema_name, model_name)

    return EndpointCoreConfigInput(
        name=endpoint_name,
        served_entities=[
            _create_served_model_input(
                model_name,
                version,
                served_model_name,
                scale_to_zero,
                environment_vars,
                instance_profile_arn,
                workload_size,
            ),
            _create_feedback_model(feedback_uc_model_name, scale_to_zero),
        ],
        traffic_config=TrafficConfig(
            routes=[
                Route(
                    served_model_name=served_model_name,
                    traffic_percentage=100,
                ),
                Route(
                    served_model_name=_FEEDBACK_MODEL_NAME,
                    traffic_percentage=0,
                ),
            ]
        ),
        auto_capture_config=AutoCaptureConfigInput(
            catalog_name=catalog_name,
            schema_name=schema_name,
            table_name_prefix=table_name,
        ),
    )


def _update_traffic_config(
    model_name: str,
    version: str,
    existing_config: EndpointCoreConfigOutput,
) -> TrafficConfig:
    served_model_name = _create_served_model_name(model_name, version)
    updated_routes = [
        Route(served_model_name=served_model_name, traffic_percentage=100)
    ]

    found_feedback_model = False
    if existing_config:
        for traffic_config in existing_config.traffic_config.routes:
            if traffic_config.served_model_name == _FEEDBACK_MODEL_NAME:
                found_feedback_model = True
            updated_routes.append(
                Route(
                    served_model_name=traffic_config.served_model_name,
                    traffic_percentage=0,
                )
            )
    if not found_feedback_model:
        updated_routes.append(
            Route(
                served_model_name=_FEEDBACK_MODEL_NAME,
                traffic_percentage=0,
            )
        )
    return TrafficConfig(routes=updated_routes)


def _update_served_models(
    model_name: str,
    version: str,
    endpoint_name: str,
    existing_config: EndpointCoreConfigOutput,
    scale_to_zero: bool,
    environment_vars: Dict[str, str],
    instance_profile_arn: str,
) -> List[ServedEntityInput]:
    served_model_name = _create_served_model_name(model_name, version)
    updated_served_models = [
        _create_served_model_input(
            model_name,
            version,
            served_model_name,
            scale_to_zero,
            environment_vars,
            instance_profile_arn,
        )
    ]

    found_feedback_model = False
    if existing_config:
        for served_model in existing_config.served_entities:
            if served_model.name == _FEEDBACK_MODEL_NAME:
                found_feedback_model = True
        updated_served_models.extend(existing_config.served_entities)
    if not found_feedback_model:
        updated_served_models.append(
            _create_feedback_model(
                _create_feedback_model_name(model_name), scale_to_zero
            )
        )

    return updated_served_models


def _update_traffic_config_for_delete(
    updated_served_models: List[ServedEntityOutput],
) -> TrafficConfig:
    updated_routes = []

    # Find the highest version
    max_version_served_model = max(
        updated_served_models, key=lambda sm: sm.entity_version
    )
    max_version = max_version_served_model.entity_version

    # All routes have traffic_percentage=0 except the new highest version
    for served_model in updated_served_models:
        traffic_percentage = 0
        if served_model.entity_version == max_version:
            traffic_percentage = 100
        updated_routes.append(
            Route(
                served_model_name=served_model.name,
                traffic_percentage=traffic_percentage,
            )
        )

    # Append route for feedback model
    updated_routes.append(
        Route(
            served_model_name=_FEEDBACK_MODEL_NAME,
            traffic_percentage=0,
        ),
    )

    return TrafficConfig(routes=updated_routes)


def _construct_query_endpoint(workspace_url, endpoint_name, model_name, version):
    # This is a temporary solution until we can identify the appropriate solution to get
    # the workspace URI in backend. Ref: https://databricks.atlassian.net/browse/ML-39391
    served_model_name = _create_served_model_name(model_name, version)
    return f"{workspace_url}/serving-endpoints/{endpoint_name}/served-models/{served_model_name}/invocations"


def deploy(
    model_name: str,
    model_version: int,
    scale_to_zero: bool = False,
    environment_vars: Dict[str, str] = None,
    instance_profile_arn: str = None,
    tags: Dict[str, str] = None,
    workload_size: ServedModelInputWorkloadSize = ServedModelInputWorkloadSize.SMALL,
    **kwargs,
) -> Deployment:
    """
    Deploy new version of the agents.

    Args:
        model_name: Name of the UC registered model.
        model_version: Model version number.
        scale_to_zero: Flag to scale the endpoint to zero when not in use. With scale to zero, \
            the compute resources may take time to come up so the app may not be ready instantly. Defaults to False.
        environment_vars: Dictionary of environment variables used to provide configuration for the endpoint. Defaults to {}.
        instance_profile_arn: Instance profile ARN to use for the endpoint. Defaults to None.
        tags: Dictionary of tags to attach to the deployment. Defaults to None.

    Returns:
        Chain deployment metadata.
    """
    _check_model_is_rag_compatible(model_name, model_version)
    _check_model_name(model_name)
    endpoint_name = kwargs.get("endpoint_name", _create_endpoint_name(model_name))
    scale_to_zero = kwargs.get("scale_to_zero", scale_to_zero)
    user_env_vars = kwargs.get(
        "environment_vars", environment_vars if environment_vars is not None else {}
    )
    _validate_environment_vars(user_env_vars)
    instance_profile_arn = kwargs.get("instance_profile_arn", instance_profile_arn)
    tags = kwargs.get("tags", tags)
    workload_size = kwargs.get("workload_size", workload_size)

    environment_vars = {}
    dynamic_vars = {
        key: var_extractor()
        for key, var_extractor in __DEPLOY_ENV_VARS_WITH_DYNAMIC_VALUES.items()
        if key not in user_env_vars
    }
    environment_vars.update(dynamic_vars)
    environment_vars.update(user_env_vars)
    environment_vars.update(__DEPLOY_ENV_VARS_WITH_STATIC_VALUES)

    w = WorkspaceClient()
    try:
        endpoint = w.serving_endpoints.get(endpoint_name)
    except ResourceDoesNotExist:
        w.serving_endpoints.create(
            name=endpoint_name,
            config=_create_new_endpoint_config(
                model_name,
                model_version,
                endpoint_name,
                scale_to_zero,
                environment_vars,
                instance_profile_arn,
                workload_size,
            ),
            tags=[EndpointTag(key, val) for key, val in tags.items()] if tags else None,
        )
    else:
        config = endpoint.config
        # TODO: https://databricks.atlassian.net/browse/ML-39649
        # config=None means this endpoint has never successfully deployed before
        # bc we have a dummy feedback model, we know feedback works, so we only want its config
        if config is None:
            config = _create_feedback_model_config(
                model_name, endpoint.pending_config, scale_to_zero
            )

        # ignore pending_config bc we only redeploy models that have succesfully deployed before
        # set the traffic config for all currently deployed models to be 0
        updated_traffic_config = _update_traffic_config(
            model_name, model_version, config
        )
        updated_served_models = _update_served_models(
            model_name,
            model_version,
            endpoint_name,
            config,
            scale_to_zero,
            environment_vars,
            instance_profile_arn,
        )
        try:
            w.serving_endpoints.update_config(
                name=endpoint_name,
                served_entities=updated_served_models,
                traffic_config=updated_traffic_config,
                auto_capture_config=config.auto_capture_config,
            )
        except ResourceConflict:
            raise ValueError(f"Endpoint {endpoint_name} is currently updating.")
        except InvalidParameterValue as e:
            if "served_models cannot contain more than 15 elements" in str(e):
                raise ValueError(
                    f"Endpoint {endpoint_name} already has 15 deployed models. Delete one before redeploying."
                )
            else:
                # pass through any other errors
                raise e
        except BadRequest as e:
            if "Cannot create 2+ served entities" in str(e):
                raise ValueError(
                    f"Endpoint {endpoint_name} already serves model {model_name}, version {model_version}."
                )
            else:
                raise e

    workspace_url = get_workspace_url()
    deployment_info = rest_deploy_chain(
        model_name=model_name,
        model_version=model_version,
        query_endpoint=_construct_query_endpoint(
            workspace_url, endpoint_name, model_name, model_version
        ),
        endpoint_name=endpoint_name,
        served_entity_name=_create_served_model_name(model_name, model_version),
        workspace_url=workspace_url,
    )
    user_message = f"""
    Deployment of {deployment_info.model_name} version {model_version} initiated.  This can take up to 15 minutes and the Review App & Query Endpoint will not work until this deployment finishes.

    View status: {deployment_info.endpoint_url}
    Review App: {deployment_info.review_app_url}
    """

    ## TODO (ML-42186) - Change this to Logger
    print(user_message)

    return deployment_info


def list_deployments() -> List[Deployment]:
    """
    Returns:
      A list of all Agent deployments.
    """
    return rest_list_chain_deployments()


def _delete_endpoint(
    workspace_client: WorkspaceClient, endpoint_name: str, model_name: str
) -> None:
    try:
        workspace_client.serving_endpoints.delete(endpoint_name)
    except PermissionDenied:
        raise PermissionDenied(
            f"User does not have permission to delete deployments for model {model_name}."
        )


def delete_deployment(model_name: str, model_version: Optional[int] = None) -> None:
    """
    Delete an agent deployment.

    Args:
        model_name: Name of UC registered model
        version: Model version number. This is optional and when specified, we delete \
            the served model for the particular version.
    """
    _check_model_name(model_name)
    deployments = get_deployments(model_name=model_name, model_version=model_version)
    if len(deployments) == 0:
        raise ValueError(f"Deployments for model {model_name} do not exist.")
    endpoint_name = deployments[0].endpoint_name

    w = WorkspaceClient()
    endpoint = None
    try:
        endpoint = w.serving_endpoints.get(endpoint_name)
    except ResourceDoesNotExist:
        _logger.warning(f"Deployments for model {model_name} do not exist.")
    except PermissionDenied:
        raise PermissionDenied(
            f"User does not have permission to delete deployments for model {model_name}."
        )

    if endpoint:
        if model_version is None:
            _delete_endpoint(w, endpoint_name, model_name)
        else:
            # If model_version is specified, then remove only the served model, leave other served entities
            config = endpoint.config
            # Config=None means the deployment never successfully deployed before. In this
            # case, we raise an error that specified model version is in a failed state or
            # does not exist.
            if config is None:
                raise ValueError(
                    f"The deployment for model version {model_version} is in a failed state or does not exist."
                )

            # Check against expected versions in the database to be resilient to endpoint
            # update failures.
            versions = set(
                [
                    deployment.model_version
                    for deployment in _get_deployments(model_name)
                ]
            )
            updated_served_models = [
                served_model
                for served_model in config.served_entities
                if not (
                    # Filter out the specified model version.
                    served_model.entity_name == model_name
                    and served_model.entity_version == str(model_version)
                )
                and (
                    # Filter out any versions that do not exist in the database.
                    served_model.name == _FEEDBACK_MODEL_NAME
                    or served_model.entity_version in versions
                )
            ]

            if len(config.served_entities) == len(updated_served_models):
                raise ValueError(
                    f"The deployment for model version {model_version} does not exist."
                )
            updated_served_models_without_feedback = [
                served_model
                for served_model in updated_served_models
                if not (served_model.name == _FEEDBACK_MODEL_NAME)
            ]

            if len(updated_served_models_without_feedback) == 0:
                # If there are no more served models remaining, delete the endpoint.
                _delete_endpoint(w, endpoint_name, model_name)
            else:
                updated_traffic_config = _update_traffic_config_for_delete(
                    updated_served_models_without_feedback
                )
                try:
                    w.serving_endpoints.update_config(
                        name=endpoint_name,
                        served_entities=updated_served_models,
                        traffic_config=updated_traffic_config,
                        auto_capture_config=config.auto_capture_config,
                    )
                except PermissionDenied:
                    raise PermissionDenied(
                        f"User does not have permission to delete deployments for model {model_name}. "
                        f"Deployment for model version {model_version} was not deleted."
                    )
                except Exception as e:
                    raise Exception(
                        f"Failed to delete deployment for model {model_name} version {model_version}. {e}"
                    )

    # ToDo[ML-42212]: Move this rest call above deleting endpoints after permissions are implemented in the backend
    rest_delete_chain(model_name, model_version)
