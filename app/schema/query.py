from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str


class Citation(BaseModel):
    title: str
    chunk_id: str
    score: float


class QueryResponse(BaseModel):
    query_id: str
    answer: str
    citations: list[Citation]
