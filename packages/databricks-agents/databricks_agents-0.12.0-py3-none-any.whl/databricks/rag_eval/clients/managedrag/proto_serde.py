"""
Data Transfer Objects (DTO) based on the GetChatAssessments proto definitions and conversion from dto objects to/from
proto-compatible JSON

This is shamelessly copied/inspired from databricks.data_monitoring.converters.metadata_json
"""

import json
from typing import Any, Collection, Dict, List, Mapping, Optional

from requests import HTTPError

from databricks.rag_eval import schemas
from databricks.rag_eval.config import (
    assessment_config,
    example_config,
)
from databricks.rag_eval.config.assessment_config import (
    AssessmentType,
)
from databricks.rag_eval.evaluation import entities

# Use a dict to represent the proto.
# Serialization can happen trivially through `json.dumps()`, and similarly
# for deserialization with `json.loads()`


class JsonProto(Dict[str, Any]):
    """
    This class wraps around a proto json dictionary and defines helper methods to obtain and set the values of optional
    proto fields:

    - set_optional_field
    - set_repeated_field
    - get_required_field
    - get_required_list

    Serialization code should use these methods instead of getting/setting directly dict fields
    so that we can maintain consistency between Py-friendly structs and JSON-to-proto-serialization semantics.
    """

    def set_required_field(self, field: str, value: Any) -> None:
        """
        Sets a required field to the input value.
        :param field: The name of the field.
        :param value: The value to be set.
        """
        self[field] = value

    def set_optional_field(self, optional_field: str, value: Optional[Any]) -> None:
        """
        Sets an optional field to the input value if the latter is not None. If the field is already set and the new value
        is None, overwrite it to None

        :param optional_field: The name of the optional field.
        :param value: An optional value.
        """

        if value is None and optional_field in self:
            # remove the field if it is set and the value is None
            del self[optional_field]

        if value is None:
            return

        self[optional_field] = value

    def set_repeated_field(self, field: str, value: Optional[Collection]) -> None:
        """
        Sets a repeated field to the input value if the latter is not empty.
        :param field: The name of the field.
        :param value: An optional collection
        """
        if value is not None and len(value) > 0:
            self[field] = value

    @classmethod
    def get_required_field(cls, json_dict: Mapping[str, Any], field: str) -> Any:
        """
        Gets the value of a required field. Throws an error if the field is not set.
        :param field: The name of the field.
        :param json_dict: The json proto that is assumed to hold the field.
        :return: The value of the field.
        """
        if field not in json_dict:
            raise ValueError(
                f"Serialization error: could not find field '{field}' in {json.dumps(json_dict)}"
            )
        return json_dict.get(field)

    @classmethod
    def get_required_list(cls, json_dict: Mapping[str, Any], field: str) -> List:
        """
        Gets the value of a required repeated field. Throws an error if the field is not set.
        :param json_dict: The json proto that is assumed to hold the field.
        :param field: The name of the field.
        :return: The value of the field.
        """
        if field not in json_dict:
            raise ValueError(
                f"Serialization error: could not find field '{field}' in {json.dumps(json_dict)}"
            )
        return list(json_dict.get(field))

    @classmethod
    def get_optional_list(cls, json_dict: Mapping[str, Any], field: str) -> List:
        """
        Similar to get_required_list above but returns an empty list if the field is not set.
        """
        return list() if field not in json_dict else list(json_dict.get(field))

    @classmethod
    def get_optional_field(
        cls, json_dict: Mapping[str, Any], field: str
    ) -> Optional[Any]:
        """
        Gets the value of an optional field.

        :param json_dict: The json proto that is assumed to hold the field.
        :param field: The name of the field.
        :return: The value of the field or None if the field is not set.
        """
        return json_dict.get(field, None)


