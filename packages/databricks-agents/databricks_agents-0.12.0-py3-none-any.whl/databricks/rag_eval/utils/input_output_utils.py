"""Utilities to validate and manipulate model inputs and outputs."""

from typing import Any, Dict, List, NewType, Optional, Union

import mlflow.entities as mlflow_entities
import pandas as pd

from databricks.rag_eval.utils import collection_utils

ModelInput = NewType("ModelInput", Union[Dict[str, Any], str])
ModelOutput = NewType(
    "ModelOutput", Optional[Union[Dict[str, Any], str, List[Dict[str, Any]], List[str]]]
)

# ChatCompletionRequest fields
_MESSAGES = "messages"
_ROLE = "role"
_CONTENT = "content"
_USER_ROLE = "user"
_CHOICES = "choices"
_MESSAGE = "message"
# SplitChatMessagesRequest fields
_QUERY = "query"
_HISTORY = "history"

_RETURN_TRACE_FLAG = {
    "databricks_options": {
        "return_trace": True,
    }
}


def to_chat_completion_request(data: ModelInput) -> Dict[str, Any]:
    """Converts a model input to a ChatCompletionRequest. The input can be a string or a dict."""
    if isinstance(data, str):
        # For backward compatibility, we convert input strings into ChatCompletionRequests
        # before invoking the model.
        return {
            _MESSAGES: [
                {
                    _ROLE: _USER_ROLE,
                    _CONTENT: data,
                },
            ],
        }
    else:
        return data


def set_include_trace(model_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Set the flag to include trace in the model input.

    :param model_input: The model input
    :return: The model input with the flag set
    """
    return collection_utils.deep_update(model_input, _RETURN_TRACE_FLAG)


def to_chat_completion_response(data: Optional[str]) -> Optional[ModelOutput]:
    """Converts a model output to a ChatCompletionResponse."""
    if data is None:
        return None
    return {
        _CHOICES: [
            {
                _MESSAGE: {
                    _CONTENT: data,
                },
            },
        ],
    }


def extract_question_from_input(data: ModelInput) -> str:
    """
    Extract the user question/query from a model input.

    The following input formats are accepted:
    1. str: The user question/query
    2. Dictionary representations of ChatCompletionRequest: The last message in the conversation
    3. Dictionary representations of SplitChatMessagesRequest: The `query` field

    This method performs the minimal validations required to extract the input string.
    """
    if isinstance(data, str):
        return data
    if not isinstance(data, Dict):
        raise ValueError(f"Expected a dictionary, got {type(data)}")
    # ChatCompletionRequest input
    if (
        _MESSAGES in data
        and len(data[_MESSAGES]) > 0
        and data[_MESSAGES][-1].get(_CONTENT) is not None
    ):
        return data[_MESSAGES][-1][_CONTENT]
    # SplitChatMessagesRequest input
    if _QUERY in data:
        return data[_QUERY]
    raise ValueError(f"Invalid input: {data}")


def is_valid_input(data: ModelInput) -> bool:
    """Checks whether an input is considered valid for the purposes of evaluation.

    Valid input formats are described in the docstring for `input_to_string`.
    """
    try:
        return extract_question_from_input(data) is not None
    except ValueError:
        return False


def is_none_or_nan(value: Any) -> bool:
    """Checks whether a value is None or NaN."""
    # isinstance(value, float) check is needed to ensure that pd.isna is not called on an array.
    return value is None or (isinstance(value, float) and pd.isna(value))


def output_to_string(data: ModelOutput) -> Optional[str]:
    """Converts a model output to a string. The following output formats are accepted:
    1. str
    2. Dictionary representations of ChatCompletionResponse
    3. Dictionary representations of StringResponse

    If None is passed in, None is returned.

    This method performs the minimal validations required to extract the output string.
    """
    if is_none_or_nan(data):
        return None
    if isinstance(data, str):
        return data
    if isinstance(data, list) and len(data) > 0:
        # PyFuncModel.predict may wrap the output in a list
        return output_to_string(data[0])
    if not isinstance(data, Dict):
        raise ValueError(f"Expected a dictionary, got {type(data)}")
    # ChatCompletionResponse output
    if (
        _CHOICES in data
        and len(data[_CHOICES]) > 0
        and data[_CHOICES][0].get(_MESSAGE) is not None
        and data[_CHOICES][0][_MESSAGE].get(_CONTENT) is not None
    ):
        return data[_CHOICES][0][_MESSAGE][_CONTENT]
    # StringResponse output
    if _CONTENT in data:
        return data[_CONTENT]

    raise ValueError(f"Invalid output: {data}")


def extract_trace_from_output(data: ModelOutput) -> Optional[mlflow_entities.Trace]:
    """Extracts the trace from a model output. The trace is expected to be a dictionary."""
    if is_none_or_nan(data):
        return None
    if not isinstance(data, Dict):
        return None
    trace_dict = data.get("databricks_output", {}).get("trace")
    if trace_dict:
        try:
            return mlflow_entities.Trace.from_dict(trace_dict)
        except Exception:
            return None


def is_valid_output(data: ModelOutput) -> bool:
    """Checks whether an output is considered valid for the purposes of evaluation.

    Valid output formats are described in the docstring for `output_to_string`.
    """
    try:
        output_to_string(data)
        return True
    except ValueError:
        return False
