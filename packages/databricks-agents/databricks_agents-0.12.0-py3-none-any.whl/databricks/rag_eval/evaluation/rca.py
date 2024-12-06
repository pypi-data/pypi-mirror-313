from typing import Collection, Optional

from databricks.rag_eval import env_vars
from databricks.rag_eval.config import assessment_config
from databricks.rag_eval.evaluation import entities
from databricks.rag_eval.utils import error_utils

CHUNK_PRECISION_IS_LOW_MESSAGE = (
    "The root cause of failure is traced to the negative ratings of "
    f"{assessment_config.CHUNK_RELEVANCE.assessment_name} which marked all retrieved "
    "chunks as irrelevant to the question. "
    f"See the {assessment_config.CHUNK_RELEVANCE.assessment_name} rationale for more details."
)

PER_CHUNK_ASSESSMENTS_FAIL_MESSAGE = (
    "The root cause of failure is traced to the negative per-chunk ratings of {judge_name}. "
    "See the {judge_name} rationale for more details."
)

DEFAULT_FAIL_MESSAGE = (
    "The root cause of failure is traced to the negative rating of {judge_name}. "
    "See the {judge_name} rationale for more details."
)

SUGGESTED_ACTIONS = {
    assessment_config.CONTEXT_SUFFICIENCY.assessment_name: (
        "First, you should ensure that the vector DB contains the "
        "missing information. Second, you should tune your retrieval "
        "step to retrieve the missing information (see the judges' rationales to understand what's missing). "
        "Here are some methods that you can try for this: retrieving more chunks, trying different embedding models, "
        "or over-fetching & reranking results."
    ),
    assessment_config.CHUNK_RELEVANCE.assessment_name: (
        "First, you should ensure that relevant chunks are present in the "
        "vector DB. Second, you should tune your retrieval step to retrieve the missing information (see the judges' "
        "rationales to understand what's missing). Here are some methods that you can try for this: "
        "retrieving more chunks, trying different embedding models, or over-fetching & reranking results."
    ),
    assessment_config.HARMFULNESS.assessment_name: (
        "Consider implementing guardrails to prevent harmful content or a "
        "post-processing step to filter out harmful content."
    ),
    assessment_config.RELEVANCE_TO_QUERY.assessment_name: (
        "Consider improving the prompt template to encourage direct, "
        "specific responses, re-ranking retrievals to provide more relevant chunks to the LLM earlier "
        "in the prompt, or using a more capable LLM."
    ),
    assessment_config.GROUNDEDNESS.assessment_name: (
        "Consider updating the prompt template to emphasize "
        "reliance on retrieved context, using a more capable LLM, or implementing a post-generation "
        "verification step."
    ),
    assessment_config.CORRECTNESS.assessment_name: (
        "Consider improving the prompt template to encourage direct, "
        "specific responses, re-ranking retrievals to provide more relevant chunks to the LLM earlier in "
        "the prompt, or using a more capable LLM."
    ),
}


def compute_overall_assessment(
    assessment_results: Collection[entities.AssessmentResult],
) -> Optional[entities.Rating]:
    """
    Compute the overall assessment based on the individual assessment results and applying our RCA logic.
    """

    overall_assessment = _compute_overall_assessment(assessment_results)

    # TODO: Remove this check after the RCA is fully implemented
    if (
        overall_assessment is not None
        and not env_vars.AGENT_EVAL_SHOW_RCA_RATIONALE.get()
    ):
        overall_assessment.rationale = None

    return overall_assessment


# ================ Overall assessment ================
def construct_fail_assessment(assessment: entities.AssessmentResult) -> entities.Rating:
    """
    Construct fail assessment with an RCA from the given assessment.

    The rationale of the failed assessment has the following format for builtin-judges:
    "[judge_name] {message}. *Suggested Action*: {action}".

    For custom judges, the rationale is: "[judge_name] {message}".

    The "message" part is defined as follows:
    - DEFAULT_FAIL_MESSAGE for per-request assessments, with the judge name substituted.
    - CHUNK_PRECISION_IS_LOW_MESSAGE for chunk relevance.
    - PER_CHUNK_ASSESSMENTS_FAIL_MESSAGE for other per-chunk assessments.

    The action for built-in judges is defined in SUGGESTED_ACTIONS.
    """
    judge_name = assessment.assessment_name

    if isinstance(assessment, entities.PerRequestAssessmentResult):
        message = DEFAULT_FAIL_MESSAGE.format(judge_name=judge_name)
    elif isinstance(assessment, entities.PerChunkAssessmentResult):
        if judge_name == assessment_config.CHUNK_RELEVANCE.assessment_name:
            message = CHUNK_PRECISION_IS_LOW_MESSAGE
        else:
            message = PER_CHUNK_ASSESSMENTS_FAIL_MESSAGE.format(judge_name=judge_name)
    else:
        raise error_utils.ValidationError(
            f"""Invalid assessment result type provided: {type(assessment)}. 
            Expected one of: [{type(entities.PerRequestAssessmentResult), type(entities.PerChunkAssessmentResult)}]"""
        )

    rationale = f"[{judge_name}] {message}"

    action = SUGGESTED_ACTIONS.get(judge_name)
    if action is not None:
        rationale += f" **Suggested Actions**: {action}"

    return entities.Rating.value(
        categorical_value=entities.CategoricalRating.NO,
        rationale=rationale,
    )


