from abc import ABC, abstractmethod


class TutorIAInterface(ABC):
    @abstractmethod
    def responder(self, pergunta: str) -> str:
        """
        Método que todas as implementações do Tutor IA devem implementar.

        Deve receber uma pergunta (string) e retornar a resposta (string).
        """
        pass
