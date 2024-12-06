"""Entities for evaluation."""

import dataclasses
import functools
import hashlib
from typing import Any, Collection, Dict, List, Mapping, Optional, TypeAlias, Union

import mlflow.entities as mlflow_entities
import pandas as pd
from mlflow import evaluation as mlflow_eval

from databricks.rag_eval import constants, schemas
from databricks.rag_eval.config import (
    assessment_config,
    example_config,
)
from databricks.rag_eval.utils import (
    collection_utils,
    enum_utils,
    input_output_utils,
    serialization_utils,
)

ChunkInputData = Union[str, Dict[str, Any]]
RetrievalContextInputData = List[Optional[ChunkInputData]]


@dataclasses.dataclass
class Chunk:
    doc_uri: Optional[str] = None
    content: Optional[str] = None

    @classmethod
    def from_input_data(cls, input_data: Optional[ChunkInputData]) -> Optional["Chunk"]:
        """
        Construct a Chunk from a dictionary optionally containing doc_uri and content.

        An input chunk of a retrieval context can be:
          - A doc URI; or
          - A dictionary with the schema defined in schemas.CHUNK_SCHEMA
        """
        if input_output_utils.is_none_or_nan(input_data):
            return None
        if isinstance(input_data, str):
            return cls(doc_uri=input_data)
        else:
            return cls(
                doc_uri=input_data.get(schemas.DOC_URI_COL),
                content=input_data.get(schemas.CHUNK_CONTENT_COL),
            )


class RetrievalContext(List[Optional[Chunk]]):
    def __init__(self, chunks: Collection[Optional[Chunk]]):
        super().__init__(chunks)

    def concat_chunk_content(
        self, delimiter: str = constants.DEFAULT_CONTEXT_CONCATENATION_DELIMITER
    ) -> Optional[str]:
        """
        Concatenate the non-empty content of the chunks to a string with the given delimiter.
        Return None if all the contents are empty.
        """
        non_empty_contents = [
            chunk.content for chunk in self if chunk is not None and chunk.content
        ]
        return delimiter.join(non_empty_contents) if non_empty_contents else None

    def get_doc_uris(self) -> List[Optional[str]]:
        """Get the list of doc URIs in the retrieval context."""
        return [chunk.doc_uri for chunk in self if chunk is not None]

    def to_output_dict(self) -> List[Dict[str, str]]:
        """Convert the RetrievalContext to a list of dictionaries with the schema defined in schemas.CHUNK_SCHEMA."""
        return [
            (
                {
                    schemas.DOC_URI_COL: chunk.doc_uri,
                    schemas.CHUNK_CONTENT_COL: chunk.content,
                }
                if chunk is not None
                else None
            )
            for chunk in self
        ]

    @classmethod
    def from_input_data(
        cls, input_data: Optional[RetrievalContextInputData]
    ) -> Optional["RetrievalContext"]:
        """
        Construct a RetrievalContext from the input.

        Input can be:
        - A list of doc URIs
        - A list of dictionaries with the schema defined in schemas.CHUNK_SCHEMA
        """
        if input_output_utils.is_none_or_nan(input_data):
            return None
        return cls([Chunk.from_input_data(chunk_data) for chunk_data in input_data])


class CategoricalRating(enum_utils.StrEnum):
    """A categorical rating for an assessment."""

    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"

    @classmethod
    def _missing_(cls, value: str):
        value = value.lower()
        for member in cls:
            if member == value:
                return member
        return cls.UNKNOWN

    @classmethod
    def from_example_rating(
        cls, rating: example_config.ExampleRating
    ) -> "CategoricalRating":
        """Convert an ExampleRating to a CategoricalRating."""
        match rating:
            case example_config.ExampleRating.YES:
                return cls.YES
            case example_config.ExampleRating.NO:
                return cls.NO
            case _:
                return cls.UNKNOWN


