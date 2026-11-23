from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.knowledge.documents.chunk_service import (
    DocumentChunkService,
)
from app.knowledge.documents.file_extractor import (
    FileTextExtractor,
    UnsupportedFileTypeError,
)
from app.knowledge.documents.indexing_service import (
    DocumentIndexingService,
)
from app.knowledge.documents.repository import (
    DocumentRepository,
)
from app.knowledge.documents.schemas import (
    DocumentCreate,
)


class DocumentIngestionService:
    @staticmethod
    async def ingest(
        db: AsyncSession,
        title: str,
        filename: str,
        mime_type: str | None,
        file_content: bytes,
    ):
        try:
            text = FileTextExtractor.extract(
                filename=filename,
                content=file_content,
            )

        except UnsupportedFileTypeError as exc:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=str(exc),
            ) from exc

        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc),
            ) from exc

        document = await DocumentRepository.create(
            db,
            DocumentCreate(
                title=title,
                source="upload",
                file_name=filename,
                mime_type=mime_type,
                content=text,
                status="pending",
            ),
        )

        await DocumentChunkService.process_document(
            db=db,
            document_id=document.id,
        )

        await DocumentIndexingService.index_document(
            db=db,
            document_id=document.id,
        )

        document = await DocumentRepository.get_by_id(
            db,
            document.id,
        )

        return document
