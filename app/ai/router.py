from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.rag_service import RAGService
from app.ai.schemas import RAGRequest, RAGResponse
from app.db.session import get_db

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/answer",
    response_model=RAGResponse,
)
async def answer_question(
    data: RAGRequest,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
) -> RAGResponse:
    return await RAGService.answer(
        db=db,
        question=data.question,
    )
