from fastapi import APIRouter, Depends, Request

from app.dependencies import require_api_key

router = APIRouter(tags=["documents"], dependencies=[Depends(require_api_key)])


@router.get("/documents")
async def list_documents(req: Request) -> dict:
    db = getattr(req.app.state, "database", None)
    retriever = getattr(req.app.state, "retriever", None)
    if db:
        docs = await db.get_all_documents()
    else:
        docs = []
    count = retriever.count() if retriever else 0
    return {"documents": docs, "total_chunks": count}


@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str, req: Request) -> dict:
    retriever = getattr(req.app.state, "retriever", None)
    if retriever:
        retriever.delete_by_doc_id(doc_id)
    return {"doc_id": doc_id, "status": "deleted"}
