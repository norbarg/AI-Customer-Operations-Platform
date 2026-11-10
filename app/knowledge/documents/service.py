from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.knowledge.documents.models import Document
from app.knowledge.documents.repository import DocumentRepository
from app.knowledge.documents.schemas import DocumentCreate, DocumentUpdate


class DocumentService:
    @staticmethod
    async def create_document(
        db: AsyncSession,
        data: DocumentCreate,
    ) -> Document:
        return await DocumentRepository.create(db, data)

    @staticmethod
    async def get_document(
        db: AsyncSession,
        document_id: int,
    ) -> Document:
        document = await DocumentRepository.get_by_id(
            db,
            document_id,
        )

        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found",
            )

        return document

    @staticmethod
    async def get_documents(
        db: AsyncSession,
    ) -> list[Document]:
        return await DocumentRepository.get_all(db)

    @staticmethod
    async def update_document(
        db: AsyncSession,
        document_id: int,
        data: DocumentUpdate,
    ) -> Document:
        document = await DocumentService.get_document(
            db,
            document_id,
        )

        return await DocumentRepository.update(
            db,
            document,
            data,
        )

    @staticmethod
    async def delete_document(
        db: AsyncSession,
        document_id: int,
    ) -> None:
        document = await DocumentService.get_document(
            db,
            document_id,
        )

        await DocumentRepository.delete(
            db,
            document,
        )
