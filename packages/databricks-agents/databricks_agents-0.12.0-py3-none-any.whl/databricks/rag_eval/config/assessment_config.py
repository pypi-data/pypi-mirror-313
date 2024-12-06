"""All the internal configs."""

import dataclasses
import numbers
from dataclasses import field
from typing import Any, Dict, List, Optional

import mlflow.models
import pandas as pd

from databricks.rag_eval import constants, env_vars, schemas
from databricks.rag_eval.config import example_config
from databricks.rag_eval.utils import collection_utils, enum_utils, error_utils

_ALLOWED_VARIABLES = [
    schemas.REQUEST_COL,
    schemas.RESPONSE_COL,
    schemas.RETRIEVED_CONTEXT_COL,
    schemas.EXPECTED_RESPONSE_COL,
]

METRIC_METADATA__ASSESSMENT_TYPE = "assessment_type"
METRIC_METADATA__SCORE_THRESHOLD = "score_threshold"


@dataclasses.dataclass(frozen=True)
class BinaryConversion:
    """
    Conversion for the result of an assessment to a binary result.
    """

    threshold: float
    """
    Threshold value for converting to the binary.
    If not None, it means the output of the metric can be converted to a binary result.
    """
    greater_is_true: bool = field(default=True)
    """
    Whether to convert to True when the metric value is greater than the threshold or vice versa.
    If True, the binary result is True when the metric value score is greater than or equal to the threshold.
    If False, the binary result is True when the metric value score is less than or equal to the threshold.
    """

    def convert(self, score: Any) -> Optional[bool]:
        """
        Convert the score to a binary result based on the threshold and greater_is_true.

        If the score is not a real number, return None.
        """
        if isinstance(score, numbers.Real):
            # noinspection PyTypeChecker
            return (
                score >= self.threshold
                if self.greater_is_true
                else score <= self.threshold
            )
        else:
            return None

    def convert_to_score(self, rating: example_config.ExampleRating) -> str:
        """
        Convert an example rating to a score based on the threshold and greater_is_true.
        """
        return (
            "5"
            if self.greater_is_true == (rating == example_config.ExampleRating.YES)
            else "1"
        )


class AssessmentType(enum_utils.StrEnum):
    """Type of the assessment."""

    RETRIEVAL = "RETRIEVAL"
    """Assessment for a retrieved chunk. This is used to assess the quality of retrieval over a single chunk."""
    RETRIEVAL_LIST = "RETRIEVAL_LIST"
    """Assessment for all retrievals. This is used to assess the quality of retrieval over the whole context."""
    ANSWER = "ANSWER"
    """Assessment for answer. This is used to assess the quality of answer."""


class AssessmentInputRequirements(enum_utils.StrEnum):
    ASSESSMENT_INPUT_REQUIREMENTS_UNSPECIFIED = (
        "ASSESSMENT_INPUT_REQUIREMENTS_UNSPECIFIED"
    )
    CHAT_REQUEST = "CHAT_REQUEST"
    CHAT_RESPONSE = "CHAT_RESPONSE"
    RETRIEVAL_CONTEXT = "RETRIEVAL_CONTEXT"
    GROUND_TRUTH_CHAT_RESPONSE = "GROUND_TRUTH_CHAT_RESPONSE"
    GROUND_TRUTH_RETRIEVAL_CONTEXT = "GROUND_TRUTH_RETRIEVAL_CONTEXT"
    GRADING_NOTES = "GRADING_NOTES"
    EXPECTED_FACTS = "EXPECTED_FACTS"

    @classmethod
    def to_user_facing_column_name(
        cls, input_requirement: "AssessmentInputRequirements"
    ) -> str:
        match input_requirement:
            case cls.CHAT_REQUEST:
                return schemas.REQUEST_COL
            case cls.CHAT_RESPONSE:
                return schemas.RESPONSE_COL
            case cls.RETRIEVAL_CONTEXT:
                return schemas.RETRIEVED_CONTEXT_COL
            case cls.GROUND_TRUTH_CHAT_RESPONSE:
                return schemas.EXPECTED_RESPONSE_COL
            case cls.GROUND_TRUTH_RETRIEVAL_CONTEXT:
                return schemas.EXPECTED_RETRIEVED_CONTEXT_COL
            case cls.GRADING_NOTES:
                return schemas.GRADING_NOTES_COL
            case cls.EXPECTED_FACTS:
                return schemas.EXPECTED_FACTS_COL
            case _:
                raise ValueError(f"Unrecognized input requirement: {input_requirement}")


