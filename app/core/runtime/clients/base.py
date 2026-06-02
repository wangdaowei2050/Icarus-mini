from abc import ABC, abstractmethod
from typing import Generator

class BaseProviderClient(ABC):

    @abstractmethod
    def invoke_llm(self, model_name: str, messages: list) -> Generator[str, None, None]:
        pass
