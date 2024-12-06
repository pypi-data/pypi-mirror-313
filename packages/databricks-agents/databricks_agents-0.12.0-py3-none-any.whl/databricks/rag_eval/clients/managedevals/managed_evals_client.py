import warnings
from typing import Collection, Dict, Iterable, List, Optional, TypedDict

import requests
from urllib3.util import retry

from databricks import version
from databricks.agents.utils.mlflow_utils import get_workspace_url
from databricks.rag_eval import entities, env_vars, schemas, session
from databricks.rag_eval.clients import databricks_api_client
from databricks.rag_eval.monitoring import rest_entities
from databricks.rag_eval.utils import NO_CHANGE, input_output_utils

SESSION_ID_HEADER = "managed-evals-session-id"
CLIENT_VERSION_HEADER = "managed-evals-client-version"
SYNTHETIC_GENERATION_NUM_DOCS_HEADER = "managed-evals-synthetic-generation-num-docs"
SYNTHETIC_GENERATION_NUM_EVALS_HEADER = "managed-evals-synthetic-generation-num-evals"
USE_NOTEBOOK_CLUSTER_ID = False

TagType = TypedDict("TagType", {"tag_name": str, "tag_id": str})


def get_default_retry_config():
    return retry.Retry(
        total=env_vars.AGENT_EVAL_GENERATE_EVALS_MAX_RETRIES.get(),
        backoff_factor=env_vars.AGENT_EVAL_GENERATE_EVALS_BACKOFF_FACTOR.get(),
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_jitter=env_vars.AGENT_EVAL_GENERATE_EVALS_BACKOFF_JITTER.get(),
        allowed_methods=frozenset(
            ["GET", "POST"]
        ),  # by default, it doesn't retry on POST
    )


def _raise_for_status(resp: requests.Response) -> None:
    """
    Raise an Exception if the response is an error.
    Custom error message is extracted from the response JSON.
    """
    if resp.status_code == requests.codes.ok:
        return
    http_error_msg = ""
    if 400 <= resp.status_code < 500:
        http_error_msg = (
            f"{resp.status_code} Client Error: {resp.reason}\n{resp.text}. "
        )
    elif 500 <= resp.status_code < 600:
        http_error_msg = (
            f"{resp.status_code} Server Error: {resp.reason}\n{resp.text}. "
        )
    raise requests.HTTPError(http_error_msg, response=resp)


def _get_default_headers() -> Dict[str, str]:
    """
    Constructs the default request headers.
    """
    return {
        CLIENT_VERSION_HEADER: version.VERSION,
    }


def _get_synthesis_headers() -> Dict[str, str]:
    """
    Constructs the request headers for synthetic generation.
    """
    eval_session = session.current_session()
    if eval_session is None:
        return {}
    return {
        CLIENT_VERSION_HEADER: version.VERSION,
        SESSION_ID_HEADER: eval_session.session_id,
        SYNTHETIC_GENERATION_NUM_DOCS_HEADER: str(
            eval_session.synthetic_generation_num_docs
        ),
        SYNTHETIC_GENERATION_NUM_EVALS_HEADER: str(
            eval_session.synthetic_generation_num_evals
        ),
    }