@dataclasses.dataclass(frozen=True)
class AssessmentInputRequirementExpression:
    required: List[AssessmentInputRequirements] = field(default_factory=list)
    """Required columns for the assessment."""

    at_least_one_of: List[AssessmentInputRequirements] = field(default_factory=list)
    """At least one of the columns is required for the assessment."""

    at_most_one_of: List[AssessmentInputRequirements] = field(default_factory=list)
    """At most one of the columns should be provided for the assessment."""

    @classmethod
    def get_user_facing_requirement_names(
        cls, requirements: List[AssessmentInputRequirements]
    ) -> List[str]:
        return [
            AssessmentInputRequirements.to_user_facing_column_name(requirement)
            for requirement in requirements
        ]


@dataclasses.dataclass(frozen=True)
class AssessmentConfig:
    assessment_name: str

    assessment_type: AssessmentType

    flip_rating: bool = field(default=False)
    """Whether to flip the rating from the service."""

    # TODO(ML-44244): Call the /chat-assessments-definitions endpoints to get input requirements
    require_question: bool = field(default=False)
    """Whether the assessment requires input to be present in the dataset to eval."""

    require_answer: bool = field(default=False)
    """Whether the assessment requires output to be present in the dataset to eval."""

    require_retrieval_context: bool = field(default=False)
    """Whether the assessment requires retrieval context to be present in the dataset to eval."""

    require_retrieval_context_array: bool = field(default=False)
    """Whether the assessment requires retrieval context array to be present in the dataset to eval."""

    require_ground_truth_answer: bool = field(default=False)
    """Whether the assessment requires ground truth answer to be present in the dataset to eval."""

    require_ground_truth_answer_or_expected_facts: bool = field(default=False)
    """Whether the assessment requires ground truth answer or expected facts to be present in the dataset to eval."""

    require_ground_truth_answer_or_expected_facts_or_grading_notes: bool = field(
        default=False
    )
    """Whether the assessment requires ground truth answer, expected facts, or grading notes to be present in the dataset to eval."""


@dataclasses.dataclass(frozen=True)
class BuiltinAssessmentConfig(AssessmentConfig):
    """
    Assessment represents a method to assess the quality of a RAG system.

    The method is defined by an MLflow EvaluationMetric object.
    """

    user_facing_assessment_name: Optional[str] = field(default=None)
    """If the service uses a different assessment name than the client, this is the user-facing name."""

    examples: List[example_config.AssessmentExample] = dataclasses.field(
        default_factory=list
    )

    domain_instructions: Optional[str] = field(default=None)
    """
    Domain-specific instruction to insert into the prompt for this assessment.
    """

    def __hash__(self):
        """
        Allow this object to be used as a key in a dictionary.
        """
        return hash(self.assessment_name)


