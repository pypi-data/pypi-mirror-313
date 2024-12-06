"""Entry point to the evaluation harness"""

from __future__ import annotations

import logging
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache, partialmethod
from typing import Iterable, List, Optional, Union

import mlflow
from tqdm.auto import tqdm

from databricks.rag_eval import context, env_vars, session
from databricks.rag_eval.config import assessment_config, evaluation_config
from databricks.rag_eval.evaluation import (
    assessments,
    custom_metrics,
    datasets,
    entities,
    metrics,
    models,
    rca,
    traces,
)
from databricks.rag_eval.utils import input_output_utils, rate_limit, rating_utils

_logger = logging.getLogger(__name__)

EvalResults = List[entities.EvalResult]


def run(
    *,
    eval_dataset: Union[datasets.EvaluationDataframe, List[entities.EvalItem]],
    config: evaluation_config.EvaluationConfig,
    model=None,
) -> EvalResults:
    """
    Run the logic of the eval harness.

    :param eval_dataset: The evaluation dataset
    :param config: The evaluation config
    :param model: Optional model to use for generating responses and traces
    """

    eval_items = (
        eval_dataset.eval_items
        if isinstance(eval_dataset, datasets.EvaluationDataframe)
        else eval_dataset
    )

    # Disable tqdm progress bar by default so that the progress bars inside MLflow eval_fn do not show
    tqdm.__init__ = partialmethod(tqdm.__init__, disable=True)

    # emit custom assessment usage event prior to all logic
    _emit_custom_assessments_usage_event_if_present(config.assessment_configs)

    eval_results = []
    with ThreadPoolExecutor(
        max_workers=env_vars.RAG_EVAL_MAX_WORKERS.get()
    ) as executor:
        futures = [
            executor.submit(
                _run_single,
                eval_item=eval_item,
                assessments_to_run=_get_assessments_to_run(config, eval_item),
                custom_metrics_to_run=config.custom_metrics,
                model=model,
            )
            for eval_item in eval_items
        ]

        futures_as_completed = as_completed(futures)
        # Add a progress bar to show the progress of the assessments
        futures_as_completed = tqdm(
            futures_as_completed,
            total=len(futures),
            disable=False,
            desc="Evaluating",
            smoothing=0,  # 0 means using average speed for remaining time estimates
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [Elapsed: {elapsed}, Remaining: {remaining}]",
        )

        for future in futures_as_completed:
            result = future.result()
            eval_results.append(result)
    return _postprocess_eval_results(eval_results)


def _get_assessments_to_run(
    config: evaluation_config.EvaluationConfig, eval_item: entities.EvalItem
) -> List[assessments.Assessment]:
    """
    Get the minimum required list of assessments for a given evaluation item.
    :param config: The evaluation config
    :param eval_item: Evaluation item
    :return: Minimum list of assessments to run
    """
    assessments_to_run: List[assessments.Assessment] = _get_assessments_for_configs(
        tuple(config.assessment_configs)
    )
    # If the assessments are provided by the user, do not filter them
    if not config.is_default_config:
        return assessments_to_run

    if (
        eval_item.ground_truth_answer is not None
        or eval_item.expected_facts is not None
    ):
        enabled_metrics = (
            evaluation_config.default_metrics_with_expected_response_or_expected_facts()
        )
    elif eval_item.grading_notes is not None:
        enabled_metrics = evaluation_config.default_metrics_with_grading_notes()
    else:
        enabled_metrics = (
            evaluation_config.default_metrics_without_ground_truth_or_expected_facts_or_grading_notes()
        )

    minimum_assessments_to_run = [
        assessment
        for assessment in assessments_to_run
        if (
            isinstance(assessment, assessments.BuiltInAssessment)
            and assessment.config.assessment_name in enabled_metrics
        )
        or isinstance(assessment, assessments.EvaluationMetricAssessment)
    ]
    return minimum_assessments_to_run


