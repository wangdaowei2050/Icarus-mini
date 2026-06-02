from typing import Generator
from openai import OpenAI

from app.core.runtime.clients.base import BaseProviderClient

class OpenAICompatibleClient(BaseProviderClient):

    def __init__(self, api_key: str, base_url: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    def invoke_llm(self, model_name: str, messages: list) -> Generator[str, None, None]:
        stream = self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=True,
        )

        for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content