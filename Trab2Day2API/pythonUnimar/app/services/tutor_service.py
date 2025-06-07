from app.providers.openai_provider import OpenAIProvider
from app.providers.anthropic_provider import AnthropicProvider
from app.providers.tutor_ia_fake import TutorIAFake
from app.config import PROVIDER

class TutorService:
    def __init__(self):
        if PROVIDER == "openai":
            self.llm = OpenAIProvider()
        elif PROVIDER == "anthropic":
            self.llm = AnthropicProvider()
        else:
            self.llm = TutorIAFake()

    async def processar_pergunta(self, pergunta: str) -> str:
        return await self.llm.responder(pergunta)
