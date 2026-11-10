from qdrant_client import AsyncQdrantClient, models

from app.core.config import settings

qdrant_client = AsyncQdrantClient(
    url=settings.qdrant_url,
)


async def ensure_collection() -> None:
    collection_exists = await qdrant_client.collection_exists(
        settings.qdrant_collection
    )

    if collection_exists:
        return

    await qdrant_client.create_collection(
        collection_name=settings.qdrant_collection,
        vectors_config=models.VectorParams(
            size=settings.embedding_dimensions,
            distance=models.Distance.COSINE,
        ),
    )
