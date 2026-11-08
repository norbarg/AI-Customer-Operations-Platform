from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.documents.models import Document
from app.documents.schemas import DocumentCreate, DocumentUpdate


class DocumentRepository:
    @staticmethod
    async def create(
        db: AsyncSession,
        data: DocumentCreate,
    ) -> Document:
        document = Document(
            title=data.title,
            source=data.source,
            file_name=data.file_name,
            mime_type=data.mime_type,
            content=data.content,
        )

        db.add(document)
        await db.commit()
        await db.refresh(document)

        return document

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        document_id: int,
    ) -> Document | None:
        result = await db.execute(select(Document).where(Document.id == document_id))

        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ) -> list[Document]:
        result = await db.execute(select(Document).order_by(Document.id))

        return list(result.scalars().all())

    @staticmethod
    async def update(
        db: AsyncSession,
        document: Document,
        data: DocumentUpdate,
    ) -> Document:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(document, field, value)

        await db.commit()
        await db.refresh(document)

        return document

    @staticmethod
    async def delete(
        db: AsyncSession,
        document: Document,
    ) -> None:
        await db.delete(document)
        await db.commit()
