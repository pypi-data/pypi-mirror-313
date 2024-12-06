import logging

from databricks.rag_eval.callable_builtin_judges import (
    chunk_relevance,
    context_sufficiency,
    correctness,
    groundedness,
    relevance_to_query,
    safety,
)

logging.warning(
    "DeprecationWarning: `databricks.agents.eval.judges` package is deprecated. "
    "Use `databricks.agents.evals.judges` instead."
)

__all__ = [
    # Callable judges
    "chunk_relevance",
    "context_sufficiency",
    "correctness",
    "groundedness",
    "relevance_to_query",
    "safety",
]
