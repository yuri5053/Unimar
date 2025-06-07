from app.interfaces.tutor_interface import TutorIAInterface

class TutorIAFake(TutorIAInterface):
    async def responder(self, pergunta: str) -> str:
        return f"Você perguntou: '{pergunta}'. Esta é uma resposta simulada do Tutor IA (modo offline)."
