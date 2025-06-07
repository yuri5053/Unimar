import httpx
from app.config import OPENAI_API_KEY
from app.providers.base_provider import BaseProvider

class OpenAIProvider(BaseProvider):
    async def responder(self, pergunta: str) -> str:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "Você é um tutor educacional."},
                {"role": "user", "content": pergunta}
            ]
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
