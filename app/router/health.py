from fastapi import APIRouter, Request

router = APIRouter(tags=["health"])


@router.get("/health")
async def health(req: Request):
    return {"status": "ok"}


@router.get("/ready")
async def ready(req: Request):
    checks = {}
    ok = True

    db = getattr(req.app.state, "database", None)
    if db:
        try:
            c = await db.get_document_count()
            checks["postgres"] = f"connected ({c} docs)"
        except Exception as e:
            checks["postgres"] = f"error: {e}"
            ok = False
    else:
        checks["postgres"] = "not initialized"
        ok = False

    retriever = getattr(req.app.state, "retriever", None)
    if retriever:
        try:
            n = retriever.count()
            checks["qdrant"] = f"connected ({n} points)"
        except Exception as e:
            checks["qdrant"] = f"error: {e}"
            ok = False
    else:
        checks["qdrant"] = "not initialized"
        ok = False

    gen = getattr(req.app.state, "generation", None)
    if gen and gen.available:
        checks["llm"] = gen.model
    else:
        checks["llm"] = "not configured"

    return {"status": "ready" if ok else "degraded", "checks": checks}