def _postprocess_eval_results(
    eval_results: List[entities.EvalResult],
) -> List[entities.EvalResult]:
    """
    Postprocess the eval results by:
    1. Moving missing input field errors (identified by "Error[1001]") from error_messages to rationales.
    2. If all error messages for a particular assessment are the same across all eval items, change these errors to null and instead log the error.

    After the completion of ML-41351, we should migrate this logic to run as a pre-check before sending requests to the managed-rag service.
    """
    # Track errors for each assessment
    assessment_error_counts = defaultdict(
        lambda: defaultdict(int)
    )  # assessment_name -> normalized_error_message -> count
    total_assessments = defaultdict(int)  # assessment_name -> count
    error_messages = defaultdict(str)  # assessment_name -> error_message

    # First pass: Count errors and track common errors
    for eval_result in eval_results:
        for assessment_result in eval_result.assessment_results:
            assessment_name = assessment_result.assessment_name
            total_assessments[assessment_name] += 1
            if isinstance(assessment_result, entities.PerRequestAssessmentResult):
                rating = assessment_result.rating
                if rating_utils.is_missing_input_error(
                    rating.error_message
                ) or rating_utils.has_conflicting_input_error(rating.error_message):
                    normalized_message = rating_utils.normalize_error_message(
                        rating.error_message
                    )
                    assessment_error_counts[assessment_name][normalized_message] += 1
                    error_messages[assessment_name] = rating.error_message
            elif isinstance(assessment_result, entities.PerChunkAssessmentResult):
                for rating in assessment_result.positional_rating.values():
                    if rating_utils.is_missing_input_error(
                        rating.error_message
                    ) or rating_utils.has_conflicting_input_error(rating.error_message):
                        normalized_message = rating_utils.normalize_error_message(
                            rating.error_message
                        )
                        assessment_error_counts[assessment_name][
                            normalized_message
                        ] += 1
                        error_messages[assessment_name] = rating.error_message

    # Determine common errors
    common_errors = {
        assessment_name: error_messages[assessment_name]
        for assessment_name, errors in assessment_error_counts.items()
        if len(errors) == 1
        and list(errors.values())[0] == total_assessments[assessment_name]
    }

    # Log common errors
    for assessment_name, error_message in common_errors.items():
        missing_fields = rating_utils.extract_missing_fields_from_missing_input_error(
            error_message
        )
        conflicting_fields = (
            rating_utils.extract_conflicting_fields_from_conflicting_input_error(
                error_message
            )
        )

        if missing_fields:
            reason = f"missing input fields: {missing_fields}"
        elif len(conflicting_fields) > 0:
            conflicting_fields_str = " and ".join(
                list(map(lambda x: f"[{x}]", conflicting_fields))
            )
            reason = f"conflicting input fields. Pick one of: {conflicting_fields_str}"
        else:
            reason = rating_utils.normalize_error_message(error_message)

        session.current_session().append_warning(
            f"Skipped metric '{assessment_name}' due to {reason}"
        )

    return eval_results


def _run_single(
    eval_item: entities.EvalItem,
    assessments_to_run: List[assessments.Assessment],
    custom_metrics_to_run: List[custom_metrics.CustomMetric],
    model: Optional[mlflow.pyfunc.PyFuncModel] = None,
) -> entities.EvalResult:
    """
    Run the logic of the eval harness for a single eval item.

    :param eval_item: The eval item to evaluate
    :param assessments_to_run: The list of assessments to run
    :param model: Optional model to use for generating responses and traces
    """
    if model:
        eval_item = _populate_model_result_to_eval_item(
            eval_item=eval_item,
            model_result=models.invoke_model(model, eval_item),
        )
        # Skip the evaluation if invoking the model failed
        if eval_item.model_error_message is not None:
            try:
                context.get_context().build_managed_rag_client().emit_client_error_usage_event(
                    eval_item.model_error_message
                )
            except Exception:
                # Telemetry logging failures are non-fatal.
                pass
            return _no_op_eval_result(eval_item)
    else:
        eval_item = _maybe_populate_eval_item_with_trace(eval_item)
    assessment_results = assessments.generate_llm_assessments(
        eval_item=eval_item,
        assessments=assessments_to_run,
    )

    return entities.EvalResult(
        eval_item=eval_item,
        assessment_results=assessment_results,
        overall_assessment=rca.compute_overall_assessment(assessment_results),
        metric_results=metrics.compute_eval_metrics(
            eval_item=eval_item,
            assessment_results=assessment_results,
            metrics=metrics.BUILT_IN_METRICS + custom_metrics_to_run,
        ),
    )


def _no_op_eval_result(eval_item: entities.EvalItem) -> entities.EvalResult:
    """
    Create a no-op eval result for the eval item for skipping the evaluation.

    :param eval_item: The eval item to create a no-op eval result for
    :return: The no-op eval result
    """
    return entities.EvalResult(
        eval_item=eval_item,
        assessment_results=[],
        overall_assessment=None,
        metric_results=[],
    )


