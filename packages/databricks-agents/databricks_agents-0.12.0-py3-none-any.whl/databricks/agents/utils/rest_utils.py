import posixpath
from typing import Any, Dict, Optional

from mlflow.deployments.constants import MLFLOW_DEPLOYMENT_CLIENT_REQUEST_RETRY_CODES
from mlflow.environment_variables import MLFLOW_HTTP_REQUEST_TIMEOUT
from mlflow.utils.databricks_utils import get_databricks_host_creds
from mlflow.utils.rest_utils import augmented_raise_for_status, http_request


def call_endpoint(
    *,
    method: str,
    prefix: str = "/api/2.0/agents",
    route: Optional[str] = "",
    json_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[int] = None,
):
    call_kwargs = {}
    if method.lower() == "get":
        call_kwargs["params"] = json_body
    else:
        call_kwargs["json"] = json_body

    response = http_request(
        # TODO: come back to this in order to add support for profiles in the future
        host_creds=get_databricks_host_creds("databricks"),
        endpoint=posixpath.join(prefix, route),
        method=method,
        timeout=MLFLOW_HTTP_REQUEST_TIMEOUT.get() if timeout is None else timeout,
        raise_on_status=False,
        retry_codes=MLFLOW_DEPLOYMENT_CLIENT_REQUEST_RETRY_CODES,
        **call_kwargs,
    )
    augmented_raise_for_status(response)
    #  TODO: replace this with response protos
    return response.json()


def construct_endpoint_url(workspace_url, endpoint_name):
    return (
        f"{workspace_url}/ml/endpoints/{endpoint_name}"
        if (endpoint_name is not None and workspace_url is not None)
        else None
    )
