from app.interfaces.tutor_interface import TutorIAInterface
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

class AnthropicTutorIA(TutorIAInterface):
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

    def responder(self, pergunta: str) -> str:
        try:
            response = self.client.completions.create(
                model="claude-2",
                prompt=HUMAN_PROMPT + pergunta + AI_PROMPT,
                max_tokens_to_sample=150,
                temperature=0.7,
            )
            return response.completion.strip()
        except Exception as e:
            return f"Erro na API Anthropic: {str(e)}"
