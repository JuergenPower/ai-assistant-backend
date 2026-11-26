import os
import secrets
from functools import lru_cache
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from openai import APIError
from pydantic import BaseModel, Field

from llm_provider import OpenAIResponsesProvider, ProviderConfigurationError
from llm_types import LLMMessage

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
bearer_scheme = HTTPBearer(auto_error=False)


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1)


class ResponsesRequest(BaseModel):
    messages: list[Message] = Field(min_length=1)


class ResponsesResult(BaseModel):
    text: str


@lru_cache
def get_llm_provider() -> OpenAIResponsesProvider:
    return OpenAIResponsesProvider()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/responses", response_model=ResponsesResult)
def create_response(
    request: ResponsesRequest,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> ResponsesResult:
    expected_token = os.getenv("BACKEND_ACCESS_TOKEN")
    if not expected_token:
        raise HTTPException(
            status_code=500,
            detail="Backend access token is not configured.",
        )

    if (
        credentials is None
        or not secrets.compare_digest(
            credentials.credentials.encode("utf-8"),
            expected_token.encode("utf-8"),
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing access token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        provider = get_llm_provider()
        text = provider.generate(
            [
                LLMMessage(role=message.role, content=message.content)
                for message in request.messages
            ]
        )
    except ProviderConfigurationError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    except APIError as error:
        raise HTTPException(
            status_code=502,
            detail="The LLM provider request failed.",
        ) from error

    return ResponsesResult(text=text)
