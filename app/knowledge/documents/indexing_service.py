from fastapi import HTTPException, status
from qdrant_client import models
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.embeddings import EmbeddingService
from app.core.config import settings
from app.knowledge.documents.chunk_repository import DocumentChunkRepository
from app.knowledge.documents.repository import DocumentRepository
from app.knowledge.documents.schemas import DocumentUpdate
from app.knowledge.vector.qdrant import ensure_collection, qdrant_client


class DocumentIndexingService:
    @staticmethod
    async def index_document(
        db: AsyncSession,
        document_id: int,
    ) -> int:
        document = await DocumentRepository.get_by_id(
            db,
            document_id,
        )

        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found",
            )

        chunks = await DocumentChunkRepository.get_by_document_id(
            db,
            document_id,
        )

        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Document has no chunks. Chunk the document first.",
            )

        await DocumentRepository.update(
            db,
            document,
            DocumentUpdate(status="processing"),
        )

        try:
            await ensure_collection()

            texts = [chunk.content for chunk in chunks]

            embeddings = await EmbeddingService.embed_texts(texts)

            points = [
                models.PointStruct(
                    id=chunk.id,
                    vector=embedding,
                    payload={
                        "chunk_id": chunk.id,
                        "document_id": document.id,
                        "document_title": document.title,
                        "chunk_index": chunk.chunk_index,
                        "content": chunk.content,
                    },
                )
                for chunk, embedding in zip(
                    chunks,
                    embeddings,
                    strict=True,
                )
            ]

            await qdrant_client.delete(
                collection_name=settings.qdrant_collection,
                points_selector=models.FilterSelector(
                    filter=models.Filter(
                        must=[
                            models.FieldCondition(
                                key="document_id",
                                match=models.MatchValue(
                                    value=document.id,
                                ),
                            ),
                        ],
                    )
                ),
                wait=True,
            )

            await qdrant_client.upsert(
                collection_name=settings.qdrant_collection,
                points=points,
                wait=True,
            )

            await DocumentRepository.update(
                db,
                document,
                DocumentUpdate(status="ready"),
            )

            return len(points)

        except HTTPException:
            raise

        except Exception:
            await DocumentRepository.update(
                db,
                document,
                DocumentUpdate(status="failed"),
            )

            raise
