from openai import AsyncOpenAI

from app.core.config import settings

openrouter_client = AsyncOpenAI(
    api_key=settings.openrouter_api_key,
    base_url=settings.openrouter_base_url,
)