def construct_pass_assessment() -> entities.Rating:
    """Construct pass assessment."""
    return entities.Rating.value(
        categorical_value=entities.CategoricalRating.YES,
    )


def _compute_overall_assessment(
    assessment_results: Collection[entities.AssessmentResult],
) -> Optional[entities.Rating]:
    """
    Compute the overall assessment based on the individual assessment results and applying our RCA logic.

    The categorical rating contains a high-level tag describing quality issues. If our logic does
    not recognize the set of judges, we return `YES` or `NO` based on a logical AND of all judges.
    Note that all errors are ignored in the logical AND.

    The rationale contains the root cause analysis (RCA) and potential fixes based on the assessment
    results. If all judges are passing, the RCA will be empty.
    """
    # Filter out errored per-request assessments or fully errored per-chunk assessments out of RCA
    filtered_assessment_results = [
        assessment_result
        for assessment_result in assessment_results
        if (
            isinstance(assessment_result, entities.PerRequestAssessmentResult)
            and assessment_result.rating.error_code is None
        )
        or (
            isinstance(assessment_result, entities.PerChunkAssessmentResult)
            and any(
                rating.error_code is None
                for rating in assessment_result.positional_rating.values()
            )
        )
    ]
    if not len(filtered_assessment_results):
        return None

    assessment_results_mapping = {
        assessment_result.assessment_name: assessment_result
        for assessment_result in filtered_assessment_results
    }

    # Find the first negative assessment
    first_negative_assessment = next(
        (
            assessment_result
            for assessment_result in filtered_assessment_results
            if _assessment_is_fail(assessment_result)
        ),
        None,
    )

    # Early return if there are no negative assessments.
    if first_negative_assessment is None:
        return construct_pass_assessment()

    # RCA logic. We will check judges in the following order to find the first one that fails.
    assessments_to_check = [
        assessment_config.CONTEXT_SUFFICIENCY.assessment_name,
        assessment_config.CHUNK_RELEVANCE.assessment_name,
        assessment_config.GROUNDEDNESS.assessment_name,
        assessment_config.CORRECTNESS.assessment_name,
        assessment_config.RELEVANCE_TO_QUERY.assessment_name,
        assessment_config.HARMFULNESS.assessment_name,
    ]
    for assessment_name in assessments_to_check:
        assessment = assessment_results_mapping.get(assessment_name)
        if _assessment_is_fail(assessment):
            return construct_fail_assessment(assessment)

    # Built-in logic passes, so some custom judge failed. Return a rating indicating the first failed judge.
    return construct_fail_assessment(first_negative_assessment)


def _assessment_is_fail(
    assessment_result: Optional[entities.AssessmentResult],
) -> bool:
    """
    Check if an assessment result corresponds to a failure. For per-request assessments, the rating should be NO. For
    per-chunk assessments, at least one rating should be NO, except for chunk relevance, for which
    all ratings must be NO.

    :param assessment_result: The assessment result
    :return: True if the assessment result is a failure per the rule above, False otherwise or if the input is None.
    """
    if assessment_result is None:
        return False

    if isinstance(assessment_result, entities.PerRequestAssessmentResult):
        return (
            assessment_result.rating.categorical_value == entities.CategoricalRating.NO
        )
    elif isinstance(assessment_result, entities.PerChunkAssessmentResult):
        positional_ratings_are_no = [
            rating.categorical_value == entities.CategoricalRating.NO
            for rating in assessment_result.positional_rating.values()
            if rating.error_code is None
        ]
        if (
            assessment_result.assessment_name
            == assessment_config.CHUNK_RELEVANCE.assessment_name
        ):
            return all(positional_ratings_are_no)
        else:
            return any(positional_ratings_are_no)
    else:
        raise error_utils.ValidationError(
            f"""Invalid assessment result type provided: {type(assessment_result)}. 
            Expected one of: [{type(entities.PerRequestAssessmentResult), type(entities.PerChunkAssessmentResult)}]"""
        )
