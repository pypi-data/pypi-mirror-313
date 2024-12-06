"""Helper functions to convert RagEval entities to MLflow entities."""

import time
from typing import List, Optional, Union

import mlflow
from mlflow import MlflowClient
from mlflow import evaluation as mlflow_eval
from mlflow.deployments import get_deploy_client
from mlflow.entities import metric as mlflow_metric
from mlflow.models import evaluation as mlflow_models_evaluation

from databricks.rag_eval import env_vars, schemas
from databricks.rag_eval.evaluation import datasets, entities
from databricks.rag_eval.utils import enum_utils, error_utils

_CHUNK_INDEX_KEY = "chunk_index"
_IS_OVERALL_ASSESSMENT_KEY = "is_overall_assessment"


class EvaluationErrorCode(enum_utils.StrEnum):
    MODEL_ERROR = "MODEL_ERROR"


def eval_result_to_mlflow_evaluation(
    eval_result: entities.EvalResult,
) -> mlflow_eval.Evaluation:
    """
    Convert an EvalResult object to an MLflow Evaluation object.

    :param eval_result: EvalResult object
    :return: MLflow Evaluation object
    """
    eval_item = eval_result.eval_item
    # Inputs
    inputs = {
        schemas.REQUEST_COL: eval_item.question,
    }
    # Outputs
    outputs = {}
    if eval_item.retrieval_context:
        outputs[schemas.RETRIEVED_CONTEXT_COL] = (
            eval_item.retrieval_context.to_output_dict()
        )
    if eval_item.answer:
        outputs[schemas.RESPONSE_COL] = eval_item.answer
    # Targets
    targets = {}
    if eval_item.ground_truth_answer:
        targets[schemas.EXPECTED_RESPONSE_COL] = eval_item.ground_truth_answer
    if eval_item.ground_truth_retrieval_context:
        targets[schemas.EXPECTED_RETRIEVED_CONTEXT_COL] = (
            eval_item.ground_truth_retrieval_context.to_output_dict()
        )
    if eval_item.grading_notes:
        targets[schemas.GRADING_NOTES_COL] = eval_item.grading_notes
    if eval_item.expected_facts:
        targets[schemas.EXPECTED_FACTS_COL] = eval_item.expected_facts
    if eval_item.extra_expected:
        targets[schemas.EXTRA_EXPECTED_COL] = eval_item.extra_expected
    # Assessments
    assessments = []
    for assessment_result in eval_result.assessment_results:
        assessments.extend(assessment_result_to_mlflow_assessments(assessment_result))
    # Overall assessment
    overall_assessment = _get_overall_assessment(eval_result)
    if overall_assessment:
        assessments.append(overall_assessment)
    # Assessments from custom metrics
    assessments.extend(
        _get_mlflow_assessment_to_log_from_metric_results(eval_result.metric_results)
    )
    # Metrics
    metrics = eval_result_to_mlflow_metrics(eval_result)

    # Tags
    tags = {}
    if eval_item.managed_evals_eval_id:
        tags[schemas.MANAGED_EVALS_EVAL_ID_COL] = eval_item.managed_evals_eval_id
    if eval_item.managed_evals_dataset_id:
        tags[schemas.MANAGED_EVALS_DATASET_ID_COL] = eval_item.managed_evals_dataset_id
    if eval_item.source_doc_uri:
        tags[schemas.SOURCE_ID_COL] = eval_item.source_doc_uri

    error_message = None
    error_code = None
    if eval_item.model_error_message:
        error_code = EvaluationErrorCode.MODEL_ERROR
        error_message = eval_item.model_error_message

    evaluation = mlflow_eval.Evaluation(
        inputs=inputs,
        outputs=outputs,
        inputs_id=eval_item.question_id,
        request_id=eval_item.trace.info.request_id if eval_item.trace else None,
        targets=targets,
        error_code=error_code,
        error_message=error_message,
        assessments=assessments,
        metrics=metrics,
        tags=tags,
    )

    return evaluation


def eval_result_to_mlflow_metrics(
    eval_result: entities.EvalResult,
) -> List[mlflow_metric.Metric]:
    """Get a list of MLflow Metric objects from an EvalResult object."""
    return [
        _construct_mlflow_metrics(
            key=k,
            value=v,
        )
        for k, v in eval_result.get_metrics_dict().items()
        # Do not log metrics with non-numeric-or-boolean values
        if isinstance(v, (int, float, bool))
    ]


def _construct_mlflow_metrics(
    key: str, value: Union[int, float, bool]
) -> mlflow_metric.Metric:
    """
    Construct an MLflow Metric object from key and value.
    Timestamp is the current time and step is 0.
    """
    return mlflow_metric.Metric(
        key=key,
        value=value,
        timestamp=int(time.time() * 1000),
        step=0,
    )


