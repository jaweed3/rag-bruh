from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from core.config import QdrantConfig


class Retriever:
    def __init__(self, cfg: QdrantConfig) -> None:
        self.client = QdrantClient(host=cfg.host, port=cfg.port)
        self.collection = cfg.collection
        self._ensure_collection(cfg)

    def _ensure_collection(self, cfg: QdrantConfig) -> None:
        collections = [c.name for c in self.client.get_collections().collections]
        if cfg.collection not in collections:
            self.client.create_collection(
                collection_name=cfg.collection,
                vectors_config=VectorParams(size=cfg.vector_size, distance=Distance.COSINE),
            )

    def upsert(self, points: list[PointStruct]) -> None:
        self.client.upsert(collection_name=self.collection, points=points)

    def search(self, vector: list[float], top_k: int = 5, min_score: float = 0.0) -> list:
        results = self.client.search(
            collection_name=self.collection,
            query_vector=vector,
            limit=top_k,
            score_threshold=min_score,
        )
        return [
            {
                "chunk_id": r.id,
                "text": r.payload.get("text", ""),
                "doc_id": r.payload.get("doc_id", ""),
                "title": r.payload.get("title", ""),
                "author": r.payload.get("author", ""),
                "source": r.payload.get("source", ""),
                "chunk_idx": r.payload.get("chunk_idx", 0),
                "score": r.score,
            }
            for r in results
        ]

    def delete_by_doc_id(self, doc_id: str) -> None:
        from qdrant_client.models import Filter, FilterSelector, HasIdCondition

        points = self.client.scroll(
            collection_name=self.collection,
            scroll_filter=Filter(must=[HasIdCondition(has_id=[doc_id])]),
            limit=10000,
        )[0]
        if points:
            self.client.delete(
                collection_name=self.collection,
                points_selector=FilterSelector(
                    filter=Filter(must=[HasIdCondition(has_id=[p.id for p in points])])
                ),
            )

    def count(self) -> int:
        return self.client.count(collection_name=self.collection).count