@dataclasses.dataclass(frozen=True)
class EvaluationMetricAssessmentConfig(AssessmentConfig):
    """
    Represents a provided evaluation metric assessment configuration.

    This is used to represent an assessment that is provided by the user as an MLflow EvaluationMetric object.
    """

    binary_conversion: Optional[BinaryConversion] = field(default=None)
    """
    Configs how the result can be converted to binary.
    None if the result is not for converting to binary.
    """

    evaluation_metric: mlflow.models.EvaluationMetric = field(default=None)

    @classmethod
    def from_eval_metric(cls, evaluation_metric: mlflow.models.EvaluationMetric):
        """
        Create a EvaluationMetricAssessmentConfig object from an MLflow EvaluationMetric object.
        """
        try:
            assessment_type = AssessmentType(
                evaluation_metric.metric_metadata.get(
                    METRIC_METADATA__ASSESSMENT_TYPE, ""
                ).upper()
            )
        except Exception:
            raise error_utils.ValidationError(
                f"Invalid assessment type in evaluation metric: {evaluation_metric.name}. Evaluation metric "
                f"must contain metric metadata with key 'assessment_type' and value 'RETRIEVAL', 'RETRIEVAL_LIST', or 'ANSWER'."
            )

        threshold = evaluation_metric.metric_metadata.get(
            METRIC_METADATA__SCORE_THRESHOLD, 3
        )

        return cls(
            assessment_name=evaluation_metric.name,
            assessment_type=AssessmentType(assessment_type),
            evaluation_metric=evaluation_metric,
            binary_conversion=BinaryConversion(
                threshold=threshold, greater_is_true=evaluation_metric.greater_is_better
            ),
        )

    def __hash__(self):
        """
        Allow this object to be used as a key in a dictionary.
        """
        return hash(self.assessment_name)


def _get_col_names_in_example_df_for_assessment(
    assessment_conf: BuiltinAssessmentConfig,
) -> (str, str):
    """
    Get the rating and rationale column names for a given assessment in the examples
    DataFrame
    """
    if assessment_conf.assessment_type == AssessmentType.ANSWER:
        rating_col = schemas.get_response_llm_rating_col_name(
            assessment_conf.assessment_name
        )
        rationale_col = schemas.get_response_llm_rationale_col_name(
            assessment_conf.assessment_name
        )
    else:
        rating_col = schemas.get_retrieval_llm_rating_col_name(
            assessment_conf.assessment_name
        )
        rationale_col = schemas.get_retrieval_llm_rationale_col_name(
            assessment_conf.assessment_name
        )
    return rating_col, rationale_col


def _explode_examples_on_context_chunk_array(
    examples_list, rating_col, rationale_col, assessment_conf
):
    """
    Given a list of examples, explode the examples into one example per chunk for a given retrieval assessment,
    excluding cases where the context chunk is None or the chunk contains a None content.
    :param examples_list: List of examples in the form of pd.DataFrame record dicts
    :param rating_col: Name of the rating column for this assessment
    :param rationale_col: Name of the rationale column for this assessment
    :param assessment_conf: Config for this assessment
    """
    exploded_examples_list = []
    for example in examples_list:
        context_array = example[schemas.RETRIEVED_CONTEXT_COL]
        if len(context_array) != len(example[rating_col]) or len(context_array) != len(
            example[rationale_col]
        ):
            raise error_utils.ValidationError(
                f"Number of retrieved contexts, ratings, and rationales must match. "
                f"Got {len(context_array)} contexts, {len(example[rating_col])} ratings, "
                f"and {len(example[rationale_col])} rationales for assessment {assessment_conf.assessment_name}."
            )
        for i, context in enumerate(context_array):
            if context is None:
                continue
            content = context.get(schemas.CHUNK_CONTENT_COL, None)
            if content is None:
                continue
            new_example = dict(example)  # Copy example
            new_example[schemas.RETRIEVED_CONTEXT_COL] = content
            new_example[rating_col] = example[rating_col][i]
            new_example[rationale_col] = example[rationale_col][i]
            exploded_examples_list.append(new_example)

    return exploded_examples_list


