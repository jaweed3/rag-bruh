from app.schema.query import Citation, QueryRequest, QueryResponse


def test_query_request_model():
    req = QueryRequest(query="test query")
    assert req.query == "test query"


def test_query_response_model():
    resp = QueryResponse(
        query_id="123",
        answer="test answer",
        citations=[Citation(title="Doc1", chunk_id="c1", score=0.9)],
    )
    assert resp.answer == "test answer"
    assert len(resp.citations) == 1