# TODO: this class keeps no state, considering moving it into module level
class ChatAssessmentProtoSerde:
    """
    Utility class to convert to and from proto JSON for the LLM judge service and the entities used in the RAG
    eval harness.
    """

    def construct_chat_assessment_usage_event_json(
        self, custom_assessment: assessment_config.EvaluationMetricAssessmentConfig
    ) -> JsonProto:
        custom_assessment_usage_event = JsonProto()
        custom_assessment_usage_event.set_required_field(
            "assessment_name", custom_assessment.assessment_name
        )
        custom_assessment_usage_event.set_required_field(
            "assessment_type",
            _assessment_type_to_proto_assessment_type(
                custom_assessment.assessment_type
            ),
        )
        return custom_assessment_usage_event

    def construct_chat_assessment_usage_event_request_json(
        self,
        custom_assessments: List[assessment_config.EvaluationMetricAssessmentConfig],
        num_questions: Optional[int],
    ) -> JsonProto:
        result = JsonProto()
        result.set_repeated_field(
            "usage_events",
            [
                self.construct_chat_assessment_usage_event_json(custom_assessment)
                for custom_assessment in custom_assessments
            ],
        )
        result.set_optional_field("num_questions", num_questions)
        return result

    def construct_assessment_request_json(
        self,
        eval_item: entities.EvalItem,
        assessment_name: str,
        examples: List[example_config.AssessmentExample],
        domain_instructions: Optional[str],
    ) -> JsonProto:
        result = JsonProto()
        result.set_required_field(
            "assessment_input", self.construct_assessment_input_json(eval_item)
        )
        result.set_repeated_field(
            "requested_assessments",
            [
                self.construct_assessment_definition(
                    assessment_name, examples, domain_instructions
                )
            ],
        )
        return result

    def construct_assessment_input_json(
        self, eval_item: entities.EvalItem
    ) -> JsonProto:
        result = JsonProto()
        result.set_required_field("chat_request", eval_item.question)
        result.set_optional_field("chat_response", eval_item.answer)
        result.set_optional_field(
            "retrieval_context",
            (
                self.construct_retrieval_ctx_json(eval_item.retrieval_context)
                if eval_item.retrieval_context
                else None
            ),
        )
        result.set_optional_field(
            "ground_truth",
            (
                self.construct_ground_truth_json(
                    eval_item.ground_truth_answer,
                    eval_item.ground_truth_retrieval_context,
                    eval_item.expected_facts,
                )
                if eval_item.ground_truth_answer
                or eval_item.ground_truth_retrieval_context
                or eval_item.expected_facts
                else None
            ),
        )
        result.set_optional_field("grading_notes", eval_item.grading_notes)

        return result

    def construct_example_assessment_input_json(
        self, example: example_config.AssessmentExample
    ) -> JsonProto:
        result = JsonProto()
        result.set_required_field(
            "chat_request",
            example.variables[schemas.REQUEST_COL],
        )
        result.set_optional_field(
            "chat_response",
            example.variables.get(schemas.RESPONSE_COL, None),
        )
        result.set_optional_field(
            "retrieval_context",
            self.construct_example_retrieval_ctx_json(
                example.variables.get(schemas.RETRIEVED_CONTEXT_COL)
            ),
        )
        result.set_optional_field(
            "ground_truth",
            self.construct_example_ground_truth_json(example),
        )
        return result

    def construct_example_retrieval_ctx_json(
        self, context_str: str
    ) -> Optional[JsonProto]:
        if context_str is None:
            return None

        result = JsonProto()
        chunks = entities.Chunk(doc_uri=None, content=context_str)
        result.set_repeated_field(
            "retrieved_documents", [self.construct_chunk_json(chunks)]
        )
        return result

    def construct_example_ground_truth_json(
        self, example: example_config.AssessmentExample
    ) -> Optional[JsonProto]:
        result = JsonProto()
        result.set_optional_field(
            "expected_chat_response",
            example.variables.get(schemas.EXPECTED_RESPONSE_COL, None),
        )
        # TODO do we support expected_context? it's not part of the user documentation as of 05/01/2024
        # result.set_optional_field(
        #     "expected_retrieval_context",
        #     self.construct_example_retrieval_ctx_json(
        #         example.variables.get("expected_context", None)
        #     ),
        # )
        # ground truth has all optional fields so return None if all fields are None
        return result if any(result.values()) else None

    def construct_assessment_definition(
        self,
        assessment_name: str,
        examples: List[example_config.AssessmentExample],
        domain_instructions: Optional[str],
    ) -> JsonProto:
        result = JsonProto()
        result.set_required_field("assessment_name", assessment_name)
        result.set_repeated_field(
            "assessment_examples",
            [self.construct_example_json(example) for example in examples],
        )
        result.set_optional_field("domain_instructions", domain_instructions)
        return result

    def construct_example_json(
        self, example: example_config.AssessmentExample
    ) -> JsonProto:
        result = JsonProto()
        result.set_required_field(
            "example_assessment_input",
            self.construct_example_assessment_input_json(example),
        )
        result.set_required_field(
            "expected_rating", self.construct_example_rating_json(example)
        )
        return result

    def construct_example_rating_json(
        self, example: example_config.AssessmentExample
    ) -> JsonProto:
        result = JsonProto()
        result.set_optional_field(
            "categorical_value",
            entities.CategoricalRating.from_example_rating(example.rating),
        )
        result.set_optional_field("justification", example.rationale)
        return result

    def construct_retrieval_ctx_json(
        self, retrieval_ctx: entities.RetrievalContext
    ) -> JsonProto:
        result = JsonProto()
        result.set_repeated_field(
            "retrieved_documents",
            [
                self.construct_chunk_json(chunk)
                for chunk in retrieval_ctx
                if chunk is not None
            ],
        )
        return result

    def construct_ground_truth_json(
        self,
        ground_truth_answer: Optional[str],
        ground_truth_retrieval_context: Optional[entities.RetrievalContext],
        expected_facts: Optional[List[str]],
    ) -> JsonProto:
        result = JsonProto()
        result.set_optional_field("expected_chat_response", ground_truth_answer)
        result.set_optional_field(
            "expected_retrieval_context",
            (
                self.construct_retrieval_ctx_json(ground_truth_retrieval_context)
                if ground_truth_retrieval_context
                else None
            ),
        )
        result.set_optional_field("expected_facts", expected_facts)
        return result

    def construct_chunk_json(self, chunk: entities.Chunk) -> JsonProto:
        result = JsonProto()
        result.set_optional_field("doc_uri", chunk.doc_uri)
        result.set_optional_field("content", chunk.content)
        return result

    def construct_assessment_result(
        self,
        response_json: JsonProto,
        assessment_name: str,
        assessment_type: assessment_config.AssessmentType,
    ) -> List[entities.AssessmentResult]:
        chat_assessment_json = JsonProto.get_required_field(response_json, "result")
        response_assessment_json = JsonProto.get_required_field(
            chat_assessment_json, "response_assessment"
        )
        retrieval_assessment_json = JsonProto.get_optional_field(
            chat_assessment_json, "retrieval_assessment"
        )

        response_assessment_ratings: dict[str, entities.Rating] = (
            self.json_to_rating_map(response_assessment_json)
        )

        retrieval_assessment_ratings: dict[str, entities.PositionalRating] = (
            self.json_to_positional_rating_map(retrieval_assessment_json)
        )

        # Convert the service metric name to the corresponding user-facing metric name
        eval_assessment_name = assessment_config.translate_to_eval_assessment_name(
            assessment_name
        )
        if assessment_name in response_assessment_ratings.keys():
            eval_rating = response_assessment_ratings.get(assessment_name)
            # TODO[ML-42124]: Remove the flip logic once the harmfulness judge in the service is updated
            # Flip the binary rating from the service if needed
            eval_rating = (
                entities.Rating.flip(eval_rating)
                if assessment_config.needs_flip(assessment_name)
                else eval_rating
            )

            return [
                entities.PerRequestAssessmentResult(
                    assessment_name=eval_assessment_name,
                    assessment_type=assessment_type,
                    assessment_source=entities.AssessmentSource.builtin(),
                    rating=eval_rating,
                )
            ]
        elif assessment_name in retrieval_assessment_ratings.keys():
            return [
                entities.PerChunkAssessmentResult(
                    assessment_name=eval_assessment_name,
                    assessment_source=entities.AssessmentSource.builtin(),
                    positional_rating=retrieval_assessment_ratings.get(assessment_name),
                )
            ]
        else:
            return []

    def construct_assessment_error_result(
        self,
        assessment_name: str,
        assessment_type: AssessmentType,
        error_code: int,
        e: HTTPError,
    ) -> List[entities.AssessmentResult]:
        error_msg = f"Llm judge error [{error_code}]: {str(e)}"
        error_rating = entities.Rating.error(
            error_message=error_msg, error_code=str(error_code)
        )
        # Convert the service metric name to the corresponding user-facing metric name
        eval_assessment_name = assessment_config.translate_to_eval_assessment_name(
            assessment_name
        )

        # if an error occurs, gracefully return a RatingError based on the type
        match assessment_type:
            case AssessmentType.ANSWER:
                return [
                    entities.PerRequestAssessmentResult(
                        assessment_name=eval_assessment_name,
                        assessment_type=assessment_type,
                        assessment_source=entities.AssessmentSource.builtin(),
                        rating=error_rating,
                    )
                ]
            case AssessmentType.RETRIEVAL_LIST:
                return [
                    entities.PerRequestAssessmentResult(
                        assessment_name=eval_assessment_name,
                        assessment_type=assessment_type,
                        assessment_source=entities.AssessmentSource.builtin(),
                        rating=error_rating,
                    )
                ]
            case AssessmentType.RETRIEVAL:
                return [
                    entities.PerChunkAssessmentResult(
                        assessment_name=eval_assessment_name,
                        assessment_source=entities.AssessmentSource.builtin(),
                        positional_rating={0: error_rating},
                    )
                ]

    def construct_assessment_metric_definition_request_json(
        self,
        assessment_names: List[str],
    ) -> JsonProto:
        result = JsonProto()
        result.set_required_field("assessment_names", list(assessment_names))
        return result

    def construct_assessment_input_requirement_expressions(
        self, response_json: JsonProto
    ) -> Dict[str, assessment_config.AssessmentInputRequirementExpression]:
        """
        Converts a JSON proto to a mapping from assessment name to AssessmentInputRequirementExpression.
        """
        return {
            JsonProto.get_required_field(
                definition, "assessment_name"
            ): self._construct_assessment_input_requirement_expression(definition)
            for definition in JsonProto.get_required_list(response_json, "definitions")
        }

    def _construct_assessment_input_requirement_expression(
        self, response_json: JsonProto
    ) -> assessment_config.AssessmentInputRequirementExpression:
        """
        Converts a JSON proto to an AssessmentInputRequirementExpression.
        """
        input_requirement_expression = JsonProto.get_required_field(
            response_json, "input_requirement_expression"
        )
        required = JsonProto.get_optional_field(
            input_requirement_expression, "required"
        )
        at_least_one_of = JsonProto.get_optional_list(
            input_requirement_expression, "at_least_one_of"
        )
        at_most_one_of = JsonProto.get_optional_list(
            input_requirement_expression, "at_most_one_of"
        )

        return assessment_config.AssessmentInputRequirementExpression(
            required=required if required is not None else [],
            at_least_one_of=at_least_one_of if at_least_one_of is not None else [],
            at_most_one_of=at_most_one_of if at_most_one_of is not None else [],
        )

    def json_to_rating_map(self, proto: JsonProto) -> Dict[str, entities.Rating]:
        """
        Converts a JSON proto to a ResponseAssessment.
        """
        ratings = JsonProto.get_optional_field(proto, "ratings")

        return (
            {key: self.json_to_rating(value) for key, value in ratings.items()}
            if ratings
            else {}
        )

    def json_to_positional_rating_map(
        self, proto: JsonProto
    ) -> Dict[str, entities.PositionalRating]:
        """
        Converts a JSON proto to a ResponseAssessment.
        """

        result = {}
        positional_rating_map = JsonProto.get_optional_field(
            proto, "positional_ratings"
        )
        if positional_rating_map:
            for key, value in positional_rating_map.items():
                positional_rating_list = JsonProto.get_optional_list(value, "rating")
                positional_ratings = {
                    JsonProto.get_required_field(
                        rating, "position"
                    ): self.json_to_rating(
                        JsonProto.get_required_field(rating, "rating")
                    )
                    for rating in positional_rating_list
                }
                result[key] = positional_ratings

        return result

    def json_to_rating(self, proto: JsonProto) -> entities.Rating:
        """
        Converts a JSON proto to a Rating.
        """
        maybe_value = JsonProto.get_optional_field(proto, "value")
        maybe_error = JsonProto.get_optional_field(proto, "error")

        # the proto is an oneof so only one of them should be present
        if maybe_value is not None:
            return entities.Rating.value(
                double_value=JsonProto.get_optional_field(maybe_value, "double_value"),
                rationale=JsonProto.get_optional_field(maybe_value, "justification"),
                categorical_value=JsonProto.get_optional_field(
                    maybe_value, "categorical_value"
                ),
            )
        elif maybe_error is not None:
            return entities.Rating.error(
                error_message=JsonProto.get_optional_field(maybe_error, "error_msg"),
                error_code=JsonProto.get_optional_field(maybe_error, "error_code"),
            )
        else:
            # This should never happen but just in case
            return entities.Rating.error(
                error_message="Rating returned from LLM judge contains no value nor error.",
            )

    def construct_client_error_usage_event_request_json(
        self, error_message: str
    ) -> JsonProto:
        agent_invocation_error = JsonProto()
        agent_invocation_error.set_required_field("error_message", error_message)
        evaluation_client_usage_event = JsonProto()
        evaluation_client_usage_event.set_required_field(
            "agent_invocation_error", agent_invocation_error
        )
        usage_events = [evaluation_client_usage_event]

        result = JsonProto()
        result.set_required_field("agent_evaluation_client_usage_events", usage_events)
        return result


def _assessment_type_to_proto_assessment_type(
    assessment_type: assessment_config.AssessmentType,
) -> str:
    """
    Convert to enum expected by service proto.
    """
    if assessment_type == assessment_type.ANSWER:
        return "RESPONSE"
    return str(assessment_type)
