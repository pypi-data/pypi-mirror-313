import functools

from burr.integrations.pydantic import PydanticTypingSystem
from burr.tracking import LocalTrackingClient

from examples.fastapi.application import EmailAssistantState
from examples.fastapi import application as email_assistant_application

"""
This module contains the FastAPI code that interacts with the Burr application.
"""

import importlib
import os
from typing import Any, Dict, List, Literal, Optional

import pydantic
from fastapi import APIRouter, FastAPI

from burr.core import Application, ApplicationBuilder

# email_assistant_application = importlib.import_module(
#     "burr.examples.email-assistant.application"
# )  # noqa: F401

app = FastAPI()
router = APIRouter()


class AppResponse(pydantic.BaseModel):
    app_id: str
    next_step: Optional[Literal["process_input", "clarify_instructions", "process_feedback"]]
    state: EmailAssistantState

    @staticmethod
    def from_app(app: Application[EmailAssistantState]) -> "AppResponse":
        return AppResponse(
            app_id=app.uid,
            next_step=app.get_next_action().name,  # type: ignore
            state=app.state.data,
        )


@functools.lru_cache(maxsize=128)
def _get_application(project_id: str, app_id: str) -> Application[EmailAssistantState]:
    """Utility to get the application. Depending on
    your use-case you might want to reload from state every time (or consider cache invalidation)"""
    # graph = email_assistant_application.application(app_id=app_id, project=project_id)
    graph = email_assistant_application.graph
    tracker = LocalTrackingClient(project=project_id)
    builder = (
        ApplicationBuilder()
        .with_graph(graph)
        .with_tracker(tracker := LocalTrackingClient(project=project_id))
        .with_identifiers(app_id=app_id)
        .with_typing(PydanticTypingSystem(EmailAssistantState))
        .initialize_from(
            tracker,
            resume_at_next_action=True,
            default_state={"draft_history": []},
            default_entrypoint="process_input",
        )
    ) 
    return builder.build()


def _run_through(project_id: str, app_id: Optional[str], inputs: Dict[str, Any]) -> AppResponse:
    """This advances the state machine, moving through to the next 'halting' point"""
    if app_id == "create_new":  # quick hack to allow for null
        app_id = None
    email_assistant_app = _get_application(project_id, app_id)
    email_assistant_app.run(  # Using this as a side-effect, we'll just get the state aft
        halt_before=["clarify_instructions", "process_feedback"],
        halt_after=["final_result"],
        inputs=inputs,
    )
    return AppResponse(
        next_step=email_assistant_app.get_next_action().name,  # type: ignore
        state=email_assistant_app.state.data,
        app_id=email_assistant_app.uid,
    )


class DraftInit(pydantic.BaseModel):
    email_to_respond: str
    response_instructions: str


@router.post("/create_new/{project_id}/{app_id}")
def create_new_application(project_id: str, app_id: str) -> str:
    app = _get_application(project_id, app_id)
    return app.uid


@router.post("/create/{project_id}/{app_id}")
def initialize_draft(project_id: str, app_id: str, draft_data: DraftInit) -> AppResponse:
    """Endpoint to initialize the draft with the email and instructions

    :param project_id: ID of the project (used by telemetry tracking/storage)
    :param app_id: ID of the application (used to reference the app)
    :param draft_data: Data to initialize the draft
    :return: The state of the application after initialization
    """
    return _run_through(
        project_id,
        app_id,
        dict(
            email_to_respond=draft_data.email_to_respond,
            response_instructions=draft_data.response_instructions,
        ),
    )


class QuestionAnswers(pydantic.BaseModel):
    answers: List[str]


@router.post("/answer_questions/{project_id}/{app_id}")
def answer_questions(
    project_id: str, app_id: str, question_answers: QuestionAnswers
) -> AppResponse:
    """Endpoint to answer questions the LLM provides

    :param project_id: ID of the project (used by telemetry tracking/storage)
    :param app_id: ID of the application (used to reference the app)
    :param question_answers: Answers to the questions
    :return: The state of the application after answering the questions
    """
    return _run_through(project_id, app_id, dict(clarification_inputs=question_answers.answers))


class Feedback(pydantic.BaseModel):
    feedback: str


@router.post("/provide_feedback/{project_id}/{app_id}")
def provide_feedback(project_id: str, app_id: str, feedback: Feedback) -> AppResponse:
    """Endpoint to provide feedback to the LLM

    :param project_id: ID of the project (used by telemetry tracking/storage)
    :param app_id: ID of the application (used to reference the app)
    :param feedback: Feedback to provide to the LLM
    :return: The state of the application after providing feedback
    """
    return _run_through(project_id, app_id, dict(feedback=feedback.feedback))


@router.get("/state/{project_id}/{app_id}")
def get_state(project_id: str, app_id: str) -> AppResponse:
    """Get the current state of the application

    :param project_id: ID of the project (used by telemetry tracking/storage)
    :param app_id:  ID of the application (used to reference the app)
    :return: The state of the application
    """
    email_assistant_app = _get_application(project_id, app_id)
    return AppResponse.from_app(email_assistant_app)


@router.get("/validate/{project_id}/{app_id}")
def validate_environment() -> Optional[str]:
    """Validate the environment"""
    if "OPENAI_API_KEY" in os.environ:
        return
    return (
        "You have not set an API key for [OpenAI](https://www.openai.com). Do this "
        "by setting the environment variable `OPENAI_API_KEY` to your key. "
        "You can get a key at https://platform.openai.com. "
        "You can still look at chat history/examples."
    )


if __name__ == "__main__":
    import uvicorn

    app.include_router(router, prefix="")

    uvicorn.run(app, host="localhost", port=7242)
