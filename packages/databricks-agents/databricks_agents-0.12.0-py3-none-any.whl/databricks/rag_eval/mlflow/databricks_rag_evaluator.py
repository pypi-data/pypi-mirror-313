import json
import logging
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import mlflow
import pandas as pd
from jinja2 import Environment, PackageLoader, select_autoescape
from mlflow import models as mlflow_models
from mlflow.models import evaluation as mlflow_evaluation
from mlflow.models.evaluation import artifacts as mlflow_artifacts
from mlflow.utils import mlflow_tags

from databricks.rag_eval import (
    constants,
    context,
    evaluator_plugin,
    schemas,
    session,
)
from databricks.rag_eval.config import evaluation_config
from databricks.rag_eval.evaluation import entities, harness, per_run_metrics
from databricks.rag_eval.mlflow import eval_logging, mlflow_utils
from databricks.rag_eval.utils import error_utils, workspace_url_resolver

_logger = logging.getLogger(__name__)


def _log_pandas_df_artifact(pandas_df, artifact_name):
    """
    Logs a pandas DataFrame as a JSON artifact, then returns an EvaluationArtifact object.
    """
    mlflow_artifact_name = f"{artifact_name}.json"
    mlflow.log_table(pandas_df, mlflow_artifact_name)
    return mlflow_artifacts.JsonEvaluationArtifact(
        uri=mlflow.get_artifact_uri(mlflow_artifact_name),
    )


def _count_passing(results_df: pd.DataFrame) -> Optional[int]:
    """
    Counts the number of rows that are considered passing in the evaluation results.

    For now, we consider a row passing if the overall assessment rating is YES.

    Return None if the overall assessment column is not present in the results_df.

    :param results_df: DataFrame containing evaluation results
    :return: Number of rows that are considered passing
    """
    overall_assessment_rating_col = schemas.OVERALL_ASSESSMENT_RATING_COL
    return (
        (
            results_df[overall_assessment_rating_col] == entities.CategoricalRating.YES
        ).sum()
        if overall_assessment_rating_col in results_df.columns
        else None
    )


def _count_model_errors(results_df: pd.DataFrame) -> int:
    """
    Counts the number of rows that have model errors in the evaluation results.

    :param results_df: DataFrame containing evaluation results
    :return: Number of rows that have model errors
    """
    return (
        results_df[schemas.MODEL_ERROR_MESSAGE_COL].notnull().sum()
        if schemas.MODEL_ERROR_MESSAGE_COL in results_df.columns
        else 0
    )


def _count_judge_errors(results_df: pd.DataFrame) -> int:
    """
    Counts the number of rows that contain judge errors in the evaluation results.

    :param results_df: DataFrame containing evaluation results
    :return: Number of rows that contain judge errors
    """
    count = 0
    try:
        for index, row in results_df.iterrows():
            contains_judge_error = False
            for col in results_df.columns:
                if schemas.is_response_llm_error_message_col(col):
                    if pd.notnull(row[col]):
                        contains_judge_error = True
                elif schemas.is_retrieval_llm_error_message_col(col):
                    col_not_null = pd.notnull(row[col])
                    if (
                        any(col_not_null)
                        if isinstance(col_not_null, Iterable)
                        else col_not_null
                    ):
                        contains_judge_error = True
                else:
                    continue
            if contains_judge_error:
                count += 1
    except Exception as ex:
        # This operation shouldn't fail. Catch exception just in case.
        _logger.debug(f"Error in counting judge errors: {ex}")
        pass
    return count


def generate_summary(results_df: pd.DataFrame) -> Optional[str]:
    """
    Generates a short summary of the evaluation results suitable for printing.

    :param results_df: DataFrame containing evaluation results
    :return: A summary string.
    """

    num_rows = len(results_df)
    num_passing = _count_passing(results_df)

    return (
        f"{num_passing}/{num_rows} pass all assessments"
        if num_passing is not None
        else None
    )


def generate_error_messages(results_df: pd.DataFrame) -> List[str]:
    """
    Generates a list of strings, where each string is a line of the error message.

    :param results_df: DataFrame containing evaluation results
    :return: A list of strings, where each string is a line of the error message.
    """

    num_rows = len(results_df)
    num_model_errors = _count_model_errors(results_df)
    num_judge_errors = _count_judge_errors(results_df)

    error_messages = []
    if num_model_errors > 0:
        error_messages.append(f"{num_model_errors}/{num_rows} contain model errors")
    if num_judge_errors > 0:
        error_messages.append(f"{num_judge_errors}/{num_rows} contain judge errors")

    return error_messages