def _get_examples_with_concatenated_context(examples_list):
    """
    Given a list of examples, return a list of examples where the context chunks for each example
    are concatenated into a single string. This excludes cases where the context chunk is None or the chunk
    contains a None content.
    """
    result = []
    for example in examples_list:
        context_array = example.get(schemas.RETRIEVED_CONTEXT_COL)
        if context_array:
            chunks = [
                context.get(schemas.CHUNK_CONTENT_COL, None)
                for context in context_array
                if context is not None
            ]
            context_str = constants.DEFAULT_CONTEXT_CONCATENATION_DELIMITER.join(
                [chunk for chunk in chunks if chunk is not None]
            )
            example[schemas.RETRIEVED_CONTEXT_COL] = context_str
        result.append(example)
    return result


def _get_example_configs_from_examples_df(
    examples_df: Optional[pd.DataFrame],
    assessment_conf: BuiltinAssessmentConfig,
) -> List[example_config.AssessmentExample]:
    """
    Given a DataFrame of examples in the same format as the mlflow.evaluate output df,
    return a list of AssessmentExample targeted at the given assessment config.
    """
    if examples_df is None:
        return []

    rating_col, rationale_col = _get_col_names_in_example_df_for_assessment(
        assessment_conf
    )

    if (
        rating_col not in examples_df.columns
        or rationale_col not in examples_df.columns
    ):
        return []

    # a set of columns that we require at least one of them to have values
    require_one_of_cols = set()
    # a set of columns that we require to have values in all of them
    required_cols = {
        schemas.REQUEST_COL,
        rating_col,
    }
    # a set of columns that are optional but will be included if present
    optional_cols = {rationale_col}

    if assessment_conf.require_answer:
        required_cols.add(schemas.RESPONSE_COL)
    if (
        assessment_conf.require_retrieval_context
        or assessment_conf.require_retrieval_context_array
    ):
        required_cols.add(schemas.RETRIEVED_CONTEXT_COL)
    if assessment_conf.require_ground_truth_answer:
        required_cols.add(schemas.EXPECTED_RESPONSE_COL)

    if assessment_conf.require_ground_truth_answer_or_expected_facts_or_grading_notes:
        require_one_of_cols.update(
            {
                schemas.EXPECTED_RESPONSE_COL,
                schemas.GRADING_NOTES_COL,
                schemas.EXPECTED_FACTS_COL,
            }
        )
    elif assessment_conf.require_ground_truth_answer_or_expected_facts:
        require_one_of_cols.update(
            {
                schemas.EXPECTED_RESPONSE_COL,
                schemas.EXPECTED_FACTS_COL,
            }
        )

    # Select the columns that needs to be included
    selected_cols = set(examples_df.columns) & (
        required_cols | optional_cols | require_one_of_cols
    )
    relevant_df = examples_df[selected_cols]

    # Exclude rows where all require_one_of_cols are None
    if len(require_one_of_cols) != 0:
        relevant_df = relevant_df.dropna(
            how="all", subset=set(relevant_df.columns) & require_one_of_cols
        )

    # Exclude rows where any required_cols is None
    relevant_df = relevant_df.dropna(subset=set(relevant_df.columns) & required_cols)

    examples_list = relevant_df.to_dict(orient="records")

    if len(examples_list) > env_vars.RAG_EVAL_MAX_FEW_SHOT_EXAMPLES.get():
        raise error_utils.ValidationError(
            f"The number of rows in `examples_df` exceeds the maximum: {env_vars.RAG_EVAL_MAX_FEW_SHOT_EXAMPLES.get()}. "
            f"Got {len(examples_list)} rows. Please reduce the number of examples."
        )

    if assessment_conf.require_retrieval_context_array:
        # This is a retrieval metric. Need to return one example per chunk
        exploded_examples_list = _explode_examples_on_context_chunk_array(
            examples_list, rating_col, rationale_col, assessment_conf
        )
    elif assessment_conf.require_retrieval_context:
        # Answer metric. Return example with concatenated context string
        exploded_examples_list = _get_examples_with_concatenated_context(examples_list)
    else:
        exploded_examples_list = (
            examples_list  # Don't need to explode, context will not be used
        )

    if len(exploded_examples_list) > env_vars.RAG_EVAL_MAX_FEW_SHOT_EXAMPLES.get():
        raise error_utils.ValidationError(
            f"The total number of chunks in `examples_df` exceeds the maximum: {env_vars.RAG_EVAL_MAX_FEW_SHOT_EXAMPLES.get()}. "
            f"Got {len(exploded_examples_list)} chunks. Please reduce the number of rows or chunks per row."
        )

    return [
        example_config.AssessmentExample(
            variables=collection_utils.omit_keys(
                example,
                [
                    rating_col,
                    rationale_col,
                ],
            ),
            rating=example_config.ExampleRating(example.get(rating_col)),
            rationale=example.get(rationale_col),
        )
        for example in exploded_examples_list
    ]


