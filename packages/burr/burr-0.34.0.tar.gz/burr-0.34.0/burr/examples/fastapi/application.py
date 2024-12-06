import functools
import os
from typing import List, Optional, Tuple

import instructor
import openai
import pydantic

from burr.core import Application, ApplicationBuilder, State, action, expr
from burr.core.graph import GraphBuilder
from burr.tracking import LocalTrackingClient


class ClarificationQuestions(pydantic.BaseModel):
    question: List[str]


class ClarificationAnswers(pydantic.BaseModel):
    answers: List[str]


class Email(pydantic.BaseModel):
    subject: str
    contents: str


class EmailAssistantState(pydantic.BaseModel):
    email_to_respond: Optional[str] = None
    response_instructions: Optional[str] = None
    questions: Optional[ClarificationQuestions] = None
    answers: Optional[ClarificationAnswers] = None
    draft_history: List[Email] = pydantic.Field(default_factory=list)
    current_draft: Optional[Email] = None
    feedback_history: List[str] = pydantic.Field(default_factory=list)
    feedback: Optional[str] = None
    final_draft: Optional[str] = None


@functools.lru_cache
def _get_openai_client():
    openai_client = instructor.from_openai(openai.OpenAI())
    return openai_client


@action.pydantic(reads=[], writes=["email_to_respond", "response_instructions"])
def process_input(
    state: EmailAssistantState, email_to_respond: str, response_instructions: str
) -> EmailAssistantState:
    """Processes input from user and updates state with the input."""
    state.email_to_respond = email_to_respond
    state.response_instructions = response_instructions
    return state


@action.pydantic(reads=["response_instructions", "email_to_respond"], writes=["questions"])
def determine_clarifications(state: EmailAssistantState) -> EmailAssistantState:
    """Determines if the response instructions require clarification."""
    # TODO -- query an LLM to determine if the response instructions are clear, or if it needs more information
    client = _get_openai_client()
    # TODO -- use instructor to get a pydantic model
    result = client.chat.completions.create(
        model="gpt-4",
        response_model=ClarificationQuestions,
        messages=[
            {
                "role": "system",
                "content": "You are a chatbot that has the task of generating responses to an email on behalf of a user. ",
            },
            {
                "role": "user",
                "content": (
                    f"The email you are to respond to is: {state.email_to_respond}."
                    f"Your instructions are: {state.response_instructions}."
                    "Your first task is to ask any clarifying questions for the user"
                    " who is asking you to respond to this email. These clarifying questions are for the user, "
                    "*not* for the original sender of the email. Please "
                    "generate a list of at most 3 questions (and you really can do less -- 2, 1, or even none are OK! joined by newlines, included only if you feel that you could leverage "
                    "clarification (my time is valuable)."
                    "The questions, joined by newlines, must be the only text you return. If you do not need clarification, return an empty string."
                ),
            },
        ],
    )
    state.questions = result
    return state


@action.pydantic(reads=["questions"], writes=["answers"])
def clarify_instructions(
    state: EmailAssistantState, clarification_inputs: list[str]
) -> EmailAssistantState:
    """Clarifies the response instructions if needed."""
    state.answers = ClarificationAnswers(answers=clarification_inputs)
    return state


@action.pydantic(
    reads=[
        "email_to_respond",
        "response_instructions",
        "answers",
        "questions",
        "draft_history",
        "feedback",
    ],
    writes=["current_draft", "draft_history"],
)
def formulate_draft(state: EmailAssistantState) -> EmailAssistantState:
    """Formulates the draft response based on the incoming email, response instructions, and any clarifications."""
    # TODO -- query an LLM to generate the draft response
    email_to_respond = state.email_to_respond
    response_instructions = state.response_instructions
    client = _get_openai_client()
    # TODO -- use instructor to get a pydantic model
    clarification_answers_formatted_q_a = "\n".join(
        [f"Q: {q}\nA: {a}" for q, a in zip(state.questions.question, state.answers.answers)]
    )
    instructions = [
        f"The email you are to respond to is: {email_to_respond}.",
        f"Your instructions are: {response_instructions}.",
        "You have already asked the following questions and received the following answers: ",
        clarification_answers_formatted_q_a,
    ]
    if state.draft_history:
        instructions.append("Your previous draft was: ")
        instructions.append(state["draft_history"][-1])
        instructions.append(
            "you received the following feedback, please incorporate this into your response: "
        )
        instructions.append(state["feedback"])
    instructions.append("Please generate a draft response using all this information!")
    prompt = " ".join(instructions)

    result = client.chat.completions.create(
        model="gpt-4",
        response_model=Email,
        messages=[
            {
                "role": "system",
                "content": "You are a chatbot that has the task of generating responses to an email. ",
            },
            {"role": "user", "content": prompt},
        ],
    )
    state.current_draft = result
    state.draft_history.append(result)
    return state

    # # returning some intermediate results for debugging as well
    # return {"prompt": prompt, "current_draft": content}, state.update(current_draft=content).append(
    #     draft_history=result
    # )


@action.pydantic(reads=[], writes=["feedback", "feedback_history"])
def process_feedback(state: EmailAssistantState, feedback: str) -> EmailAssistantState:
    """Processes feedback from user and updates state with the feedback."""
    state.feedback_history.append(feedback)
    state.feedback = feedback
    return state


@action.pydantic(reads=["current_draft"], writes=["final_draft"])
def final_result(state: EmailAssistantState) -> EmailAssistantState:
    """Returns the final result of the process."""
    state.final_draft = state.current_draft
    return state


graph = (
    GraphBuilder()
    .with_actions(
        process_input,
        determine_clarifications,
        clarify_instructions,
        formulate_draft,
        process_feedback,
        final_result,
    )
    .with_transitions(
        ("process_input", "determine_clarifications"),
        (
            "determine_clarifications",
            "clarify_instructions",
            expr("len(questions) > 0"),
        ),
        ("determine_clarifications", "formulate_draft"),
        ("clarify_instructions", "formulate_draft"),
        ("formulate_draft", "process_feedback"),
        ("process_feedback", "formulate_draft", expr("len(feedback) > 0")),
        ("process_feedback", "final_result"),
    )
).build()


def application(
    app_id: str = None, project: str = "demo_email_assistant", username: str = None
) -> Application:
    tracker = LocalTrackingClient(project=project)
    builder = (
        ApplicationBuilder()
        .with_graph(graph)
        .with_tracker("local", project=project)
        .with_identifiers(app_id=app_id, partition_key=username)
        .initialize_from(
            tracker,
            resume_at_next_action=True,
            default_state={"draft_history": []},
            default_entrypoint="process_input",
        )
    )
    return builder.build()


if __name__ == "__main__":
    app = application()
    app.visualize(
        output_file_path="statemachine", include_conditions=True, include_state=True, format="png"
    )