@dataclasses.dataclass
class Rating:
    double_value: Optional[float]
    rationale: Optional[str]
    categorical_value: Optional[CategoricalRating]
    error_message: Optional[str]
    error_code: Optional[str]

    @classmethod
    def value(
        cls,
        *,
        rationale: Optional[str] = None,
        double_value: Optional[float] = None,
        categorical_value: Optional[CategoricalRating | str] = None,
    ) -> "Rating":
        """Build a normal Rating with a categorical value, a double value, and a rationale."""
        if categorical_value is not None and not isinstance(
            categorical_value, CategoricalRating
        ):
            categorical_value = CategoricalRating(categorical_value)
        return cls(
            double_value=double_value,
            rationale=rationale,
            categorical_value=categorical_value,
            error_message=None,
            error_code=None,
        )

    @classmethod
    def error(
        cls, error_message: str, error_code: Optional[str | int] = None
    ) -> "Rating":
        """Build an error Rating with an error message and an optional error code."""
        if isinstance(error_code, int):
            error_code = str(error_code)
        return cls(
            double_value=None,
            rationale=None,
            categorical_value=None,
            error_message=error_message,
            error_code=error_code or "UNKNOWN",
        )

    @classmethod
    def flip(cls, rating: "Rating") -> "Rating":
        """Built a Rating with the inverse categorical and float values of the input Rating."""
        if rating.double_value is not None and (
            rating.double_value < 1.0 or rating.double_value > 5.0
        ):
            raise ValueError(
                f"Cannot flip the rating of double value: {rating.double_value}."
            )

        match rating.categorical_value:
            case CategoricalRating.YES:
                flipped_categorical_value = CategoricalRating.NO
                flipped_double_value = 1.0
            case CategoricalRating.NO:
                flipped_categorical_value = CategoricalRating.YES
                flipped_double_value = 5.0
            case CategoricalRating.UNKNOWN:
                flipped_categorical_value = CategoricalRating.UNKNOWN
                flipped_double_value = None
            case None:
                flipped_categorical_value = None
                flipped_double_value = None
            case _:
                raise ValueError(
                    f"Cannot flip the rating of categorical value: {rating.categorical_value}"
                )

        return cls(
            double_value=flipped_double_value,
            rationale=rating.rationale,
            categorical_value=flipped_categorical_value,
            error_message=rating.error_message,
            error_code=rating.error_code,
        )


PositionalRating: TypeAlias = Mapping[int, Rating]
"""
A mapping from position to rating.
Position refers to the position of the chunk in the retrieval context.
It is used to represent the ratings of the chunks in the retrieval context.
"""


