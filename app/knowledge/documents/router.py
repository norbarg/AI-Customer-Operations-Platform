from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.knowledge.documents.chunk_repository import DocumentChunkRepository
from app.knowledge.documents.chunk_service import DocumentChunkService
from app.knowledge.documents.indexing_service import DocumentIndexingService
from app.knowledge.documents.schemas import (
    DocumentChunkResponse,
    DocumentCreate,
    DocumentResponse,
    DocumentUpdate,
)
from app.knowledge.documents.service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_document(
    data: DocumentCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DocumentResponse:
    return await DocumentService.create_document(db, data)


@router.get(
    "",
    response_model=list[DocumentResponse],
)
async def get_documents(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[DocumentResponse]:
    return await DocumentService.get_documents(db)


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
async def get_document(
    document_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DocumentResponse:
    return await DocumentService.get_document(db, document_id)


@router.patch(
    "/{document_id}",
    response_model=DocumentResponse,
)
async def update_document(
    document_id: int,
    data: DocumentUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DocumentResponse:
    return await DocumentService.update_document(
        db,
        document_id,
        data,
    )


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_document(
    document_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    await DocumentService.delete_document(
        db,
        document_id,
    )


@router.post(
    "/{document_id}/chunk",
    response_model=list[DocumentChunkResponse],
)
async def chunk_document(
    document_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[DocumentChunkResponse]:
    return await DocumentChunkService.process_document(
        db,
        document_id,
    )


@router.get(
    "/{document_id}/chunks",
    response_model=list[DocumentChunkResponse],
)
async def get_document_chunks(
    document_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[DocumentChunkResponse]:
    await DocumentService.get_document(
        db,
        document_id,
    )

    return await DocumentChunkRepository.get_by_document_id(
        db,
        document_id,
    )


@router.post(
    "/{document_id}/index",
)
async def index_document(
    document_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, int]:
    indexed_chunks = await DocumentIndexingService.index_document(
        db,
        document_id,
    )

    return {
        "indexed_chunks": indexed_chunks,
    }
