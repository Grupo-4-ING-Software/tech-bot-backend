from abc import ABC, abstractmethod
from typing import Any

class AIProvider(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    async def initialize(self) -> None:
        pass 