def create_builtin_assessment_configs(
    assessment_list: List[str],
    examples_df: Optional[pd.DataFrame],
    domain_instructions: Optional[Dict[str, str]],
) -> List[BuiltinAssessmentConfig]:
    """
    Parse a list of builtin assessments (and optional examples) into a list of BuiltinAssessmentConfigs
    """

    assessment_configs = []
    if domain_instructions is None:
        domain_instructions = {}

    for assessment_name in assessment_list:
        builtin_assessment_conf = (
            _get_builtin_assessment_config_with_name_with_instruction(
                assessment_name, domain_instructions.get(assessment_name, None)
            )
        )

        df_examples = _get_example_configs_from_examples_df(
            examples_df, builtin_assessment_conf
        )
        builtin_assessment_conf = dataclasses.replace(
            builtin_assessment_conf, examples=df_examples
        )
        assessment_configs.append(builtin_assessment_conf)

    return assessment_configs


def create_custom_eval_metric_assessment_configs(
    eval_metrics: Optional[List[mlflow.models.EvaluationMetric]],
) -> List[EvaluationMetricAssessmentConfig]:
    """
    Create AssessmentJudge objects from a list of custom evaluation metrics.
    """
    if eval_metrics is None:
        return []
    return [
        EvaluationMetricAssessmentConfig.from_eval_metric(metric)
        for metric in eval_metrics
        if isinstance(metric, mlflow.models.EvaluationMetric)
    ]


# ================ Builtin Assessments ================
GROUNDEDNESS = BuiltinAssessmentConfig(
    assessment_name="groundedness",
    assessment_type=AssessmentType.ANSWER,
    require_question=True,
    require_answer=True,
    require_retrieval_context=True,
)

CORRECTNESS = BuiltinAssessmentConfig(
    assessment_name="correctness",
    assessment_type=AssessmentType.ANSWER,
    require_question=True,
    require_answer=True,
    require_ground_truth_answer_or_expected_facts_or_grading_notes=True,
)

HARMFULNESS = BuiltinAssessmentConfig(
    assessment_name="harmfulness",
    user_facing_assessment_name="safety",
    assessment_type=AssessmentType.ANSWER,
    require_answer=True,
    flip_rating=True,
)

RELEVANCE_TO_QUERY = BuiltinAssessmentConfig(
    assessment_name="relevance_to_query",
    assessment_type=AssessmentType.ANSWER,
    require_question=True,
    require_answer=True,
)

CONTEXT_SUFFICIENCY = BuiltinAssessmentConfig(
    assessment_name="context_sufficiency",
    assessment_type=AssessmentType.RETRIEVAL_LIST,
    require_question=True,
    require_ground_truth_answer_or_expected_facts=True,
    require_retrieval_context=True,
)

CHUNK_RELEVANCE = BuiltinAssessmentConfig(
    assessment_name="chunk_relevance",
    assessment_type=AssessmentType.RETRIEVAL,
    require_question=True,
    require_retrieval_context_array=True,
)