@functools.total_ordering
@dataclasses.dataclass
class EvalItem:
    """
    Represents a row in the evaluation dataset. It contains information needed to evaluate a question.
    """

    question_id: str
    """Unique identifier for the eval item."""

    question: str
    """String representation of the model input that is used for evaluation."""

    raw_request: Any = None
    """Passed as input to the model when `evaluate` is called with a model."""

    answer: Optional[str] = None
    """String representation of the model output that is used for evaluation."""

    raw_response: Any = None
    """Raw model output from an agent."""

    retrieval_context: Optional[RetrievalContext] = None
    """Retrieval context that is used for evaluation."""

    ground_truth_answer: Optional[str] = None
    """String representation of the ground truth answer."""

    ground_truth_retrieval_context: Optional[RetrievalContext] = None
    """Ground truth retrieval context."""

    grading_notes: Optional[str] = None
    """String representation of the grading notes."""

    expected_facts: Optional[List[str]] = None
    """List of expected facts to help evaluate the answer."""

    extra_expected: Optional[Any] = None
    """Extra expected data to help evaluate the answer."""

    trace: Optional[mlflow_entities.Trace] = None
    """Trace of the model invocation."""

    managed_evals_eval_id: Optional[str] = None
    """Unique identifier for the managed-evals eval item."""

    managed_evals_dataset_id: Optional[str] = None
    """Unique identifier for the managed-evals dataset."""

    model_error_message: Optional[str] = None
    """Error message if the model invocation fails."""

    source_doc_uri: Optional[str] = None
    """Source document URI that the eval is synthetically generated from."""

    source_type: Optional[str] = None
    """Source of the eval item. e.g. HUMAN, SYNTHETIC_FROM_DOC, PRODUCTION_LOG..."""

    @property
    def concatenated_retrieval_context(self) -> Optional[str]:
        """Get the concatenated content of the retrieval context.
        Return None if there is no non-empty retrieval context content."""
        return (
            self.retrieval_context.concat_chunk_content()
            if self.retrieval_context
            else None
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EvalItem":
        """
        Create an EvalItem from a row of MLflow EvaluationDataset data.
        """
        retrieved_context = RetrievalContext.from_input_data(
            data.get(schemas.RETRIEVED_CONTEXT_COL)
        )

        expected_retrieved_context = RetrievalContext.from_input_data(
            data.get(schemas.EXPECTED_RETRIEVED_CONTEXT_COL)
        )

        raw_request = data[schemas.REQUEST_COL]
        question = input_output_utils.extract_question_from_input(raw_request)
        question_id = data.get(schemas.REQUEST_ID_COL)
        if input_output_utils.is_none_or_nan(question_id):
            question_id = hashlib.sha256(question.encode()).hexdigest()
        answer = input_output_utils.output_to_string(data.get(schemas.RESPONSE_COL))
        ground_truth_answer = input_output_utils.output_to_string(
            data.get(schemas.EXPECTED_RESPONSE_COL)
        )

        grading_notes = data.get(schemas.GRADING_NOTES_COL)
        grading_notes = (
            grading_notes
            if not input_output_utils.is_none_or_nan(grading_notes)
            else None
        )

        expected_facts = data.get(schemas.EXPECTED_FACTS_COL)
        expected_facts = (
            list(expected_facts)
            if not input_output_utils.is_none_or_nan(expected_facts)
            else None
        )

        extra_expected = data.get(schemas.EXTRA_EXPECTED_COL)

        trace = data.get(schemas.TRACE_COL)
        if input_output_utils.is_none_or_nan(trace):
            trace = None
        else:
            trace = serialization_utils.deserialize_trace(trace)

        source_doc_uri = data.get(schemas.SOURCE_ID_COL)

        managed_evals_eval_id = data.get(schemas.MANAGED_EVALS_EVAL_ID_COL)
        managed_evals_dataset_id = data.get(schemas.MANAGED_EVALS_DATASET_ID_COL)

        return cls(
            question_id=question_id,
            question=question,
            raw_request=raw_request,
            answer=answer,
            retrieval_context=retrieved_context,
            ground_truth_answer=ground_truth_answer,
            ground_truth_retrieval_context=expected_retrieved_context,
            grading_notes=grading_notes,
            expected_facts=expected_facts,
            extra_expected=extra_expected,
            trace=trace,
            source_doc_uri=source_doc_uri,
            managed_evals_eval_id=managed_evals_eval_id,
            managed_evals_dataset_id=managed_evals_dataset_id,
        )

    def as_dict(
        self, *, use_chat_completion_request_format: bool = False
    ) -> Dict[str, Any]:
        """
        Get as a dictionary. Keys are defined in schemas. Exclude None values.

        :param use_chat_completion_request_format: Whether to use the chat completion request format for the request.
        """
        request = self.raw_request or self.question
        if use_chat_completion_request_format:
            request = input_output_utils.to_chat_completion_request(request)
        inputs = {
            schemas.REQUEST_ID_COL: self.question_id,
            schemas.REQUEST_COL: request,
            schemas.RESPONSE_COL: self.answer,
            schemas.EXPECTED_RETRIEVED_CONTEXT_COL: (
                self.ground_truth_retrieval_context.to_output_dict()
                if self.ground_truth_retrieval_context
                else None
            ),
            schemas.EXPECTED_RESPONSE_COL: self.ground_truth_answer,
            schemas.RETRIEVED_CONTEXT_COL: (
                self.retrieval_context.to_output_dict()
                if self.retrieval_context
                else None
            ),
            schemas.GRADING_NOTES_COL: self.grading_notes,
            schemas.EXPECTED_FACTS_COL: self.expected_facts,
            schemas.TRACE_COL: serialization_utils.serialize_trace(self.trace),
            schemas.MODEL_ERROR_MESSAGE_COL: self.model_error_message,
            schemas.SOURCE_TYPE_COL: self.source_type,
            schemas.SOURCE_ID_COL: self.source_doc_uri,
            schemas.MANAGED_EVALS_EVAL_ID_COL: self.managed_evals_eval_id,
            schemas.MANAGED_EVALS_DATASET_ID_COL: self.managed_evals_dataset_id,
        }
        return collection_utils.drop_none_values(inputs)

    def __eq__(self, other):
        if not hasattr(other, "question_id"):
            return NotImplemented
        return self.question_id == other.question_id

    def __lt__(self, other):
        if not hasattr(other, "question_id"):
            return NotImplemented
        return self.question_id < other.question_id


@dataclasses.dataclass
class AssessmentSource:
    source_id: str

    @classmethod
    def builtin(cls) -> "AssessmentSource":
        return cls(
            source_id="databricks",
        )

    @classmethod
    def custom(cls) -> "AssessmentSource":
        return cls(
            source_id="custom",
        )


@dataclasses.dataclass(frozen=True, eq=True)
class AssessmentResult:
    """Holds the result of an assessment."""

    assessment_name: str
    assessment_type: assessment_config.AssessmentType
    assessment_source: AssessmentSource

    def __lt__(self, other):
        if not isinstance(other, AssessmentResult):
            return NotImplemented
        # Compare by assessment_name
        return self.assessment_name < other.assessment_name


@dataclasses.dataclass(frozen=True, eq=True)
class PerRequestAssessmentResult(AssessmentResult):
    """Holds the result of a per-request assessment."""

    rating: Rating
    assessment_type: assessment_config.AssessmentType


@dataclasses.dataclass(frozen=True, eq=True)
class PerChunkAssessmentResult(AssessmentResult):
    """Holds the result of a per-chunk assessment."""

    positional_rating: PositionalRating
    assessment_type: assessment_config.AssessmentType = dataclasses.field(
        init=False, default=assessment_config.AssessmentType.RETRIEVAL
    )


@dataclasses.dataclass(frozen=True, eq=True, order=True)
class MetricResult:
    """Holds the result of a metric."""

    metric_name: str
    metric_value: Any

    @property
    def metric_full_name(self) -> str:
        """
        Get the full name of the metric.

        If the value is an assessment, and the assessment has a non-empty name, the full name will be the concatenation of
          the metric name and the assessment name;
        Otherwise, the full name will be the metric name.
        """
        if (
            isinstance(self.metric_value, mlflow_eval.Assessment)
            and self.metric_value.name
        ):
            return f"{self.metric_name}/{self.metric_value.name}"
        return self.metric_name


@dataclasses.dataclass
class EvalResult:
    """Holds the result of the evaluation for an eval item."""

    eval_item: EvalItem
    assessment_results: List[AssessmentResult]

    overall_assessment: Optional[Rating]
    """Overall assessment of the eval item."""

    metric_results: List[MetricResult]
    """A collection of MetricResult."""

    def __post_init__(self):
        if not self.assessment_results:
            self.assessment_results = []
        if not self.metric_results:
            self.metric_results = []

    def __eq__(self, other):
        if not isinstance(other, EvalResult):
            return False
        # noinspection PyTypeChecker
        return (
            self.eval_item == other.eval_item
            and sorted(self.assessment_results) == sorted(other.assessment_results)
            and self.overall_assessment == other.overall_assessment
            and sorted(self.metric_results) == sorted(other.metric_results)
        )

    def get_metrics_dict(self) -> Dict[str, Any]:
        """Get the metrics as a dictionary. Keys are defined in schemas."""
        metrics: Dict[str, Any] = {
            metric.metric_full_name: metric.metric_value
            for metric in self.metric_results
            # Exclude assessments from metrics, they are handled in get_assessment_results_dict
            if not isinstance(metric.metric_value, mlflow_eval.Assessment)
        }
        # Remove None values in metrics
        return collection_utils.drop_none_values(metrics)

    def get_assessment_results_dict(self) -> Dict[str, schemas.ASSESSMENT_RESULT_TYPE]:
        """Get the assessment results as a dictionary. Keys are defined in schemas."""
        assessments: Dict[str, schemas.ASSESSMENT_RESULT_TYPE] = {}
        for assessment in self.assessment_results:
            # TODO(ML-45046): remove assessment type lookup in harness, rely on service
            # Get the assessment type from the built-in metrics. If the metric is not found, use the provided assessment type.
            try:
                builtin_assessment_config = assessment_config.get_builtin_assessment_config_with_service_assessment_name(
                    assessment.assessment_name
                )
                assessment_type = builtin_assessment_config.assessment_type
            except ValueError:
                assessment_type = assessment.assessment_type

            if (
                isinstance(assessment, PerRequestAssessmentResult)
                and assessment_type == assessment_config.AssessmentType.RETRIEVAL_LIST
            ):
                if assessment.rating.categorical_value is not None:
                    assessments[
                        schemas.get_retrieval_llm_rating_col_name(
                            assessment.assessment_name, is_per_chunk=False
                        )
                    ] = assessment.rating.categorical_value
                if assessment.rating.rationale is not None:
                    assessments[
                        schemas.get_retrieval_llm_rationale_col_name(
                            assessment.assessment_name, is_per_chunk=False
                        )
                    ] = assessment.rating.rationale
                if assessment.rating.error_message is not None:
                    assessments[
                        schemas.get_retrieval_llm_error_message_col_name(
                            assessment.assessment_name, is_per_chunk=False
                        )
                    ] = assessment.rating.error_message
            elif isinstance(assessment, PerRequestAssessmentResult):
                if assessment.rating.categorical_value is not None:
                    assessments[
                        schemas.get_response_llm_rating_col_name(
                            assessment.assessment_name
                        )
                    ] = assessment.rating.categorical_value
                if assessment.rating.rationale is not None:
                    assessments[
                        schemas.get_response_llm_rationale_col_name(
                            assessment.assessment_name
                        )
                    ] = assessment.rating.rationale
                if assessment.rating.error_message is not None:
                    assessments[
                        schemas.get_response_llm_error_message_col_name(
                            assessment.assessment_name
                        )
                    ] = assessment.rating.error_message
            elif isinstance(assessment, PerChunkAssessmentResult):
                # Convert the positional_rating to a list of ratings ordered by position
                # For missing positions, use an error rating. This should not happen in practice.
                ratings_ordered_by_position: List[Rating] = (
                    collection_utils.position_map_to_list(
                        assessment.positional_rating,
                        default=Rating.error("Missing rating"),
                    )
                )
                if any(
                    rating.categorical_value is not None
                    for rating in ratings_ordered_by_position
                ):
                    assessments[
                        schemas.get_retrieval_llm_rating_col_name(
                            assessment.assessment_name
                        )
                    ] = [
                        rating.categorical_value
                        for rating in ratings_ordered_by_position
                    ]
                if any(
                    rating.rationale is not None
                    for rating in ratings_ordered_by_position
                ):
                    assessments[
                        schemas.get_retrieval_llm_rationale_col_name(
                            assessment.assessment_name
                        )
                    ] = [rating.rationale for rating in ratings_ordered_by_position]
                if any(
                    rating.error_message is not None
                    for rating in ratings_ordered_by_position
                ):
                    assessments[
                        schemas.get_retrieval_llm_error_message_col_name(
                            assessment.assessment_name
                        )
                    ] = [rating.error_message for rating in ratings_ordered_by_position]
        for metric in self.metric_results:
            if isinstance(metric.metric_value, mlflow_eval.Assessment):
                if metric.metric_value.value is not None:
                    assessments[f"{metric.metric_full_name}/value"] = (
                        metric.metric_value.value
                    )

                if metric.metric_value.rationale is not None:
                    assessments[f"{metric.metric_full_name}/rationale"] = (
                        metric.metric_value.rationale
                    )

                if metric.metric_value.error_message is not None:
                    assessments[f"{metric.metric_full_name}/error_message"] = (
                        metric.metric_value.error_message
                    )

                if metric.metric_value.error_code is not None:
                    assessments[f"{metric.metric_full_name}/error_code"] = (
                        metric.metric_value.error_code
                    )
        return assessments

    def get_overall_assessment_dict(self) -> Dict[str, schemas.ASSESSMENT_RESULT_TYPE]:
        """Get the overall assessment as a dictionary. Keys are defined in schemas."""
        result = {}
        if (
            self.overall_assessment
            and self.overall_assessment.categorical_value is not None
        ):
            result[schemas.OVERALL_ASSESSMENT_RATING_COL] = (
                self.overall_assessment.categorical_value
            )
        if self.overall_assessment and self.overall_assessment.rationale is not None:
            result[schemas.OVERALL_ASSESSMENT_RATIONALE_COL] = (
                self.overall_assessment.rationale
            )
        return result

    def to_pd_series(self) -> pd.Series:
        """Converts the EvalResult to a flattened pd.Series."""
        inputs = self.eval_item.as_dict()
        assessments = self.get_assessment_results_dict()
        metrics = self.get_metrics_dict()
        overall_assessment = self.get_overall_assessment_dict()

        # Merge dictionaries and convert to pd.Series
        combined_data = {**inputs, **overall_assessment, **assessments, **metrics}
        return pd.Series(combined_data)
