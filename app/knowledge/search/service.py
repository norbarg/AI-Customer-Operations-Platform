from app.ai.embeddings import EmbeddingService
from app.core.config import settings
from app.knowledge.search.schemas import SearchResult
from app.knowledge.vector.qdrant import ensure_collection, qdrant_client


class SearchService:
    @staticmethod
    async def search(
        query: str,
        limit: int = 5,
        score_threshold: float = 0.25,
    ) -> list[SearchResult]:
        await ensure_collection()

        query_vector = await EmbeddingService.embed_text(query)

        response = await qdrant_client.query_points(
            collection_name=settings.qdrant_collection,
            query=query_vector,
            limit=limit,
            score_threshold=score_threshold,
            with_payload=True,
        )

        results: list[SearchResult] = []

        for point in response.points:
            payload = point.payload or {}

            results.append(
                SearchResult(
                    chunk_id=int(payload["chunk_id"]),
                    document_id=int(payload["document_id"]),
                    document_title=str(payload["document_title"]),
                    chunk_index=int(payload["chunk_index"]),
                    content=str(payload["content"]),
                    score=point.score,
                )
            )

        return results
