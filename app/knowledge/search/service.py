import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.embeddings import EmbeddingService
from app.core.config import settings
from app.knowledge.search.keyword_repository import (
    KeywordSearchRepository,
)
from app.knowledge.search.schemas import SearchResult
from app.knowledge.vector.qdrant import (
    ensure_collection,
    qdrant_client,
)


class SearchService:
    @staticmethod
    async def search(
        db: AsyncSession,
        query: str,
        limit: int,
        score_threshold: float,
    ) -> list[SearchResult]:
        vector_results, keyword_results = await asyncio.gather(
            SearchService._vector_search(
                query=query,
                limit=settings.hybrid_candidate_limit,
                score_threshold=score_threshold,
            ),
            KeywordSearchRepository.search(
                db=db,
                query=query,
                limit=settings.hybrid_candidate_limit,
            ),
        )

        return SearchService._rrf_merge(
            vector_results=vector_results,
            keyword_results=keyword_results,
            limit=limit,
        )

    @staticmethod
    async def _vector_search(
        query: str,
        limit: int,
        score_threshold: float,
    ) -> list[SearchResult]:
        await ensure_collection()

        query_vector = await EmbeddingService.embed_text(query)

        response = await qdrant_client.query_points(
            collection_name=(settings.qdrant_collection),
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
                    score=float(point.score),
                )
            )

        return results

    @staticmethod
    def _rrf_merge(
        vector_results: list[SearchResult],
        keyword_results: list[SearchResult],
        limit: int,
    ) -> list[SearchResult]:
        scores: dict[int, float] = {}
        results_by_chunk: dict[
            int,
            SearchResult,
        ] = {}

        for rank, result in enumerate(
            vector_results,
            start=1,
        ):
            results_by_chunk[result.chunk_id] = result

            scores[result.chunk_id] = scores.get(result.chunk_id, 0) + 1 / (
                settings.hybrid_rrf_k + rank
            )

        for rank, result in enumerate(
            keyword_results,
            start=1,
        ):
            results_by_chunk[result.chunk_id] = result

            scores[result.chunk_id] = scores.get(result.chunk_id, 0) + 1 / (
                settings.hybrid_rrf_k + rank
            )

        sorted_chunk_ids = sorted(
            scores,
            key=scores.get,
            reverse=True,
        )

        merged_results: list[SearchResult] = []

        max_rrf_score = 2 / (settings.hybrid_rrf_k + 1)

        for chunk_id in sorted_chunk_ids[:limit]:
            result = results_by_chunk[chunk_id]

            normalized_score = scores[chunk_id] / max_rrf_score

            merged_results.append(result.model_copy(update={"score": normalized_score}))

        return merged_results
