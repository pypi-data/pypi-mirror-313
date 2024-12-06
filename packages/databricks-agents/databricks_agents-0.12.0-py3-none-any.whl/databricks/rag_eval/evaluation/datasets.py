""" This module defines classes that wrap pandas DataFrames used in evaluation.

Wrappers handle data validation and normalization.
 """

from abc import ABC
from typing import Any, Iterable, List, Mapping, Set

import pandas as pd

from databricks.rag_eval import schemas
from databricks.rag_eval.evaluation import entities
from databricks.rag_eval.utils import (
    collection_utils,
    input_output_utils,
    serialization_utils,
)


class _InputColumn(ABC):
    """Represents a column in the evaluation dataset dataframe."""

    name: str
    required: bool

    @classmethod
    def validate(cls, df: pd.DataFrame) -> None:
        if cls.required and cls.name not in df.columns:
            raise ValueError(
                f'Column "{cls.name}" is required but not found in the input DataFrame.'
            )
        if cls.name not in df.columns:
            return
        col = df[cls.name]
        if cls.required:
            for index, value in col.items():
                if input_output_utils.is_none_or_nan(value):
                    raise ValueError(
                        f'Column "{cls.name}" is required and must not contain null values. '
                        f"Got null at row: {index}."
                    )


class _StringColumn(_InputColumn):
    @classmethod
    def validate(cls, df: pd.DataFrame):
        super().validate(df)

        # Skip validation if the column is not present
        if cls.name not in df.columns:
            return

        for index, value in df[cls.name].items():
            if input_output_utils.is_none_or_nan(value):
                # Null values are valid in optional column.
                continue
            if not isinstance(value, str):
                raise ValueError(
                    f"Column '{cls.name}' must contain only string values. "
                    f"Got '{value}' at row: {index}."
                )


def _mapping_has_field(
    mapping: Mapping[str, Any],
    field_name: str,
    expected_type: type,
    required: bool = False,
) -> bool:
    """
    Validates a field within a Mapping (eg dict). If `required`, the field must be present.
    If present, the field must be of the expected type.
    """
    field_value = mapping.get(field_name)
    if input_output_utils.is_none_or_nan(field_value):
        return not required
    return isinstance(field_value, expected_type)


class _ContextColumn(_InputColumn):
    @classmethod
    def _chunk_is_valid(cls, chunk: Any) -> bool:
        if input_output_utils.is_none_or_nan(chunk):
            return True  # Each chunk can be null
        if isinstance(chunk, str):
            return True  # Chunk can be just a doc_uri (str)
        if not isinstance(chunk, Mapping):
            return False  # Otherwise, chunk must be a map-like object
        keys = set(chunk.keys())
        # Check types of doc_uri and content
        if not _mapping_has_field(chunk, schemas.DOC_URI_COL, str, required=False):
            return False
        if not _mapping_has_field(
            chunk, schemas.CHUNK_CONTENT_COL, str, required=False
        ):
            return False
        # Invalid if dictionary contains any other keys
        if len(keys - {schemas.DOC_URI_COL, schemas.CHUNK_CONTENT_COL}) > 0:
            return False
        return True

    @classmethod
    def validate(cls, df: pd.DataFrame):
        super().validate(df)

        # Skip validation if the column is not present
        if cls.name not in df.columns:
            return

        for index, value in df[cls.name].items():
            if input_output_utils.is_none_or_nan(value):
                # Null values are valid in optional column.
                continue
            # Check that the value is an iterable of valid chunks. Strings, Mappings, and non-iterables are not allowed.
            if (
                isinstance(value, str)
                or isinstance(value, Mapping)
                or not (
                    isinstance(value, Iterable)
                    and all(cls._chunk_is_valid(item) for item in value)
                )
            ):
                raise ValueError(
                    f"Column '{cls.name}' must contain values of the form [doc_uri: str], [{{'doc_uri': str}}], or [{{'doc_uri': str}}, {{'content': str}}]. "
                    f"Got '{value}' at row: {index}."
                )


class _RequestIdCol(_StringColumn):
    name = schemas.REQUEST_ID_COL
    required = False


class _RequestCol(_InputColumn):
    name = schemas.REQUEST_COL
    required = True

    @classmethod
    def validate(cls, df: pd.DataFrame):
        super().validate(df)
        for index, value in df[cls.name].items():
            if input_output_utils.is_none_or_nan(value):
                continue
            if not input_output_utils.is_valid_input(value):
                raise ValueError(
                    f"Column '{cls.name}' must contain string values, or dictionaries matching schema {{ChatCompletionRequest, SplitChatMessagesRequest}}. Got '{value}' at row: {index}."
                )


