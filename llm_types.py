from typing import Literal, TypedDict


class LLMMessage(TypedDict):
    role: Literal["user", "assistant"]
    content: str
