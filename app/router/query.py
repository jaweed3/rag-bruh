from fastapi import APIRouter, Depends, HTTPException, Request

from app.dependencies import require_api_key
from app.schema.query import QueryRequest, QueryResponse

router = APIRouter(tags=["query"], dependencies=[Depends(require_api_key)])


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest, req: Request) -> QueryResponse:
    pipeline = getattr(req.app.state, "query", None)
    if pipeline is None:
        raise HTTPException(503, "Query service not available (GROQ_API_KEY missing)")
    result = await pipeline.run(request.query)
    return QueryResponse(**result)
