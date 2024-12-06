"""Databricks Agent Evaluation Python SDK.

WARNING: `databricks.agents.eval` package is deprecated. Use `databricks.agents.evals` instead.

For more details see `Databricks Agent Evaluation <https://docs.databricks.com/en/generative-ai/agent-evaluation/index.html>`_."""

import logging

from databricks.rag_eval.datasets.synthetic_evals_generation import generate_evals_df

logging.warning(
    "DeprecationWarning: `databricks.agents.eval` package is deprecated. "
    "Use `databricks.agents.evals` instead."
)

__all__ = ["generate_evals_df"]
