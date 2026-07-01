import uuid

from fastapi import APIRouter, Depends, Request

from app.dependencies import require_api_key
from app.schema.ingest import IngestRequest, IngestResponse

router = APIRouter(tags=["ingest"], dependencies=[Depends(require_api_key)])


@router.post("/ingest", response_model=IngestResponse)
async def ingest(request: IngestRequest, req: Request) -> IngestResponse:
    pipeline = getattr(req.app.state, "ingestion", None)
    if pipeline is None:
        return IngestResponse(
            doc_id="",
            chunks=0,
            message="Ingestion not initialized",
        )
    doc_id = str(uuid.uuid4())
    n = await pipeline.process_document(
        doc_id=doc_id,
        title=request.title,
        author=request.author,
        source=request.source,
        text=request.text,
    )
    return IngestResponse(
        doc_id=doc_id,
        chunks=n,
        message=f"Indexed {n} chunks",
    )
