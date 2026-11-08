from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.documents.chunk_models import DocumentChunk


class DocumentChunkRepository:
    @staticmethod
    async def create_many(
        db: AsyncSession,
        document_id: int,
        chunks: list[str],
    ) -> list[DocumentChunk]:
        chunk_models = [
            DocumentChunk(
                document_id=document_id,
                chunk_index=index,
                content=content,
            )
            for index, content in enumerate(chunks)
        ]

        db.add_all(chunk_models)

        await db.commit()

        for chunk in chunk_models:
            await db.refresh(chunk)

        return chunk_models

    @staticmethod
    async def get_by_document_id(
        db: AsyncSession,
        document_id: int,
    ) -> list[DocumentChunk]:
        result = await db.execute(
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index)
        )

        return list(result.scalars().all())

    @staticmethod
    async def delete_by_document_id(
        db: AsyncSession,
        document_id: int,
    ) -> None:
        await db.execute(
            delete(DocumentChunk).where(DocumentChunk.document_id == document_id)
        )

        await db.commit()
