from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.documents.chunk_models import DocumentChunk
from app.documents.chunk_repository import DocumentChunkRepository
from app.documents.chunker import TextChunker
from app.documents.repository import DocumentRepository
from app.documents.schemas import DocumentUpdate


class DocumentChunkService:
    @staticmethod
    async def process_document(
        db: AsyncSession,
        document_id: int,
    ) -> list[DocumentChunk]:
        document = await DocumentRepository.get_by_id(
            db,
            document_id,
        )

        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found",
            )

        if not document.content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document has no content",
            )

        await DocumentRepository.update(
            db,
            document,
            DocumentUpdate(status="processing"),
        )

        try:
            chunker = TextChunker(
                max_chars=1200,
                overlap=200,
            )

            chunks = chunker.split(
                document.content,
            )

            if not chunks:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Document content produced no chunks",
                )

            await DocumentChunkRepository.delete_by_document_id(
                db,
                document_id,
            )

            saved_chunks = await DocumentChunkRepository.create_many(
                db,
                document_id,
                chunks,
            )

            await DocumentRepository.update(
                db,
                document,
                DocumentUpdate(status="chunked"),
            )

            return saved_chunks

        except HTTPException:
            raise

        except Exception:
            await DocumentRepository.update(
                db,
                document,
                DocumentUpdate(status="failed"),
            )

            raise