def _builtin_assessment_configs() -> List[BuiltinAssessmentConfig]:
    """Returns the list of built-in assessment configs"""
    return [
        HARMFULNESS,
        GROUNDEDNESS,
        CORRECTNESS,
        RELEVANCE_TO_QUERY,
        CHUNK_RELEVANCE,
        CONTEXT_SUFFICIENCY,
    ]


def builtin_assessment_names() -> List[str]:
    """Returns the list of built-in assessment names"""
    return [
        assessment_config.assessment_name
        for assessment_config in _builtin_assessment_configs()
    ]


def builtin_answer_assessment_names() -> List[str]:
    """Returns the list of built-in answer assessment configs"""
    return [
        assessment_config.assessment_name
        for assessment_config in _builtin_assessment_configs()
        if assessment_config.assessment_type == AssessmentType.ANSWER
    ]


def builtin_retrieval_assessment_names() -> List[str]:
    """Returns the list of built-in retrieval assessment configs"""
    return [
        assessment_config.assessment_name
        for assessment_config in _builtin_assessment_configs()
        if assessment_config.assessment_type == AssessmentType.RETRIEVAL
    ]


def builtin_retrieval_list_assessment_names() -> List[str]:
    """Returns the list of built-in retrieval assessment configs"""
    return [
        assessment_config.assessment_name
        for assessment_config in _builtin_assessment_configs()
        if assessment_config.assessment_type == AssessmentType.RETRIEVAL_LIST
    ]


def get_builtin_assessment_config_with_service_assessment_name(
    name: str,
) -> BuiltinAssessmentConfig:
    """
    Returns the built-in assessment config with the given service assessment name
    :param name: The service assessment name of the assessment
    :returns: The built-in assessment config
    """
    for assessment_config in _builtin_assessment_configs():
        if assessment_config.assessment_name == name:
            return assessment_config

    raise ValueError(
        f"Assessment '{name}' not found in the builtin assessments. "
        f"Available assessments: {builtin_assessment_names()}."
    )


def get_builtin_assessment_config_with_eval_assessment_name(
    name: str,
) -> BuiltinAssessmentConfig:
    """
    Returns the built-in assessment config with the given eval assessment name
    :param name: The eval assessment name of the assessment
    :returns: The built-in assessment config
    """
    for assessment_config in _builtin_assessment_configs():
        if translate_to_eval_assessment_name(assessment_config.assessment_name) == name:
            return assessment_config

    available_assessment_names = [
        translate_to_eval_assessment_name(name) for name in builtin_assessment_names()
    ]
    raise ValueError(
        f"Assessment '{name}' not found in the builtin assessments. "
        f"Available assessments: {available_assessment_names}."
    )


def _get_builtin_assessment_config_with_name_with_instruction(
    eval_assessment_name: str,
    domain_instructions: Optional[str],
) -> BuiltinAssessmentConfig:
    """Returns the built-in assessment config with the given user-facing name and adds on an instruction"""
    assessment_config = get_builtin_assessment_config_with_eval_assessment_name(
        eval_assessment_name
    )
    return dataclasses.replace(
        assessment_config, domain_instructions=domain_instructions
    )


def needs_flip(service_assessment_name: str) -> bool:
    """Returns whether the rating needs to be flipped for a given assessment."""
    return get_builtin_assessment_config_with_service_assessment_name(
        service_assessment_name
    ).flip_rating


def translate_to_eval_assessment_name(service_assessment_name: str) -> str:
    """
    Given a service assessment name, returns the corresponding user-facing assessment name. If no
    user-facing name is specified, assume the service name is the user-facing name.
    """
    if service_assessment_name not in builtin_assessment_names():
        return service_assessment_name
    assessment = get_builtin_assessment_config_with_service_assessment_name(
        service_assessment_name
    )
    return (
        assessment.user_facing_assessment_name
        if assessment.user_facing_assessment_name is not None
        else assessment.assessment_name
    )
