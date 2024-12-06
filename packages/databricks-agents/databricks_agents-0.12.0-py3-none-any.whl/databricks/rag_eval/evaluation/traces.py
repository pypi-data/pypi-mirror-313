"""This module deals with trace and extracting information from traces."""

import dataclasses
import json
import logging
from typing import Any, List, Mapping, Optional

import mlflow.entities as mlflow_entities
import mlflow.models.dependencies_schemas as mlflow_dependencies_schemas
import mlflow.tracing.constant as mlflow_tracing_constant

from databricks.rag_eval.evaluation import entities
from databricks.rag_eval.utils import input_output_utils

_logger = logging.getLogger(__name__)


_DEFAULT_DOC_URI_COL = "doc_uri"


def _span_is_type(
    span: mlflow_entities.Span,
    span_type: str | List[str],
) -> bool:
    """Check if the span is of a certain span type or one of the span types in the collection"""
    if span.attributes is None:
        return False
    if not isinstance(span_type, List):
        span_type = [span_type]
    return (
        span.attributes.get(mlflow_tracing_constant.SpanAttributeKey.SPAN_TYPE)
        in span_type
    )


# ================== Retrieval Context ==================
def extract_retrieval_context_from_trace(
    trace: Optional[mlflow_entities.Trace],
) -> Optional[entities.RetrievalContext]:
    """
    Extract the retrieval context from the trace.

    Only consider the last retrieval span in the trace if there are multiple retrieval spans.

    If the trace does not have a retrieval span, return None.

    ⚠️ Warning: Please make sure to not throw exception. If fails, return None.

    :param trace: The trace
    :return: The retrieval context
    """
    if trace is None or trace.data is None:
        return None

    retrieval_spans = [
        span
        for span in trace.data.spans or []
        if _span_is_type(span, mlflow_entities.SpanType.RETRIEVER)
    ]
    if len(retrieval_spans) == 0:
        return None
    # Only consider the last retrieval span
    retrieval_span = retrieval_spans[-1]

    # Get the retriever schema from the trace info
    retriever_schema = _get_retriever_schema_from_trace(trace.info)
    return _extract_retrieval_context_from_retrieval_span(
        retrieval_span, retriever_schema
    )


def _get_retriever_schema_from_trace(
    trace_info: Optional[mlflow_entities.TraceInfo],
) -> Optional[mlflow_dependencies_schemas.RetrieverSchema]:
    """
    Get the retriever schema from the trace info tags.

    Retriever schema is stored in the trace info tags as a JSON string of list of retriever schemas.
    Only consider the last retriever schema if there are multiple retriever schemas.
    """
    if (
        trace_info is None
        or trace_info.tags is None
        or mlflow_dependencies_schemas.DependenciesSchemasType.RETRIEVERS.value
        not in trace_info.tags
    ):
        return None
    retriever_schemas = json.loads(
        trace_info.tags[
            mlflow_dependencies_schemas.DependenciesSchemasType.RETRIEVERS.value
        ]
    )
    # Only consider the last retriever schema
    return (
        mlflow_dependencies_schemas.RetrieverSchema.from_dict(retriever_schemas[-1])
        if isinstance(retriever_schemas, list) and len(retriever_schemas) > 0
        else None
    )


def _extract_retrieval_context_from_retrieval_span(
    span: mlflow_entities.Span,
    retriever_schema: Optional[mlflow_dependencies_schemas.RetrieverSchema],
) -> Optional[entities.RetrievalContext]:
    """Get the retrieval context from a retrieval span."""
    try:
        doc_uri_col = (
            retriever_schema.doc_uri
            if retriever_schema and retriever_schema.doc_uri
            else _DEFAULT_DOC_URI_COL
        )
        retriever_outputs = span.attributes.get(
            mlflow_tracing_constant.SpanAttributeKey.OUTPUTS
        )
        return entities.RetrievalContext(
            [
                (
                    entities.Chunk(
                        doc_uri=(
                            chunk.get("metadata", {}).get(doc_uri_col)
                            if chunk
                            else None
                        ),
                        content=chunk.get("page_content") if chunk else None,
                    )
                )
                for chunk in retriever_outputs or []
            ]
        )
    except Exception as e:
        _logger.debug(f"Fail to get retrieval context from span: {span}. Error: {e!r}")
        return None


# ================== Token Count ==================
@dataclasses.dataclass
class SpanTokenCount:
    prompt_token_count: Optional[int] = None
    completion_token_count: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SpanTokenCount":
        return cls(
            prompt_token_count=data.get("prompt_tokens", None),
            completion_token_count=data.get("completion_tokens", None),
        )


@dataclasses.dataclass
class TraceTokenCount:
    input_token_count: Optional[int] = None
    output_token_count: Optional[int] = None

    @property
    def total_token_count(self) -> Optional[int]:
        if self.input_token_count is not None and self.output_token_count is not None:
            return self.input_token_count + self.output_token_count
        return None


