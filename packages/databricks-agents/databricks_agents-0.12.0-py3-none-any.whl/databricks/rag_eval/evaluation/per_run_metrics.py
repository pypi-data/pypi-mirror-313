"""Generate the metrics logged into MLflow."""

import collections
from typing import Dict, List, Optional

from mlflow import evaluation as mlflow_eval

from databricks.rag_eval import schemas
from databricks.rag_eval.config import assessment_config
from databricks.rag_eval.evaluation import entities
from databricks.rag_eval.utils import rating_utils

_AVERAGE_SUFFIX = "/average"
_PERCENTAGE_SUFFIX = "/percentage"

RunMetrics = Dict[str, float]


def generate_per_run_metrics(
    eval_results: List[entities.EvalResult],
) -> RunMetrics:
    """
    Generates per-run MLflow metrics.

    :param eval_results: List of EvalResult objects
    :return: Dictionary of aggregated MLflow metrics
    """

    result = {
        # Compute average for metrics with numeric or boolean values
        **{
            f"{metric_name}{_AVERAGE_SUFFIX}": avg_value
            for metric_name, avg_value in _compute_avg_for_numeric_or_bool_metric(
                eval_results
            ).items()
        },
        # Per-request answer assessments
        **{
            f"{schemas.get_response_llm_rating_col_name(assessment_name)}{_PERCENTAGE_SUFFIX}": true_rate
            for assessment_name, true_rate in _compute_true_rate_per_request_assessment(
                eval_results, assessment_config.AssessmentType.ANSWER
            ).items()
        },
        # Per-request retrieval assessments
        **{
            f"{schemas.get_retrieval_llm_rating_col_name(assessment_name, is_per_chunk=False)}{_PERCENTAGE_SUFFIX}": true_rate
            for assessment_name, true_rate in _compute_true_rate_per_request_assessment(
                eval_results, assessment_config.AssessmentType.RETRIEVAL_LIST
            ).items()
        },
    }

    # Overall assessment
    overall_assessment_rate = _compute_pass_rate_overall_assessment(eval_results)
    if overall_assessment_rate is not None:
        result[f"{schemas.OVERALL_ASSESSMENT_RATING_COL}{_PERCENTAGE_SUFFIX}"] = (
            overall_assessment_rate
        )

    # Count error in judges
    for assessment_name, error_count in _count_error_in_judges(eval_results).items():
        result[f"judge/{assessment_name}/error_count"] = error_count

    return result


def _compute_avg_for_numeric_or_bool_metric(
    eval_results: List[entities.EvalResult],
) -> Dict[str, float]:
    """
    Compute the average value across all eval results for metrics with numeric or boolean values.

    If the metric value is an Assessment object, the value of the Assessment is used.

    :param eval_results: List of EvalResult objects
    :return: Dictionary of average value for each metric in the group
    """
    metric_value_sums = collections.defaultdict(float)
    metric_value_counts = collections.defaultdict(int)
    for eval_result in eval_results:
        for metric_result in eval_result.metric_results:
            metric_value = (
                metric_result.metric_value.value
                if isinstance(metric_result.metric_value, mlflow_eval.Assessment)
                else metric_result.metric_value
            )
            metric_full_name = metric_result.metric_full_name
            if isinstance(metric_value, (int, float, bool)):
                metric_value_sums[metric_full_name] += metric_value
                metric_value_counts[metric_full_name] += 1
    return {
        metric_name: metric_value_sums[metric_name] / metric_value_counts[metric_name]
        for metric_name in metric_value_sums
        if metric_value_counts[metric_name] > 0
    }


def _compute_true_rate_per_request_assessment(
    eval_results: List[entities.EvalResult],
    expected_assessment_type: assessment_config.AssessmentType,
) -> Dict[str, float]:
    """
    Compute the rate of `True` in per-request assessment results.

    rate of `True` = count of `True` / count of non-null values.

    :param eval_results: List of EvalResult objects
    :param expected_assessment_type: Type of per-request assessment to compute results for (e.g., answer, retrieval_list)
    :return: Dictionary of rate of `True` for each per-request assessment
    """
    true_counts = collections.defaultdict(int)
    non_null_counts = collections.defaultdict(int)
    for eval_result in eval_results:
        for assessment_result in eval_result.assessment_results:

            # TODO(ML-45046): remove assessment type lookup in harness, rely on service
            # Get the assessment type from the built-in metrics. If the metric is not found, use the provided assessment type.
            try:
                builtin_assessment_config = assessment_config.get_builtin_assessment_config_with_service_assessment_name(
                    assessment_result.assessment_name
                )
                assessment_type = builtin_assessment_config.assessment_type
            except ValueError:
                assessment_type = assessment_result.assessment_type

            if (
                isinstance(assessment_result, entities.PerRequestAssessmentResult)
                and assessment_type == expected_assessment_type
            ):
                true_counts[assessment_result.assessment_name] += (
                    assessment_result.rating.categorical_value
                    == entities.CategoricalRating.YES
                )
                non_null_counts[assessment_result.assessment_name] += (
                    assessment_result.rating.categorical_value is not None
                )

    return {
        assessment_name: true_counts[assessment_name] / non_null_counts[assessment_name]
        for assessment_name in true_counts
        if non_null_counts[assessment_name] > 0
    }


def _compute_pass_rate_overall_assessment(
    eval_results: List[entities.EvalResult],
) -> Optional[float]:
    """
    Compute the rate of `YES` in the overall assessment results.

    rate of `YES` = count of `YES` / count of non-null values.

    :param eval_results: List of EvalResult objects
    :return: Rate of `YES` for the overall assessment, or None if no non-null values
    """
    pass_count = 0
    non_null_counts = 0
    for eval_result in eval_results:
        if (
            eval_result.overall_assessment
            and eval_result.overall_assessment.categorical_value is not None
        ):
            pass_count += (
                eval_result.overall_assessment.categorical_value
                == entities.CategoricalRating.YES
            )
            non_null_counts += 1
    return pass_count / non_null_counts if non_null_counts > 0 else None


def _count_error_in_judges(
    eval_results: List[entities.EvalResult],
) -> Dict[str, int]:
    """
    Count the number of errors in the assessment results.

    :param eval_results: List of EvalResult objects
    :return: Dictionary of count of errors for each assessment
    """
    error_counts = collections.defaultdict(int)
    for eval_result in eval_results:
        for assessment_result in eval_result.assessment_results:
            if isinstance(assessment_result, entities.PerRequestAssessmentResult):
                if _is_real_error_rating(assessment_result.rating):
                    error_counts[assessment_result.assessment_name] += 1
            elif isinstance(assessment_result, entities.PerChunkAssessmentResult):
                for positional_rating in assessment_result.positional_rating.values():
                    if _is_real_error_rating(positional_rating):
                        error_counts[assessment_result.assessment_name] += 1

    return error_counts


def _is_real_error_rating(rating: entities.Rating) -> bool:
    """Check if the rate is a real error. Missing input error is not considered as a real error."""
    return (
        rating.error_message is not None
        and not rating_utils.is_missing_input_error(rating.error_message)
        and not rating_utils.has_conflicting_input_error(rating.error_message)
    )
