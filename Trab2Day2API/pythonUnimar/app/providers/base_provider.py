from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    async def responder(self, pergunta: str) -> str:
        pass
