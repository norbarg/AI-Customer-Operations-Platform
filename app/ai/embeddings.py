from openai import AsyncOpenAI

from app.core.config import settings

client = AsyncOpenAI(
    api_key=settings.openrouter_api_key,
    base_url=settings.openrouter_base_url,
)


class EmbeddingService:
    @staticmethod
    async def embed_text(
        text: str,
    ) -> list[float]:
        response = await client.embeddings.create(
            model=settings.embedding_model,
            input=text,
        )

        return response.data[0].embedding

    @staticmethod
    async def embed_texts(
        texts: list[str],
    ) -> list[list[float]]:
        response = await client.embeddings.create(
            model=settings.embedding_model,
            input=texts,
        )

        return [item.embedding for item in response.data]
