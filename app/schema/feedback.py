from pydantic import BaseModel


class FeedbackRequest(BaseModel):
    query_id: str
    rating: int
    corrected_response: str = ""