class ManagedEvalsClient(databricks_api_client.DatabricksAPIClient):
    """
    Client to interact with the managed-evals service.
    """

    def __init__(
        self,
        api_url: str,
        api_token: str,
    ):
        super().__init__(
            api_url=api_url,
            api_token=api_token,
            version="2.0",
        )

    # override from DatabricksAPIClient
    def get_default_request_session(self, *args, **kwargs):
        session = super().get_default_request_session(*args, **kwargs)
        if USE_NOTEBOOK_CLUSTER_ID:
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.getOrCreate()
            cluster_id = spark.conf.get("spark.databricks.clusterUsageTags.clusterId")
            session.params = {"compute_cluster_id": cluster_id}
        return session

    def generate_questions(
        self,
        *,
        doc: entities.Document,
        num_questions: int,
        agent_description: Optional[str],
        question_guidelines: Optional[str],
    ) -> List[entities.SyntheticQuestion]:
        """
        Generate synthetic questions for the given document.
        """
        request_json = {
            "doc_content": doc.content,
            "num_questions": num_questions,
            "agent_description": agent_description,
            "question_guidelines": question_guidelines,
        }
        with self.get_default_request_session(
            get_default_retry_config(),
            _get_synthesis_headers(),
        ) as session:
            resp = session.post(
                url=self.get_method_url("/managed-evals/generate-questions"),
                json=request_json,
            )

        _raise_for_status(resp)

        response_json = resp.json()
        if "questions_with_context" not in response_json or "error" in response_json:
            raise ValueError(f"Invalid response: {response_json}")
        return [
            entities.SyntheticQuestion(
                question=question_with_context["question"],
                source_doc_uri=doc.doc_uri,
                source_context=question_with_context["context"],
            )
            for question_with_context in response_json["questions_with_context"]
        ]

    def generate_answer(
        self,
        *,
        question: entities.SyntheticQuestion,
        answer_types: Collection[entities.SyntheticAnswerType],
    ) -> entities.SyntheticAnswer:
        """
        Generate synthetic answer for the given question.
        """
        request_json = {
            "question": question.question,
            "context": question.source_context,
            "answer_types": [str(answer_type) for answer_type in answer_types],
        }

        with self.get_default_request_session(
            get_default_retry_config(),
            _get_synthesis_headers(),
        ) as session:
            resp = session.post(
                url=self.get_method_url("/managed-evals/generate-answer"),
                json=request_json,
            )

        _raise_for_status(resp)

        response_json = resp.json()
        return entities.SyntheticAnswer(
            question=question,
            synthetic_ground_truth=response_json.get("synthetic_ground_truth"),
            synthetic_grading_notes=response_json.get("synthetic_grading_notes"),
            synthetic_minimal_facts=response_json.get("synthetic_minimal_facts"),
        )

    def create_managed_evals_instance(
        self,
        *,
        instance_id: str,
        agent_name: Optional[str] = None,
        agent_serving_endpoint: Optional[str] = None,
        experiment_ids: Optional[Iterable[str]] = None,
    ) -> entities.EvalsInstance:
        """
        Creates a new Managed Evals instance.

        Args:
            instance_id: Managed Evals instance ID.
            agent_name: (optional) The name of the agent.
            agent_serving_endpoint: (optional) The name of the model serving endpoint that serves the agent.
            experiment_ids: (optional) The experiment IDs to associate with the instance.

        Returns:
            The created EvalsInstance.
        """
        evals_instance = entities.EvalsInstance(
            agent_name=agent_name,
            agent_serving_endpoint=agent_serving_endpoint,
            experiment_ids=experiment_ids if experiment_ids is not None else [],
        )
        request_body = {"instance": evals_instance.to_json()}
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.post(
                url=self.get_method_url(f"/managed-evals/instances/{instance_id}"),
                json=request_body,
            )
        _raise_for_status(response)
        return entities.EvalsInstance.from_json(response.json())

    def delete_managed_evals_instance(self, instance_id: str) -> None:
        """
        Deletes a Managed Evals instance.

        Args:
            instance_id: Managed Evals instance ID.
        """
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.delete(
                url=self.get_method_url(f"/managed-evals/instances/{instance_id}"),
            )
        _raise_for_status(response)

    def update_managed_evals_instance(
        self,
        *,
        instance_id: str,
        agent_name: Optional[str] = NO_CHANGE,
        agent_serving_endpoint: Optional[str] = NO_CHANGE,
        experiment_ids: List[str] = NO_CHANGE,
    ) -> entities.EvalsInstance:
        """
        Updates a Managed Evals instance.

        Args:
            instance_id: Managed Evals instance ID.
            agent_name: (optional) The name of the agent.
            agent_serving_endpoint: (optional) The name of the model serving endpoint that serves the agent.
            experiment_ids: (optional) The experiment IDs to associate with the instance.

        Returns:
            The updated EvalsInstance.
        """
        evals_instance = entities.EvalsInstance(
            agent_name=agent_name,
            agent_serving_endpoint=agent_serving_endpoint,
            experiment_ids=experiment_ids,
        )
        request_body = {
            "instance": evals_instance.to_json(),
            "update_mask": evals_instance.get_update_mask(),
        }

        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.patch(
                url=self.get_method_url(f"/managed-evals/instances/{instance_id}"),
                json=request_body,
            )
        _raise_for_status(response)
        return entities.EvalsInstance.from_json(response.json())

    def get_managed_evals_instance(self, instance_id: str) -> entities.EvalsInstance:
        """
        Gets a Managed Evals instance.

        Args:
            instance_id: Managed Evals instance ID.

        Returns:
            The EvalsInstance.
        """
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.get(
                url=self.get_method_url(
                    f"/managed-evals/instances/{instance_id}/configuration"
                ),
            )
        _raise_for_status(response)
        return entities.EvalsInstance.from_json(response.json())

    def add_evals(
        self,
        *,
        instance_id: str,
        evals: List[Dict],
    ) -> List[str]:
        """
        Add evals to the evals table.

        Args:
            instance_id: The name of the evals table.
            evals: The evals to add to the evals table.

        Returns:
            The eval IDs of the created evals.
        """
        request_body = {
            "evals": [
                {
                    "request_id": e.get(schemas.REQUEST_ID_COL),
                    "source_type": e.get(schemas.SOURCE_TYPE_COL),
                    "source_id": e.get(schemas.SOURCE_ID_COL),
                    "agent_request": input_output_utils.to_chat_completion_request(
                        e.get(schemas.REQUEST_COL)
                    ),
                    "expected_response": e.get(schemas.EXPECTED_RESPONSE_COL),
                    "expected_facts": [
                        {"fact": fact} for fact in e.get(schemas.EXPECTED_FACTS_COL, [])
                    ],
                    "expected_retrieved_context": e.get(
                        schemas.EXPECTED_RETRIEVED_CONTEXT_COL
                    ),
                    "tag_ids": e.get("tag_ids", []),
                    "review_status": e.get("review_status"),
                }
                for e in evals
            ]
        }
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.post(
                url=self.get_method_url(
                    f"/managed-evals/instances/{instance_id}/evals:batchCreate"
                ),
                json=request_body,
            )
        _raise_for_status(response)
        return response.json().get("eval_ids", [])

    def delete_evals(
        self,
        instance_id: str,
        *,
        eval_ids: List[str],
    ):
        """
        Delete evals from the evals table.
        """
        # Delete in a loop - this is inefficient but we don't have a batch delete endpoint yet.
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            for eval in eval_ids:
                response = session.delete(
                    url=self.get_method_url(
                        f"/managed-evals/instances/{instance_id}/evals/{eval}"
                    ),
                )
                _raise_for_status(response)

    def list_tags(
        self,
        instance_id: str,
    ) -> List[TagType]:
        """
        List all tags in the evals table.

        Args:
            instance_id: The name of the evals table.

        Returns:
            A list of tags.
        """
        tags = []
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            next_page_token = None
            for _ in range(100):
                response = session.get(
                    url=self.get_method_url(
                        f"/managed-evals/instances/{instance_id}/tags"
                        + (
                            ("?next_page_token=" + next_page_token)
                            if next_page_token
                            else ""
                        )
                    )
                )
                _raise_for_status(response)
                json_response = response.json()
                tags.extend(json_response.get("tags", []))
                if not (next_page_token := json_response.get("next_page_token")):
                    break
            else:
                warnings.warn(
                    "Giving up fetching tags after 100 pages of tags; potential internal error."
                )
        return tags

    def batch_create_tags(
        self,
        *,
        instance_id: str,
        tag_names: Collection[str],
    ) -> List[str]:
        """
        Call the batchCreate endpoint to create tags.

        Args:
            instance_id: The name of the evals table.
            tag_names: The tag names to create.

        Returns:
            The tag IDs of the created tags.
        """
        request_body = {
            "tags": [{"tag_name": tag_name} for tag_name in tag_names],
        }
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.post(
                url=self.get_method_url(
                    f"/managed-evals/instances/{instance_id}/tags:batchCreate"
                ),
                json=request_body,
            )
        _raise_for_status(response)
        return response.json().get("tag_ids", [])

    def batch_create_eval_tags(
        self,
        instance_id: str,
        *,
        eval_tags: List[entities.EvalTag],
    ):
        """
        Batch tag evals.

        Args:
            instance_id: The name of the evals table.
            eval_tags: A list of eval-tags; each item of the list is one tag on an eval.
        """
        request_body = {
            "eval_tags": [et.to_json() for et in eval_tags],
        }
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.post(
                url=self.get_method_url(
                    f"/managed-evals/instances/{instance_id}/eval_tags:batchCreate"
                ),
                json=request_body,
            )
        _raise_for_status(response)

    def batch_delete_eval_tags(
        self,
        instance_id: str,
        *,
        eval_tags: List[entities.EvalTag],
    ):
        """
        Batch untag evals.

        Args:
            instance_id: The name of the evals table.
            eval_tags: A list of eval-tags; each item of the list is one tag on an eval.
        """
        request_body = {
            "eval_tags": [et.to_json() for et in eval_tags],
        }
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.post(
                url=self.get_method_url(
                    f"/managed-evals/instances/{instance_id}/eval_tags:batchDelete"
                ),
                json=request_body,
            )
        _raise_for_status(response)

    def update_eval_permissions(
        self,
        instance_id: str,
        *,
        add_emails: Optional[List[str]] = None,
        remove_emails: Optional[List[str]] = None,
    ):
        """Add or remove user permissions to edit an eval instance.

        Args:
            instance_id: The name of the evals table.
            add_emails: The emails to add to the permissions list.
            remove_emails: The emails to remove from the permissions list.
        """
        request_body = {"permission_change": {}}
        if add_emails:
            request_body["permission_change"]["add"] = [
                {
                    "user_email": email,
                    "permissions": ["WRITE"],
                }
                for email in add_emails
            ]
        if remove_emails:
            request_body["permission_change"]["remove"] = [
                {
                    "user_email": email,
                    "permissions": ["WRITE"],
                }
                for email in remove_emails
            ]

        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.post(
                url=self.get_method_url(
                    f"/managed-evals/instances/{instance_id}/permissions"
                ),
                json=request_body,
            )
        _raise_for_status(response)

    def create_monitor(
        self,
        *,
        endpoint_name: str,
        monitoring_config: entities.MonitoringConfig,
        experiment_id: str,
        workspace_path: str,
    ) -> entities.Monitor:
        pause_status: Optional[str] = None
        if monitoring_config.paused is not None:
            pause_status = (
                entities.SchedulePauseStatus.PAUSED
                if monitoring_config.paused
                else entities.SchedulePauseStatus.UNPAUSED
            ).value

        monitor_rest = rest_entities.Monitor(
            experiment_id=experiment_id,
            workspace_path=workspace_path,
            evaluation_config=rest_entities.EvaluationConfig(
                metrics=[
                    rest_entities.AssessmentConfig(name=metric)
                    for metric in monitoring_config.metrics or []
                ]
            ),
            sampling=rest_entities.SamplingConfig(
                sampling_rate=monitoring_config.sample
            ),
            schedule=rest_entities.ScheduleConfig(
                frequency_interval=monitoring_config.periodic.interval,
                frequency_unit=monitoring_config.periodic.unit,
                pause_status=pause_status,
            ),
        )
        request_body = {"monitor_config": monitor_rest.to_dict()}

        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.post(
                url=self.get_method_url(f"/managed-evals/monitors/{endpoint_name}"),
                json=request_body,
            )
        _raise_for_status(response)
        monitor_info_rest = rest_entities.MonitorInfo.from_dict(response.json())
        monitor = monitor_info_rest.to_monitor(endpoint_name)

        monitoring_page_url = f"{get_workspace_url()}/ml/experiments/{experiment_id}/evaluation-monitoring"
        user_message = f"""Created monitor for endpoint "{endpoint_name}".

View monitoring page: {monitoring_page_url}"""
        print(user_message)

        return monitor

    def update_monitor(
        self,
        *,
        endpoint_name: str,
        monitoring_config: entities.MonitoringConfig,
    ) -> entities.Monitor:
        pause_status: Optional[str] = None
        if monitoring_config.paused is not None:
            pause_status = (
                entities.SchedulePauseStatus.PAUSED
                if monitoring_config.paused
                else entities.SchedulePauseStatus.UNPAUSED
            )

        evaluation_config: Optional[rest_entities.EvaluationConfig] = None
        if monitoring_config.metrics:
            evaluation_config = rest_entities.EvaluationConfig(
                metrics=[
                    rest_entities.AssessmentConfig(name=metric)
                    for metric in monitoring_config.metrics
                ]
            )

        sampling_config: Optional[rest_entities.SamplingConfig] = None
        if monitoring_config.sample:
            sampling_config = rest_entities.SamplingConfig(
                sampling_rate=monitoring_config.sample
            )

        schedule_config: Optional[rest_entities.ScheduleConfig] = None
        if monitoring_config.periodic:
            schedule_config = rest_entities.ScheduleConfig(
                frequency_interval=monitoring_config.periodic.interval,
                frequency_unit=monitoring_config.periodic.unit,
                pause_status=pause_status,
            )
        monitor_rest = rest_entities.Monitor(
            evaluation_config=evaluation_config,
            sampling=sampling_config,
            schedule=schedule_config,
        )

        request_body = {
            "monitor": monitor_rest.to_dict(),
            "update_mask": monitor_rest.get_update_mask(),
        }
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.patch(
                url=self.get_method_url(f"/managed-evals/monitors/{endpoint_name}"),
                json=request_body,
            )
        _raise_for_status(response)
        monitor_info_rest = rest_entities.MonitorInfo.from_dict(response.json())
        return monitor_info_rest.to_monitor(endpoint_name)

    def get_monitor(
        self,
        *,
        endpoint_name: str,
    ) -> entities.Monitor:
        request_body = {}
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.get(
                url=self.get_method_url(f"/managed-evals/monitors/{endpoint_name}"),
                json=request_body,
            )
        _raise_for_status(response)
        monitor_info_rest = rest_entities.MonitorInfo.from_dict(response.json())
        return monitor_info_rest.to_monitor(endpoint_name)

    def delete_monitor(self, endpoint_name: str) -> None:
        request_body = {}
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.delete(
                url=self.get_method_url(f"/managed-evals/monitors/{endpoint_name}"),
                json=request_body,
            )
        _raise_for_status(response)