def assessment_result_to_mlflow_assessments(
    assessment_result: entities.AssessmentResult,
) -> List[mlflow_eval.Assessment]:
    """
    Convert an AssessmentResult object to a list of MLflow Assessment object.

    A single PerChunkAssessmentResult object can be converted to multiple MLflow Assessment objects.

    :param assessment_result: AssessmentResult object
    :return: MLflow Assessment object
    """
    if isinstance(assessment_result, entities.PerRequestAssessmentResult):
        return [
            mlflow_eval.Assessment(
                name=assessment_result.assessment_name,
                source=_convert_to_ai_judge_assessment_source(
                    assessment_result.assessment_source
                ),
                value=assessment_result.rating.categorical_value,
                rationale=assessment_result.rating.rationale,
                error_message=assessment_result.rating.error_message,
                error_code=assessment_result.rating.error_code,
            )
        ]
    elif isinstance(assessment_result, entities.PerChunkAssessmentResult):
        return [
            mlflow_eval.Assessment(
                name=assessment_result.assessment_name,
                source=_convert_to_ai_judge_assessment_source(
                    assessment_result.assessment_source
                ),
                value=rating.categorical_value,
                rationale=rating.rationale,
                error_message=rating.error_message,
                error_code=rating.error_code,
                metadata={_CHUNK_INDEX_KEY: index},
            )
            for index, rating in assessment_result.positional_rating.items()
        ]
    else:
        raise ValueError(
            f"Unsupported assessment result type: {type(assessment_result)}"
        )


def _get_mlflow_assessment_to_log_from_metric_results(
    metric_results: List[entities.MetricResult],
) -> List[mlflow_eval.Assessment]:
    """
    Get a list of MLflow Assessment objects from a list of MetricResult objects.

    Only consider metrics that have an Assessment as the value.
    Use the full name of the metric as the assessment name.
    """
    results = []
    for metric in metric_results:
        if isinstance(metric.metric_value, mlflow_eval.Assessment):
            results.append(
                mlflow_eval.Assessment(
                    name=metric.metric_full_name,
                    source=metric.metric_value.source,
                    value=metric.metric_value.value,
                    rationale=metric.metric_value.rationale,
                    metadata=metric.metric_value.metadata,
                    error_code=metric.metric_value.error_code,
                    error_message=metric.metric_value.error_message,
                )
            )
    return results


def _convert_to_ai_judge_assessment_source(
    assessment_source: entities.AssessmentSource,
) -> mlflow_eval.AssessmentSource:
    """
    Convert an AssessmentSource object to a MLflow AssessmentSource object.
    Source type is always AI_JUDGE.
    """
    return mlflow_eval.AssessmentSource(
        source_type=mlflow_eval.AssessmentSourceType.AI_JUDGE,
        source_id=assessment_source.source_id,
    )


def _get_overall_assessment(
    eval_result: entities.EvalResult,
) -> Optional[mlflow_eval.Assessment]:
    """
    Get optional overall assessment from a EvalResult object.

    :param eval_result: A EvalResult object
    :return: Optional overall assessment
    """
    return (
        mlflow_eval.Assessment(
            name=schemas.OVERALL_ASSESSMENT,
            source=_convert_to_ai_judge_assessment_source(
                entities.AssessmentSource.builtin()
            ),
            value=eval_result.overall_assessment.categorical_value,
            rationale=eval_result.overall_assessment.rationale,
            metadata={_IS_OVERALL_ASSESSMENT_KEY: True},
        )
        if eval_result.overall_assessment
        else None
    )


def _validate_mlflow_dataset(ds: mlflow_models_evaluation.EvaluationDataset):
    """Validates an MLflow evaluation dataset."""
    features_df = ds.features_data
    # Validate max number of rows in the eval dataset
    if len(features_df) > env_vars.RAG_EVAL_MAX_INPUT_ROWS.get():
        raise error_utils.ValidationError(
            f"The number of rows in the dataset exceeds the maximum: {env_vars.RAG_EVAL_MAX_INPUT_ROWS.get()}. "
            f"Got {len(features_df)} rows."
        )
    if ds.predictions_data is not None:
        assert features_df.shape[0] == ds.predictions_data.shape[0], (
            f"Features data and predictions must have the same number of rows. "
            f"Features: {features_df.shape[0]}, Predictions: {ds.predictions_data.shape[0]}"
        )


def mlflow_dataset_to_evaluation_dataset(
    ds: mlflow_models_evaluation.EvaluationDataset,
) -> datasets.EvaluationDataframe:
    """Creates an instance of the class from an MLflow evaluation dataset and model predictions."""
    _validate_mlflow_dataset(ds)
    df = ds.features_data.copy()
    if ds.predictions_data is not None:
        df[schemas.RESPONSE_COL] = ds.predictions_data
    return datasets.EvaluationDataframe(df)


def infer_experiment_from_endpoint(endpoint_name: str) -> mlflow.entities.Experiment:
    deploy_client = get_deploy_client("databricks")
    try:
        endpoint = deploy_client.get_endpoint(endpoint_name)
        served_models = endpoint.get("config", endpoint.get("pending_config", {})).get(
            "served_models", []
        )
        if not served_models:
            raise ValueError(f"No served models found for endpoint '{endpoint_name}'.")
        served_model = served_models[0]
        model_name = served_model.get("model_name")
        model_version = served_model.get("model_version")
        client = MlflowClient()
        model_info = client.get_model_version(model_name, model_version)
        experiment_id = client.get_run(model_info.run_id).info.experiment_id
        return mlflow.get_experiment(experiment_id)
    except Exception as e:
        raise Exception(
            f"Failed to infer the experiment for endpoint '{endpoint_name}'. "
            f"Please provide 'experiment_id' explicitly:\n{e}"
        ) from e
