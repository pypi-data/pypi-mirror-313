from typing import List, TypeVar, Union

######################################################################
# Column/field names used in mlflow EvaluationDataset DataFrames
######################################################################
DOC_URI_COL = "doc_uri"
CHUNK_CONTENT_COL = "content"
TRACE_COL = "trace"
REQUEST_ID_COL = "request_id"
REQUEST_COL = "request"
EXPECTED_RETRIEVED_CONTEXT_COL = "expected_retrieved_context"
EXPECTED_RESPONSE_COL = "expected_response"
RESPONSE_COL = "response"
RETRIEVED_CONTEXT_COL = "retrieved_context"
GRADING_NOTES_COL = "grading_notes"
EXPECTED_FACTS_COL = "expected_facts"
EXTRA_EXPECTED_COL = "extra_expected"
SOURCE_TYPE_COL = "source_type"
SOURCE_ID_COL = "source_id"
MANAGED_EVALS_EVAL_ID_COL = "managed_evals_eval_id"
MANAGED_EVALS_DATASET_ID_COL = "managed_evals_dataset_id"

# Model error message column
MODEL_ERROR_MESSAGE_COL = "model_error_message"

######################################################################
# Column/field names for the output pandas DataFrame of mlflow.evaluate
######################################################################
_AGENT_PREFIX = "agent/"
_RETRIEVAL_PREFIX = "retrieval/"
_RESPONSE_PREFIX = "response/"
_LLM_JUDGED_PREFIX = "llm_judged/"
_GROUND_TRUTH_PREFIX = "ground_truth/"
CUSTOM_METRICS_PREFIX = "agent_metric/"

OVERALL_ASSESSMENT = "overall_assessment"

TOTAL_INPUT_TOKEN_COUNT_COL = _AGENT_PREFIX + "total_input_token_count"
TOTAL_OUTPUT_TOKEN_COUNT_COL = _AGENT_PREFIX + "total_output_token_count"
TOTAL_TOKEN_COUNT_COL = _AGENT_PREFIX + "total_token_count"
LATENCY_SECONDS_COL = _AGENT_PREFIX + "latency_seconds"
# Overall assessment columns
_OVERALL_ASSESSMENT_COL_PREFIX = _RESPONSE_PREFIX + OVERALL_ASSESSMENT + "/"
OVERALL_ASSESSMENT_RATING_COL = _OVERALL_ASSESSMENT_COL_PREFIX + "rating"
OVERALL_ASSESSMENT_RATIONALE_COL = _OVERALL_ASSESSMENT_COL_PREFIX + "rationale"

GROUND_TRUTH_RETRIEVAL_METRIC_COL_PREFIX = _RETRIEVAL_PREFIX + _GROUND_TRUTH_PREFIX
GROUND_TRUTH_DOCUMENT_PREFIX = "document_"
GROUND_TRUTH_DOCUMENT_RATING_COL = (
    GROUND_TRUTH_RETRIEVAL_METRIC_COL_PREFIX + GROUND_TRUTH_DOCUMENT_PREFIX + "ratings"
)
_LLM_JUDGED_RETRIEVAL_METRIC_COL_PREFIX = _RETRIEVAL_PREFIX + _LLM_JUDGED_PREFIX
_RATINGS_SUFFIX = "/ratings"
_RATIONALES_SUFFIX = "/rationales"
_ERROR_MESSAGES_SUFFIX = "/error_messages"

_LLM_JUDGED_RESPONSE_METRIC_COL_PREFIX = _RESPONSE_PREFIX + _LLM_JUDGED_PREFIX
_RATING_SUFFIX = "/rating"
_RATIONALE_SUFFIX = "/rationale"
_ERROR_MESSAGE_SUFFIX = "/error_message"

######################################################################
# Data types for the output pandas DataFrame of mlflow.evaluate
######################################################################
ASSESSMENT_RESULT_TYPE: TypeVar = TypeVar(
    "ASSESSMENT_RESULT_TYPE", bool, str, None, List[Union[bool, str, None]]
)


######################################################################
# Helper methods to get column names for the output pandas DataFrame of mlflow.evaluate
######################################################################


def get_response_llm_rating_col_name(assessment_name: str) -> str:
    """Returns the column name for the LLM judged response metric rating"""
    return f"{_LLM_JUDGED_RESPONSE_METRIC_COL_PREFIX}{assessment_name}{_RATING_SUFFIX}"


def get_response_llm_rationale_col_name(assessment_name: str) -> str:
    """Returns the column name for the LLM judged response metric rationale"""
    return (
        f"{_LLM_JUDGED_RESPONSE_METRIC_COL_PREFIX}{assessment_name}{_RATIONALE_SUFFIX}"
    )


def get_response_llm_error_message_col_name(assessment_name: str) -> str:
    """Returns the column name for the LLM judged response metric error message"""
    return f"{_LLM_JUDGED_RESPONSE_METRIC_COL_PREFIX}{assessment_name}{_ERROR_MESSAGE_SUFFIX}"


def is_response_llm_error_message_col(column_name: str) -> bool:
    """Returns True if the column name is a LLM judged response metric error message column"""
    return column_name.startswith(
        _LLM_JUDGED_RESPONSE_METRIC_COL_PREFIX
    ) and column_name.endswith(_ERROR_MESSAGE_SUFFIX)


def get_retrieval_llm_rating_col_name(
    assessment_name: str, is_per_chunk: bool = True
) -> str:
    """Returns the column name for the LLM judged retrieval metric rating"""
    suffix = _RATINGS_SUFFIX if is_per_chunk else _RATING_SUFFIX
    return f"{_LLM_JUDGED_RETRIEVAL_METRIC_COL_PREFIX}{assessment_name}{suffix}"


def get_retrieval_llm_rationale_col_name(
    assessment_name: str, is_per_chunk: bool = True
) -> str:
    """Returns the column name for the LLM judged retrieval metric rationale"""
    suffix = _RATIONALES_SUFFIX if is_per_chunk else _RATIONALE_SUFFIX
    return f"{_LLM_JUDGED_RETRIEVAL_METRIC_COL_PREFIX}{assessment_name}{suffix}"


def get_retrieval_llm_error_message_col_name(
    assessment_name: str, is_per_chunk: bool = True
) -> str:
    """Returns the column name for the LLM judged retrieval metric error message"""
    suffix = _ERROR_MESSAGES_SUFFIX if is_per_chunk else _ERROR_MESSAGE_SUFFIX
    return f"{_LLM_JUDGED_RETRIEVAL_METRIC_COL_PREFIX}{assessment_name}{suffix}"


def get_retrieval_llm_metric_col_name(metric_name: str) -> str:
    """Returns the column name for the LLM judged retrieval metric"""
    return f"{_LLM_JUDGED_RETRIEVAL_METRIC_COL_PREFIX}{metric_name}"


def is_retrieval_llm_error_message_col(column_name: str) -> bool:
    """Returns True if the column name is a LLM judged retrieval metric error message column"""
    return column_name.startswith(_LLM_JUDGED_RETRIEVAL_METRIC_COL_PREFIX) and (
        column_name.endswith(_ERROR_MESSAGES_SUFFIX)
        or column_name.endswith(_ERROR_MESSAGE_SUFFIX)
    )
