"""Log the evaluation results to MLflow using the MLflow evaluation logging API."""

from typing import List

from mlflow import evaluation as mlflow_eval

from databricks.rag_eval.evaluation import entities
from databricks.rag_eval.mlflow import mlflow_utils

_CHUNK_INDEX_KEY = "chunk_index"
_IS_OVERALL_ASSESSMENT_KEY = "is_overall_assessment"


def log_eval_results(
    eval_results: List[entities.EvalResult],
) -> List[mlflow_eval.Evaluation]:
    """
    Log the evaluation results to MLflow using the MLflow evaluation logging API.

    :param eval_results: List of EvalResult objects
    :return: List of logged MLflow Evaluation objects
    """
    return mlflow_eval.log_evaluations(
        evaluations=[
            mlflow_utils.eval_result_to_mlflow_evaluation(eval_result)
            for eval_result in eval_results
        ],
    )
