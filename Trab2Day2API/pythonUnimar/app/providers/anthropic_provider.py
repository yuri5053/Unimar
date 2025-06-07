import httpx
from app.config import ANTHROPIC_API_KEY
from app.providers.base_provider import BaseProvider

class AnthropicProvider(BaseProvider):
    async def responder(self, pergunta: str) -> str:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        data = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 1000,
            "messages": [
                {"role": "user", "content": pergunta}
            ]
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()["content"][0]["text"]
