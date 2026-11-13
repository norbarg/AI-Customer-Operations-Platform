from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.knowledge.search.schemas import (
    SearchRequest,
    SearchResponse,
)
from app.knowledge.search.service import SearchService

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.post(
    "",
    response_model=SearchResponse,
)
async def search(
    data: SearchRequest,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
) -> SearchResponse:
    results = await SearchService.search(
        db=db,
        query=data.query,
        limit=data.limit,
        score_threshold=data.score_threshold,
    )

    return SearchResponse(
        query=data.query,
        results=results,
    )
