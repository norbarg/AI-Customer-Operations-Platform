from fastapi import APIRouter

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
async def semantic_search(
    data: SearchRequest,
) -> SearchResponse:
    results = await SearchService.search(
        query=data.query,
        limit=data.limit,
        score_threshold=data.score_threshold,
    )

    return SearchResponse(
        query=data.query,
        results=results,
    )
