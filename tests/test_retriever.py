import uuid

import pytest
from qdrant_client.models import PointStruct

from app.components.retriever import Retriever
from core.config import QdrantConfig


@pytest.fixture
def retriever():
    cfg = QdrantConfig(collection=f"test_{uuid.uuid4().hex[:8]}")
    try:
        r = Retriever(cfg)
    except Exception:
        pytest.skip("Qdrant not available")
        return
    yield r
    try:
        r.client.delete_collection(cfg.collection)
    except Exception:
        pass


def test_search_returns_results(retriever):
    retriever.upsert(
        [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=[0.1] * 384,
                payload={"text": "test doc", "title": "Test"},
            ),
        ]
    )
    results = retriever.search([0.1] * 384, top_k=5, min_score=0.0)
    assert len(results) >= 1
    assert results[0]["text"] == "test doc"
