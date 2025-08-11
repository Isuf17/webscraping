from abc import ABC, abstractmethod


class IGeminiClient(ABC):
    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        pass
