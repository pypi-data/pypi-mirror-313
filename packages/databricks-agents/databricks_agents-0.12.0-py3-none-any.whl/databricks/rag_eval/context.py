"""
Introduces main Context class and the framework to specify different specialized
contexts.
"""

from __future__ import annotations

import functools
import inspect
import logging
import uuid
from abc import ABC, abstractmethod
from typing import Optional

import mlflow
from mlflow.utils import databricks_utils

from databricks.rag_eval import session
from databricks.rag_eval.clients import managedevals, managedrag

_logger = logging.getLogger(__name__)


class Context(ABC):
    """
    Abstract class for execution context.
    Context is stateless and should NOT be used to store information related to specific eval run.
    """

    @abstractmethod
    def display_html(self, html: str) -> None:
        """
        Displays HTML in the current execution context.
        """
        pass

    @abstractmethod
    def build_managed_rag_client(self) -> managedrag.ManagedRagClient:
        """
        Build a LLM Judge client for the current eval session.
        """
        pass

    @abstractmethod
    def build_managed_evals_client(self) -> managedevals.ManagedEvalsClient:
        """
        Build a Managed Evals client for the current eval session.
        """
        pass

    @abstractmethod
    def get_job_id(self) -> Optional[str]:
        """
        Get the current job ID.
        """
        pass

    @abstractmethod
    def get_job_run_id(self) -> Optional[str]:
        """
        Get the current job run ID.
        """
        pass


class NoneContext(Context):
    """
    A context that does nothing.
    """

    def display_html(self, html: str) -> None:
        raise AssertionError("Context is not set")

    def build_managed_rag_client(self) -> managedrag.ManagedRagClient:
        raise AssertionError("Context is not set")

    def build_managed_evals_client(self) -> managedevals.ManagedEvalsClient:
        raise AssertionError("Context is not set")

    def get_job_id(self) -> Optional[str]:
        raise AssertionError("Context is not set")

    def get_job_run_id(self) -> Optional[str]:
        raise AssertionError("Context is not set")


class RealContext(Context):
    """
    Context for eval execution.

    NOTE: This class is not covered by unit tests and is meant to be tested through
    smoke tests that run this code on an actual Databricks cluster.
    """

    @classmethod
    def _get_dbutils(cls):
        """
        Returns an instance of dbutils.
        """
        try:
            from databricks.sdk.runtime import dbutils

            return dbutils
        except ImportError:
            import IPython

            dbutils = IPython.get_ipython().user_ns["dbutils"]
        return dbutils

    def __init__(self):
        self._dbutils = self._get_dbutils()
        try:
            self._notebook_context = (
                self._dbutils.entry_point.getDbutils().notebook().getContext()
            )
        except Exception:
            self._notebook_context = None

        # Set MLflow model registry to Unity Catalog
        mlflow.set_registry_uri("databricks-uc")

    def display_html(self, html) -> None:
        # pylint: disable=protected-access
        self._dbutils.notebook.displayHTML(html)

    def build_managed_rag_client(self) -> managedrag.ManagedRagClient:
        host_creds = databricks_utils.get_databricks_host_creds()
        api_url = host_creds.host
        api_token = host_creds.token
        return managedrag.ManagedRagClient(api_url=api_url, api_token=api_token)

    def build_managed_evals_client(self) -> managedevals.ManagedEvalsClient:
        host_creds = databricks_utils.get_databricks_host_creds()
        api_url = host_creds.host
        api_token = host_creds.token
        return managedevals.ManagedEvalsClient(api_url=api_url, api_token=api_token)

    def get_job_id(self) -> Optional[str]:
        try:
            return self._notebook_context.jobId().get()
        except Exception:
            return None

    def get_job_run_id(self) -> Optional[str]:
        try:
            return self._notebook_context.parentRunId().get()
        except Exception:
            return None


# Context is a singleton.
_context_singleton = NoneContext()


def context_is_active() -> bool:
    """
    Check if a context is active.
    """
    return not isinstance(get_context(), NoneContext)


def get_context() -> Context:
    """
    Get the context.
    """
    return _context_singleton or NoneContext()


def eval_context(func):
    """
    Decorator for wrapping all eval APIs with setup and closure logic.

    Sets up a context singleton with RealContext if there isn't one already.
    Initializes the session for the current thread. Clears the session after the function is executed.

    :param func: eval function to wrap
    :return: return value of func
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Set up the context singleton if it doesn't exist
        if not context_is_active():
            global _context_singleton
            _context_singleton = RealContext()

        if session.current_session() is None:
            # Initialize the session
            session.init_session(str(uuid.uuid4()))
            root_call = True
        else:
            root_call = False

        error = None
        result = None

        parameters = inspect.signature(func).parameters
        # Get all the parameters with default values from the method signature.
        # If a parameter does not have default value, it will not be included in the `full_kwargs`.
        full_kwargs = {
            param_name: parameters[param_name].default
            for param_name in parameters
            if parameters[param_name].default != inspect.Parameter.empty
        }
        # Merge the parameters default values with the values passed in by the user.
        full_kwargs.update(kwargs)

        # Do any preprocessing of the args here

        try:
            result = func(*args, **full_kwargs)
        except Exception as e:  # pylint: disable=broad-except
            error = e
        finally:
            # Clear the session if this is a root call
            if root_call:
                session.clear_session()
            # Raise the original error if there was one, otherwise return
            if error is not None:
                raise error
            else:
                return result  # pylint: disable=lost-exception

    return wrapper
