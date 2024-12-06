"""
Base class for concrete clients to various Databricks APIs
"""

import abc
from typing import Dict, Optional

import jinja2
import requests
from requests import adapters, auth
from urllib3.util import retry


class DatabricksAPIClient(abc.ABC):
    """
    This is a base client to talk to Databricks API. The child classes of this base client can use the `get_auth()`
    and `get_request_session()` methods provided by `DatabricksAPIClient` to send request to the
    corresponding Databricks API.

    Example Usage:

    class MyClient(DatabricksAPIClient):
      def __init__(self, api_url: str, api_token: str):
        super().__init__(api_url=api_url, api_token=api_token, version="2.1")

      def send_request(self):
        with self.get_request_session() as s:
            resp = s.post(self.get_method_url("list"), json="request_body: {...}", auth=self.get_auth())
        self.process_response(resp)
    """

    def __init__(self, version: str, api_url: str, api_token: str):
        """
        :param api_url: The url that can be used to talk to the workspace,
                        e.g. "https://oregon.staging.cloud.databricks.com".
        :param api_token: Required auth token.
        :param version: The version of the Databricks API, e.g. "2.1", "2.0".
        """
        self._api_url = api_url
        self._api_token = api_token
        self._version = version
        self._base_api_url = f"api/{version}"

    def get_parameterized_method_path(
        self,
        method_template: str,
        method_path_params: Dict[str, str],
        endpoint: str,
        is_preview: bool = False,
    ):
        """
        Returns the path to invoke a specific method

        :param method_template: Jinja template of the method path
        :param method_path_params: Parameters for rendering the method path jinja template
        :param endpoint: Endpoint to construct base url, e.g. "workspace", "jobs".
        :param is_preview: Whether to use the preview path identifier
        """
        method_path = (
            jinja2.Template(method_template).render(method_path_params).lstrip("/")
        )
        return f"{'preview/' if is_preview else ''}{endpoint}/{method_path}"

    def get_method_url(self, method_path: str):
        """
        Returns the URL to invoke a specific method. This is a concatenation of the workspace url + the
        corresponding method path.

        :param method_path: The method path
        """
        return f"{self._api_url}/{self._base_api_url}/{method_path.lstrip('/')}"

    def get_auth(self):
        """
        Get a BearerAuth for requests
        """
        return self.BearerAuth(self._api_token)

    @classmethod
    def get_request_session(
        cls, max_retries: retry.Retry | int | None = adapters.DEFAULT_RETRIES
    ) -> requests.Session:
        """
        Creates a request session with a retry mechanism.

        :return: Session object.
        """
        adapter = adapters.HTTPAdapter(max_retries=max_retries)
        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        return session

    def get_default_request_session(
        self,
        retry_config: Optional[retry.Retry] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Session:
        """
        Creates a request session with a retry mechanism, headers, and default authentication
        :return: Session object.
        """
        session = self.get_request_session(retry_config)
        session.headers.update(headers)
        session.auth = self.get_auth()
        return session

    class BearerAuth(auth.AuthBase):
        """Bearer Authentication class which holds tokens for talking with Databricks API."""

        def __init__(self, token: str):
            self._token = token

        def __call__(self, r):
            r.headers["authorization"] = f"Bearer {self._token}"
            return r
