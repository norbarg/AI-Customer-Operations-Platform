from sqlalchemy import func, literal_column, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.knowledge.documents.chunk_models import DocumentChunk
from app.knowledge.documents.models import Document
from app.knowledge.search.schemas import SearchResult


class KeywordSearchRepository:
    @staticmethod
    async def search(
        db: AsyncSession,
        query: str,
        limit: int,
    ) -> list[SearchResult]:
        english_config = literal_column("'english'::regconfig")

        search_vector = func.to_tsvector(
            english_config,
            DocumentChunk.content,
        )

        search_query = func.websearch_to_tsquery(
            english_config,
            query,
        )

        rank = func.ts_rank_cd(
            search_vector,
            search_query,
        ).label("rank")

        stmt = (
            select(
                DocumentChunk,
                Document.title,
                rank,
            )
            .join(
                Document,
                Document.id == DocumentChunk.document_id,
            )
            .where(search_vector.op("@@")(search_query))
            .order_by(rank.desc())
            .limit(limit)
        )

        result = await db.execute(stmt)

        rows = result.all()

        return [
            SearchResult(
                chunk_id=chunk.id,
                document_id=chunk.document_id,
                document_title=document_title,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                score=float(rank_value),
            )
            for chunk, document_title, rank_value in rows
        ]