def compute_total_token_count(
    trace: Optional[mlflow_entities.Trace],
) -> TraceTokenCount:
    """
    Compute the total input/output tokens across all trace spans.

    ⚠️ Warning: Please make sure to not throw exception. If fails, return empty TraceTokenCount.

    :param trace: The trace object

    :return: Total input/output token counts
    """
    if trace is None or trace.data is None:
        return TraceTokenCount()

    # Only consider leaf spans that is of type LLM or CHAT_MODEL.
    # Depending on the implementation of LLM/CHAT_MODEL components,
    # a span may have multiple children spans that are also LLM/CHAT_MODEL spans.
    # But only the leaf spans send requests to the LLM.
    # To avoid double counting, we only consider leaf spans.
    leaf_spans = _get_leaf_spans(trace)
    leaf_llm_or_chat_model_spans = [
        span
        for span in leaf_spans
        if _span_is_type(
            span, [mlflow_entities.SpanType.LLM, mlflow_entities.SpanType.CHAT_MODEL]
        )
    ]

    input_token_counts = []
    output_token_counts = []
    for span in leaf_llm_or_chat_model_spans:
        span_token_count = _extract_span_token_counts(span)
        # Input
        if span_token_count.prompt_token_count is not None:
            input_token_counts.append(span_token_count.prompt_token_count)
        # Output
        if span_token_count.completion_token_count is not None:
            output_token_counts.append(span_token_count.completion_token_count)
    return TraceTokenCount(
        input_token_count=(
            sum(input_token_counts) if len(input_token_counts) > 0 else None
        ),
        output_token_count=(
            sum(output_token_counts) if len(output_token_counts) > 0 else None
        ),
    )


def _extract_span_token_counts(span: mlflow_entities.Span) -> SpanTokenCount:
    """Extract the token counts from the LLM/CHAT_MODEL span."""
    if (
        span.attributes is None
        or mlflow_tracing_constant.SpanAttributeKey.OUTPUTS not in span.attributes
    ):
        return SpanTokenCount()
    try:
        # See https://python.langchain.com/docs/modules/callbacks/#callback-handlers for output format
        # of CHAT_MODEL and LLM spans in LangChain
        if _span_is_type(
            span, [mlflow_entities.SpanType.CHAT_MODEL, mlflow_entities.SpanType.LLM]
        ):
            # The format of the output attribute for LLM/CHAT_MODEL is a ChatResult. Typically, the
            # token usage is either stored in 'usage' or 'llm_output' (ChatDatabricks in LangChain).
            # e.g. { 'llm_output': {'total_tokens': ...}, ... }
            span_outputs = span.attributes[
                mlflow_tracing_constant.SpanAttributeKey.OUTPUTS
            ]
            if "llm_output" in span_outputs:
                return SpanTokenCount.from_dict(span_outputs["llm_output"])
            elif "usage" in span_outputs:
                return SpanTokenCount.from_dict(span_outputs["usage"])
            else:
                return SpanTokenCount()
        else:
            # Span is not a LLM/CHAT_MODEL span, nothing to extract
            return SpanTokenCount()

    except Exception as e:
        _logger.debug(f"Fail to extract token counts from span: {span}. Error: {e!r}")
        return SpanTokenCount()


# ================== Model Input/Output ==================
def extract_model_output_from_trace(
    trace: Optional[mlflow_entities.Trace],
) -> Optional[input_output_utils.ModelOutput]:
    """
    Extract the model output from the trace.

    Model output should be recorded in the root span of the trace.

    ⚠️ Warning: Please make sure to not throw exception. If fails, return None.
    """
    if trace is None:
        return None
    root_span = _get_root_span(trace)
    if root_span is None:
        return None

    try:
        if (
            root_span.attributes is None
            or mlflow_tracing_constant.SpanAttributeKey.OUTPUTS
            not in root_span.attributes
        ):
            return None
        return root_span.attributes[mlflow_tracing_constant.SpanAttributeKey.OUTPUTS]

    except Exception as e:
        _logger.debug(
            f"Fail to extract model output from the root span: {root_span}. Error: {e!r}"
        )
        return None


# ================== Helper functions ==================
def _get_leaf_spans(trace: mlflow_entities.Trace) -> List[mlflow_entities.Span]:
    """Get all leaf spans in the trace."""
    if trace.data is None:
        return []
    spans = trace.data.spans or []
    leaf_spans_by_id = {span.span_id: span for span in spans}
    for span in spans:
        if span.parent_id:
            leaf_spans_by_id.pop(span.parent_id, None)
    return list(leaf_spans_by_id.values())


def _get_root_span(trace: mlflow_entities.Trace) -> Optional[mlflow_entities.Span]:
    """Get the root span in the trace."""
    if trace.data is None:
        return None
    spans = trace.data.spans or []
    # Root span is the span that has no parent
    return next((span for span in spans if span.parent_id is None), None)
