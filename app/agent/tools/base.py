from abc import ABC, abstractmethod
from typing import Any

class BaseTool(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, arguments: dict[str, Any]) -> Any:
        pass

    