def _populate_model_result_to_eval_item(
    eval_item: entities.EvalItem, model_result: models.ModelResult
) -> entities.EvalItem:
    """
    Populate the model result to the eval item in place.

    :param eval_item: The eval item to populate the model result
    :param model_result: The model result to populate
    :return: The populated eval item
    """
    eval_item.answer = model_result.response
    eval_item.raw_response = model_result.raw_model_output
    eval_item.retrieval_context = model_result.retrieval_context
    eval_item.trace = model_result.trace
    eval_item.model_error_message = model_result.error_message
    return eval_item


def _maybe_populate_eval_item_with_trace(eval_item: entities.EvalItem):
    """
    Populate the eval item in place by extracting additional information from the trace.

    Keep the existing values in the eval item if they already exist.
    """
    # Skip if the trace is None
    if eval_item.trace is None:
        return eval_item

    eval_item.answer = (
        input_output_utils.output_to_string(
            traces.extract_model_output_from_trace(eval_item.trace)
        )
        if eval_item.answer is None
        else eval_item.answer
    )
    eval_item.retrieval_context = (
        traces.extract_retrieval_context_from_trace(eval_item.trace)
        if eval_item.retrieval_context is None
        else eval_item.retrieval_context
    )

    return eval_item


@lru_cache(maxsize=16)
def _get_assessments_for_configs(
    assessment_configs: Iterable[assessment_config.AssessmentConfig],
) -> List[assessments.Assessment]:
    """
    Construct a list of assessments for an EvaluationConfig.
    """
    builtin_rate_limiter = _build_rate_limiter_for_assessment()
    custom_rate_limiter = _build_rate_limiter_for_assessment()
    managed_rag_client = context.get_context().build_managed_rag_client()

    results = []
    for assessment_conf in assessment_configs:
        if isinstance(assessment_conf, assessment_config.BuiltinAssessmentConfig):
            assessment_name = assessment_conf.assessment_name
            try:
                input_requirement_expression = (
                    managed_rag_client.get_assessment_metric_definitions(
                        [assessment_name]
                    ).get(assessment_name, None)
                )
            except Exception as e:
                # Log the error and continue with the assessment
                _logger.debug(
                    f"Error in collecting input requirements for {assessment_name}: {e}"
                )
                input_requirement_expression = None

            results.append(
                assessments.BuiltInAssessment(
                    config=assessment_conf,
                    rate_limiter=builtin_rate_limiter,
                    managed_rag_client=managed_rag_client,
                    input_requirement_expression=input_requirement_expression,
                )
            )
        elif isinstance(
            assessment_conf, assessment_config.EvaluationMetricAssessmentConfig
        ):
            results.append(
                assessments.EvaluationMetricAssessment(
                    config=assessment_conf,
                    rate_limiter=custom_rate_limiter,
                    managed_rag_client=managed_rag_client,
                )
            )
    return results


def _build_rate_limiter_for_assessment() -> rate_limit.RateLimiter:
    """Build a rate limiter for the assessment."""
    # Return a no-op rate limiter if the rate limiter for assessment is not enabled
    if not env_vars.RAG_EVAL_ENABLE_RATE_LIMIT_FOR_ASSESSMENT.get():
        return rate_limit.RateLimiter.no_op()

    # For now, rate limiter config is from environment variables
    rate_limit_config = rate_limit.RateLimitConfig(
        quota=env_vars.RAG_EVAL_RATE_LIMIT_QUOTA.get(),
        time_window_in_seconds=env_vars.RAG_EVAL_RATE_LIMIT_TIME_WINDOW_IN_SECONDS.get(),
    )
    return rate_limit.RateLimiter.build(
        quota=rate_limit_config.quota,
        time_window_in_seconds=rate_limit_config.time_window_in_seconds,
    )


def _emit_custom_assessments_usage_event_if_present(
    assessment_configs: List[assessment_config.AssessmentConfig],
):
    managed_rag_client = context.get_context().build_managed_rag_client()

    evaluation_metric_configs = [
        assessment_conf
        for assessment_conf in assessment_configs
        if isinstance(
            assessment_conf, assessment_config.EvaluationMetricAssessmentConfig
        )
    ]

    if evaluation_metric_configs:
        try:
            batch_size = session.current_session().session_batch_size
            managed_rag_client.emit_chat_assessment_usage_event(
                evaluation_metric_configs, batch_size
            )
        except Exception:
            # Telemetry logging failures are non-fatal.
            # Don't want to indicate to users that we're emitting data
            # TODO [ML-43811]: handle this case better since it means we have a loss of billing data
            pass
