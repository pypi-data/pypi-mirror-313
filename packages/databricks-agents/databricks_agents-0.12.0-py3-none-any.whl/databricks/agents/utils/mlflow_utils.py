import logging
from urllib.parse import urlparse

import mlflow
from mlflow import MlflowClient
from mlflow.types.llm import CHAT_MODEL_INPUT_SCHEMA, CHAT_MODEL_OUTPUT_SCHEMA
from mlflow.utils import databricks_utils

from databricks.sdk import WorkspaceClient

CHAT_COMPLETIONS_REQUEST_KEYS = ["messages"]
CHAT_COMPLETIONS_RESPONSE_KEYS = ["choices"]
SPLIT_CHAT_MESSAGES_KEYS = ["query", "history"]
STRING_RESPONSE_KEYS = ["content"]
RESERVED_INPUT_KEYS = ["databricks_options", "stream"]
RESERVED_OUTPUT_KEYS = ["databricks_output", "id"]
CUSTOM_INPUTS_KEY = "custom_inputs"
CUSTOM_OUTPUTS_KEY = "custom_outputs"

_logger = logging.getLogger(__name__)


# TODO: use `get_register_model` when `latest_versions` is fixed for UC models
def _get_latest_model_version(model_name: str) -> int:
    """
    Get the latest model version for a given model name.
    :param model_name: The name of the model.
    :return: The latest model version.
    """
    mlflow.set_registry_uri("databricks-uc")
    mlflow_client = MlflowClient()
    latest_version = 0
    for mv in mlflow_client.search_model_versions(f"name='{model_name}'"):
        version_int = int(mv.version)
        if version_int > latest_version:
            latest_version = version_int
    return latest_version


def _is_subset_of_attrs(subset, superset):
    return all(item in superset.items() for item in subset.items())


def _detect_extra_fields_and_warn(agent_schema, expected_field_names, warning_msg_fn):
    agent_fields = [field.name for field in agent_schema.inputs]
    extra_keys = set(agent_fields) - set(expected_field_names)
    if extra_keys:
        _logger.warning(warning_msg_fn(extra_keys))


def _detect_extra_inputs(agent_input_schema, expected_field_names):
    return _detect_extra_fields_and_warn(
        agent_input_schema,
        expected_field_names,
        lambda extra_keys: f"The input schema contains extra keys not recognized by agent framework: {list(extra_keys)}. "
        f"These keys will not be supported in Databricks product features like AI Playground. "
        f"Use custom_inputs to pass custom inputs to your agent in a manner compatible with "
        f"downstream product features. "
        "See https://docs.databricks.com/en/generative-ai/agent-framework/agent-schema.html#custom-agent-schemas "
        "for more details.",
    )


def _detect_extra_outputs(agent_output_schema, expected_field_names):
    return _detect_extra_fields_and_warn(
        agent_output_schema,
        expected_field_names,
        lambda extra_keys: f"The output schema contains extra keys not recognized by agent framework: {list(extra_keys)}. "
        f"These keys will not be supported in Databricks product features like AI Playground. "
        f"Use custom_outputs to return custom outputs from your agent in a manner compatible with "
        f"downstream product features. See "
        "https://docs.databricks.com/en/generative-ai/agent-framework/agent-schema.html#custom-agent-schemas "
        "for more details.",
    )


def _load_model_schema(model_name: str, version: int):
    mlflow.set_registry_uri("databricks-uc")
    model_uri = f"models:/{model_name}/{str(version)}"
    model_info = mlflow.models.get_model_info(model_uri)
    signature = model_info.signature
    return signature.inputs, signature.outputs


def _check_model_is_rag_compatible(model_name: str, version: int):
    input_schema, output_schema = _load_model_schema(model_name, version)
    return _check_model_is_rag_compatible_helper(input_schema, output_schema)


def _check_model_is_rag_compatible_new_signatures(input_schema, output_schema):
    input_properties = input_schema.to_dict()[0]
    output_properties = output_schema.to_dict()[0]
    return (
        input_properties == CHAT_MODEL_INPUT_SCHEMA.to_dict()[0]
        and output_properties == CHAT_MODEL_OUTPUT_SCHEMA.to_dict()[0]
    )


