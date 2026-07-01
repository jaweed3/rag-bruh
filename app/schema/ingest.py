from pydantic import BaseModel


class IngestRequest(BaseModel):
    title: str
    author: str = ""
    source: str = "api"
    text: str


class IngestResponse(BaseModel):
    doc_id: str
    chunks: int
    message: str
