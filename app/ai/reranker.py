from sentence_transformers import CrossEncoder

from app.core.config import settings
from app.knowledge.search.schemas import SearchResult


class RerankerService:
    _model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    @classmethod
    def rerank(
        cls,
        query: str,
        results: list[SearchResult],
        limit: int,
    ) -> list[SearchResult]:
        if not results:
            return []

        pairs = [
            (
                query,
                result.content,
            )
            for result in results
        ]

        scores = cls._model.predict(pairs)

        reranked_results = [
            result.model_copy(update={"score": float(score)})
            for result, score in zip(
                results,
                scores,
                strict=True,
            )
            if float(score) >= settings.rerank_min_score
        ]

        reranked_results.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return reranked_results[:limit]
