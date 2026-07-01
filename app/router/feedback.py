from fastapi import APIRouter, Depends, Request

from app.dependencies import require_api_key
from app.schema.feedback import FeedbackRequest

router = APIRouter(tags=["feedback"], dependencies=[Depends(require_api_key)])


@router.post("/feedback")
async def feedback(request: FeedbackRequest, req: Request) -> dict:
    db = getattr(req.app.state, "database", None)
    if db:
        await db.save_feedback(request.query_id, request.rating, request.corrected_response)
    return {"status": "received"}
