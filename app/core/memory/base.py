from abc import ABC, abstractmethod

class BaseMemory(ABC):

    @abstractmethod
    def write(self, user_id: int, content: str):
        pass

    @abstractmethod
    def read(self, user_id: int):
        pass