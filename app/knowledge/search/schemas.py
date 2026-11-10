from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)

    limit: int = Field(
        default=5,
        ge=1,
        le=20,
    )

    score_threshold: float = Field(
        default=0.25,
        ge=0,
        le=1,
    )


class SearchResult(BaseModel):
    chunk_id: int
    document_id: int
    document_title: str
    chunk_index: int
    content: str
    score: float


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