def _check_model_is_rag_compatible_legacy_signatures(input_schema, output_schema):
    try:
        from mlflow.models.rag_signatures import (
            ChatCompletionRequest,
            ChatCompletionResponse,
            SplitChatMessagesRequest,
            StringResponse,
        )
        from mlflow.types.schema import convert_dataclass_to_schema
    except ImportError:
        # Fail closed if the agent signatures are not available
        return False
    _logger.warning(
        "Agent model version did not have any of the recommended agent signatures. "
        "Falling back to checking agent model version compatibility with legacy signatures. "
        "Databricks recommends updating and re-logging agents to use the latest signatures; legacy "
        "signatures will be removed in new versions of the MLflow client."
    )
    chat_completions_request_schema = convert_dataclass_to_schema(
        ChatCompletionRequest()
    )
    chat_completions_request_properties = chat_completions_request_schema.to_dict()[0]
    split_chat_messages_schema = convert_dataclass_to_schema(SplitChatMessagesRequest())
    split_chat_messages_properties = split_chat_messages_schema.to_dict()[0]
    input_properties = input_schema.to_dict()[0]
    if _is_subset_of_attrs(chat_completions_request_properties, input_properties):
        # confirm that reserved keys and split chat messages keys are not present in the input
        if any(
            key in input_properties
            for key in RESERVED_INPUT_KEYS + SPLIT_CHAT_MESSAGES_KEYS
        ):
            raise ValueError(
                "The model's schema is not compatible with Agent Framework. The input schema must not "
                "contain a reserved key. "
                f"Input schema: {input_schema}"
            )
        _detect_extra_inputs(
            agent_input_schema=input_schema,
            expected_field_names=[
                field.name for field in chat_completions_request_schema.inputs
            ]
            + [CUSTOM_INPUTS_KEY],
        )

    elif _is_subset_of_attrs(split_chat_messages_properties, input_properties):
        # confirm that reserved keys and chat completions request keys are not present in the input
        if any(
            key in input_properties
            for key in RESERVED_INPUT_KEYS + CHAT_COMPLETIONS_REQUEST_KEYS
        ):
            raise ValueError(
                "The model's schema is not compatible with Agent Framework. The input schema must not "
                "contain a reserved key. "
                f"Input schema: {input_schema}"
            )
        _detect_extra_inputs(
            agent_input_schema=input_schema,
            expected_field_names=[
                field.name for field in split_chat_messages_schema.inputs
            ]
            + [CUSTOM_INPUTS_KEY],
        )
    elif input_properties == CHAT_MODEL_INPUT_SCHEMA.to_dict()[0]:
        pass
    else:
        # input schema does not match any of the expected schemas
        raise ValueError(
            "The model's schema is not compatible with Agent Framework. The input schema must be "
            "either ChatCompletionRequest or SplitChatMessagesRequest. "
            f"Input schema: {input_schema}"
        )

    chat_completions_response_schema = convert_dataclass_to_schema(
        ChatCompletionResponse()
    )
    chat_completions_response_properties = chat_completions_response_schema.to_dict()[0]
    string_response_schema = convert_dataclass_to_schema(StringResponse())
    string_response_properties = string_response_schema.to_dict()[0]

    output_properties = output_schema.to_dict()[0]

    if _is_subset_of_attrs(chat_completions_response_properties, output_properties):
        # confirm that reserved keys and string response keys are not present in the output
        if any(
            key in output_properties
            for key in RESERVED_OUTPUT_KEYS + STRING_RESPONSE_KEYS
        ):
            raise ValueError(
                "The model's schema is not compatible with Agent Framework. The output schema must not "
                "contain a reserved key. "
                f"Output schema: {output_schema}"
            )
        _detect_extra_outputs(
            agent_output_schema=output_schema,
            expected_field_names=[
                field.name for field in chat_completions_response_schema.inputs
            ]
            + [CUSTOM_OUTPUTS_KEY],
        )

    elif _is_subset_of_attrs(string_response_properties, output_properties):
        # confirm that reserved keys and chat completions response keys are not present in the output
        if any(
            key in output_properties
            for key in RESERVED_OUTPUT_KEYS + CHAT_COMPLETIONS_RESPONSE_KEYS
        ):
            raise ValueError(
                "The model's schema is not compatible with Agent Framework. The output schema must not "
                "contain a reserved key. "
                f"Output schema: {output_schema}"
            )
        _detect_extra_outputs(
            agent_output_schema=output_schema,
            expected_field_names=[field.name for field in string_response_schema.inputs]
            + [CUSTOM_OUTPUTS_KEY],
        )
    # check if model has legacy output schema
    # TODO: (ML-41941) switch to block these eventually
    elif output_properties == {"type": "string", "required": True}:
        pass
    # check if the model has a Pyfunc ChatModel signature
    elif output_properties == {"type": "string", "name": "id", "required": True}:
        pass
    else:
        # output schema does not match any of the expected schemas
        raise ValueError(
            "The model's schema is not compatible with Agent Framework. The output schema must be "
            "either ChatCompletionResponse or StringResponse. "
            f"Output schema: {output_schema}"
        )


def _check_model_is_rag_compatible_helper(input_schema, output_schema):
    """
    Load the model and check if the schema is compatible with agent.
    """
    return _check_model_is_rag_compatible_new_signatures(
        input_schema, output_schema
    ) or _check_model_is_rag_compatible_legacy_signatures(input_schema, output_schema)


def get_workspace_url():
    """
    Retrieves the Databricks workspace URL. Falls back to the browser hostname
    where `get_workspace_url` returns None (ex. in serverless cluster). Finally, falls back
    to the Databricks SDK WorkspaceClient to handle local development
    """
    # Note: as of Nov 2024, the Databricks SDK returns an invalid URL on standard (non-serverless) jobs
    # clusters, but MLflow's databricks utils return the correct URL. We use the SDK as a fallback
    # as a result. Ideally the Databricks SDK could be used as the sole source of truth
    hostname = (
        databricks_utils.get_browser_hostname()
        or databricks_utils.get_workspace_url()
        or WorkspaceClient().config.host
    )
    if hostname and not urlparse(hostname).scheme:
        hostname = "https://" + hostname
    return hostname