# Used to display summary and instructions to the user after evaluation is complete.
_AI_ICON_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 16 16" aria-hidden="true" focusable="false" class=""><path fill="currentColor" fill-rule="evenodd" d="M10.726 8.813 13.199 8l-2.473-.813a3 3 0 0 1-1.913-1.913L8 2.801l-.813 2.473a3 3 0 0 1-1.913 1.913L2.801 8l2.473.813a3 3 0 0 1 1.913 1.913L8 13.199l.813-2.473a3 3 0 0 1 1.913-1.913Zm2.941.612c1.376-.452 1.376-2.398 0-2.85l-2.473-.813a1.5 1.5 0 0 1-.956-.956l-.813-2.473c-.452-1.376-2.398-1.376-2.85 0l-.813 2.473a1.5 1.5 0 0 1-.956.956l-2.473.813c-1.376.452-1.376 2.398 0 2.85l2.473.813a1.5 1.5 0 0 1 .956.957l.813 2.472c.452 1.376 2.398 1.376 2.85 0l.813-2.473a1.5 1.5 0 0 1 .957-.956l2.472-.813Z" clip-rule="evenodd"></path></svg>
"""


def _display_summary_and_usage_instructions(run_id: str, results_df: pd.DataFrame):
    """
    Displays summary of the evaluation result, errors and warnings if any,
    and instructions on what to do after running `mlflow.evaluate`.
    """

    summary_text = generate_summary(results_df)

    errors_and_warnings = generate_error_messages(results_df)
    errors_and_warnings.extend(session.current_session().warnings)

    run = mlflow.get_run(run_id)
    if mlflow_tags.MLFLOW_DATABRICKS_WORKSPACE_URL in run.data.tags:
        # Include Databricks URLs in the displayed message.
        workspace_url = run.data.tags[mlflow_tags.MLFLOW_DATABRICKS_WORKSPACE_URL]
        resolver = workspace_url_resolver.WorkspaceUrlResolver(workspace_url)
        compare_evals_url = resolver.resolve_url_for_mlflow_experiment_eval_view(
            run.info
        )
        eval_results_url = resolver.resolve_url_for_mlflow_evaluation_results(run.info)

        links = [
            {"text": "View evaluation results", "url": eval_results_url},
            {"text": "Compare evaluations across runs", "url": compare_evals_url},
        ]

        # Create a Jinja2 environment and load the template
        env = Environment(
            loader=PackageLoader("databricks.rag_eval", "templates"),
            autoescape=select_autoescape(["html"]),
        )
        template = env.get_template("eval_output.html")

        # Render the template with the data
        rendered_html = template.render(
            {
                "summary_text": summary_text,
                "errors_and_warnings": errors_and_warnings,
                "links": links,
            }
        )

        context.get_context().display_html(rendered_html)
    else:
        errors_and_warnings_str = (
            "\n".join([f"* {text}" for text in errors_and_warnings])
            if errors_and_warnings
            else ""
        )
        print(
            f"""Evaluation completed{": " + summary_text if summary_text else "."}
{errors_and_warnings_str}

Metrics and evaluation results can be viewed from the MLflow run page.
To compare evaluation results across runs, view the "Evaluation" tab of the experiment.

Get aggregate metrics: `result.metrics`.
Get per-row evaluation results: `result.tables['eval_results']`.
`result` is the `EvaluationResult` object returned by `mlflow.evaluate`.
"""
        )


def _log_evaluation_input_artifacts(
    config: evaluation_config.EvaluationConfig, examples_df: Optional[pd.DataFrame]
):
    """
    Logs the configuration to MLflow, as well as the examples_df if provided.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir, "eval_config.json")
        config_str = json.dumps(config.to_dict())
        path.write_text(config_str)
        mlflow.log_artifact(str(path))

    if examples_df is not None:
        _log_pandas_df_artifact(examples_df, "eval_examples")


class DatabricksRagEvaluator(mlflow_evaluation.base.ModelEvaluator):
    def can_evaluate(self, *, model_type, evaluator_config, **kwargs) -> bool:
        """
        See parent class docstring.
        """
        return model_type == evaluator_plugin.MODEL_TYPE

    @context.eval_context
    def evaluate(
        self,
        *,
        model_type,
        dataset,
        run_id,
        evaluator_config: Optional[Dict[str, Any]] = None,
        model=None,
        custom_metrics=None,
        extra_metrics=None,
        custom_artifacts=None,
        baseline_model=None,
        predictions=None,
        **kwargs,
    ):
        """
        Runs Databricks RAG evaluation on the provided dataset.

        The following arguments are supported:
        - model_type: Must be the same as evaluator_plugin.MODEL_TYPE
        - dataset
        - run_id

        For more details, see parent class docstring.
        """
        try:
            if evaluator_config is None:
                evaluator_config = {}

            config = evaluation_config.EvaluationConfig.from_mlflow_evaluate_args(
                evaluator_config, extra_metrics
            )

            eval_dataset = mlflow_utils.mlflow_dataset_to_evaluation_dataset(dataset)

            # Set batch size to the context
            session.current_session().set_session_batch_size(
                len(eval_dataset.eval_items)
            )

            eval_results = harness.run(
                model=model, eval_dataset=eval_dataset, config=config
            )

            mlflow_per_run_metrics = per_run_metrics.generate_per_run_metrics(
                eval_results
            )

            # Log results to mlflow
            examples_df: pd.DataFrame = evaluator_config.get(
                constants.EVALUATOR_CONFIG_EXAMPLES_KEY_NAME, None
            )

            _log_evaluation_input_artifacts(config, examples_df)

            mlflow.log_metrics(mlflow_per_run_metrics)

            eval_results_df = pd.DataFrame(
                [result.to_pd_series() for result in eval_results]
            )

            eval_results_artifact = _log_pandas_df_artifact(
                eval_results_df, "eval_results"
            )

            eval_logging.log_eval_results(eval_results)

            _display_summary_and_usage_instructions(run_id, eval_results_df)

            result = mlflow_models.EvaluationResult(
                metrics=mlflow_per_run_metrics,
                artifacts={"eval_results": eval_results_artifact},
            )

            return result
        except error_utils.ValidationError as e:
            # Scrub trace for user-facing validation errors
            raise error_utils.ValidationError(str(e)) from None
