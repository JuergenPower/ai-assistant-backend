import os

from openai import OpenAI
from openai.types.responses import ResponseInputParam

from llm_types import LLMMessage


class ProviderConfigurationError(Exception):
    pass


class OpenAIResponsesProvider:
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL")
        if not api_key:
            raise ProviderConfigurationError("OPENAI_API_KEY is not configured.")
        if not model:
            raise ProviderConfigurationError("OPENAI_MODEL is not configured.")

        self._client = OpenAI(api_key=api_key)
        self._model = model

    def generate(self, messages: list[LLMMessage]) -> str:
        openai_input: ResponseInputParam = [
            {"role": message["role"], "content": message["content"]}
            for message in messages
        ]
        response = self._client.responses.create(
            model=self._model,
            input=openai_input,
        )
        return response.output_text