class _ExpectedRetrievedContextCol(_ContextColumn):
    name = schemas.EXPECTED_RETRIEVED_CONTEXT_COL
    required = False


class _ResponseCol(_InputColumn):
    name = schemas.RESPONSE_COL
    required = False

    @classmethod
    def validate(cls, df: pd.DataFrame):
        super().validate(df)

        # Skip validation if the column is not present
        if cls.name not in df.columns:
            return

        for index, value in df[cls.name].items():
            if input_output_utils.is_none_or_nan(value):
                continue
            if not input_output_utils.is_valid_output(value):
                raise ValueError(
                    f"Column '{cls.name}' must contain string values, or dictionaries matching schema {{ChatCompletionResponse, StringResponse}}. Got '{value}' at row: {index}."
                )


class _ExpectedResponseCol(_ResponseCol):
    name = schemas.EXPECTED_RESPONSE_COL
    required = False
    # _ExpectedResponseCol has the same validation as _ResponseCol


class _RetrievedContextCol(_ContextColumn):
    name = schemas.RETRIEVED_CONTEXT_COL
    required = False


class _GradingNotesCol(_StringColumn):
    name = schemas.GRADING_NOTES_COL
    required = False


class _ExpectedFactsCol(_InputColumn):
    """
    List of strings.
    """

    name = schemas.EXPECTED_FACTS_COL
    required = False

    @classmethod
    def validate(cls, df: pd.DataFrame):
        super().validate(df)

        # Skip validation if the column is not present
        if cls.name not in df.columns:
            return

        for index, value in df[cls.name].items():
            if input_output_utils.is_none_or_nan(value):
                # Null values are valid in optional column.
                continue
            # Check that the value is an iterable of strings. String, Mapping, and non-iterable are not allowed.
            if (
                isinstance(value, str)
                or isinstance(value, Mapping)
                or not (
                    isinstance(value, Iterable)
                    and all(isinstance(item, str) for item in value)
                )
            ):
                raise ValueError(
                    f"Column '{cls.name}' must be iterable of strings like [str]. Each string is an expected fact. "
                    f"Got '{value}' at row: {index}."
                )


class _TraceCol(_InputColumn):
    name = schemas.TRACE_COL
    required = False

    @classmethod
    def validate(cls, df: pd.DataFrame):
        super().validate(df)

        # Skip validation if the column is not present
        if cls.name not in df.columns:
            return

        for index, value in df[cls.name].items():
            if input_output_utils.is_none_or_nan(value):
                continue

            try:
                # Try to deserialize the trace and fail if it is not a valid trace
                serialization_utils.deserialize_trace(value)
            except Exception as e:
                # TODO[ML-41664]: add a link to MLflow tracing documentation
                raise ValueError(
                    f"Column '{cls.name}' must contain valid serialized traces. Got '{value}' at row: {index}. Error: {e}"
                )


class _ExtraExpectedCol(_InputColumn):
    name = schemas.EXTRA_EXPECTED_COL
    required = False


class _ManagedEvalsEvalIdCol(_StringColumn):
    name = schemas.MANAGED_EVALS_EVAL_ID_COL
    required = False


class _ManagedEvalsDatasetIdCol(_StringColumn):
    name = schemas.MANAGED_EVALS_DATASET_ID_COL
    required = False


class EvaluationDataframe:
    """Wraps a DataFrame with the schema of an evaluation dataset, providing data validation and normalization."""

    COLS = [
        _RequestIdCol,
        _RequestCol,
        _ExpectedRetrievedContextCol,
        _ExpectedResponseCol,
        _ResponseCol,
        _RetrievedContextCol,
        _GradingNotesCol,
        _ExpectedFactsCol,
        _ExtraExpectedCol,
        _TraceCol,
        _ManagedEvalsEvalIdCol,
        _ManagedEvalsDatasetIdCol,
    ]

    def __init__(self, df: pd.DataFrame):
        self._df = df
        self.validate()

    def validate(self):
        """Validates the input DataFrame. This method is somewhat expensive, since each row of data is validated."""
        for col in self.COLS:
            col.validate(self._df)

    @classmethod
    def required_column_names(cls) -> Set[str]:
        return {col.name for col in cls.COLS if col.required}

    @classmethod
    def optional_column_names(cls) -> Set[str]:
        return {col.name for col in cls.COLS if not col.required}

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @property
    def eval_items(self) -> List[entities.EvalItem]:
        """Returns a list of EvalItems to evaluate."""
        return [
            # Convert numpy ndarray so that it's serializable
            entities.EvalItem.from_dict(collection_utils.convert_ndarray_to_list(row))
            for row in self._df.to_dict(orient="records")
        ]
