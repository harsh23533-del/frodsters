import httpx

from app.core.config import settings

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "google/gemini-flash-1.5"


async def complete(messages: list[dict], model: str = DEFAULT_MODEL, response_format: str | None = None) -> str:
    """Send a chat-completion request to OpenRouter and return the reply text."""
    payload = {"model": model, "messages": messages}
    if response_format == "json":
        payload["response_format"] = {"type": "json_object"}

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            OPENROUTER_URL,
            headers={"Authorization": f"Bearer {settings.openrouter_api_key}"},
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
