"""Databricks Agent Evaluation Python SDK.

For more details see `Databricks Agent Evaluation <https://docs.databricks.com/en/generative-ai/agent-evaluation/index.html>`_."""

from databricks.rag_eval.datasets.synthetic_evals_generation import (
    estimate_synthetic_num_evals,
    generate_evals_df,
)

__all__ = ["generate_evals_df", "estimate_synthetic_num_evals"]
