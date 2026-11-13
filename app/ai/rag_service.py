from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.context_builder import ContextBuilder
from app.ai.llm import LLMService
from app.ai.reranker import RerankerService
from app.ai.schemas import RAGResponse, RAGSource
from app.core.config import settings
from app.knowledge.search.service import SearchService


class RAGService:
    @staticmethod
    async def answer(
        db: AsyncSession,
        question: str,
    ) -> RAGResponse:
        search_results = await SearchService.search(
            db=db,
            query=question,
            limit=settings.rerank_candidate_limit,
            score_threshold=settings.rag_min_score,
        )

        search_results = RerankerService.rerank(
            query=question,
            results=search_results,
            limit=settings.rag_search_limit,
        )

        if not search_results:
            return RAGResponse(
                question=question,
                answer=(
                    "There is not enough relevant "
                    "information in the knowledge base "
                    "to answer this question."
                ),
                sources=[],
            )

        context, used_results = ContextBuilder.build(search_results)

        if not context or not used_results:
            return RAGResponse(
                question=question,
                answer=(
                    "There is not enough relevant "
                    "information in the knowledge base "
                    "to answer this question."
                ),
                sources=[],
            )

        answer = await LLMService.generate_answer(
            question=question,
            context=context,
        )

        sources = [
            RAGSource(
                citation=f"S{index}",
                chunk_id=result.chunk_id,
                document_id=result.document_id,
                document_title=result.document_title,
                chunk_index=result.chunk_index,
                relevance_score=result.score,
            )
            for index, result in enumerate(
                used_results,
                start=1,
            )
        ]

        return RAGResponse(
            question=question,
            answer=answer,
            sources=sources,
        )
