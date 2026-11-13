from pydantic import BaseModel, Field


class RAGRequest(BaseModel):
    question: str = Field(min_length=1)


class RAGSource(BaseModel):
    citation: str

    chunk_id: int
    document_id: int
    document_title: str
    chunk_index: int

    relevance_score: float


class RAGResponse(BaseModel):
    question: str
    answer: str
    sources: list[RAGSource]
