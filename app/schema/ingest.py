from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(default="", max_length=200)
    source: str = Field(default="api", max_length=100)
    text: str = Field(..., min_length=1, max_length=500_000)


class IngestResponse(BaseModel):
    doc_id: str
    chunks: int
    message: str
