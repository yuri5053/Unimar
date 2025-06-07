from app.interfaces.tutor_interface import TutorIAInterface
import openai

class OpenAITutorIA(TutorIAInterface):
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def responder(self, pergunta: str) -> str:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": pergunta}],
                max_tokens=150,
                temperature=0.7,
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            return f"Erro na API OpenAI: {str(e)}"
