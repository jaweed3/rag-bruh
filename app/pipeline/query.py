from __future__ import annotations

import time
import uuid

from app.components.database import Database
from app.components.embedder import Embedder
from app.components.generator import Generator
from app.components.metrics import generation_latency, query_total, retrieval_latency
from app.components.retriever import Retriever
from core.config import InferenceConfig
from core.logger import get_logger

log = get_logger("query")


class QueryPipeline:
    def __init__(
        self,
        embedder: Embedder,
        retriever: Retriever,
        database: Database,
        generator: Generator,
        inf_cfg: InferenceConfig,
    ) -> None:
        self.embedder = embedder
        self.retriever = retriever
        self.database = database
        self.generator = generator
        self.inf_cfg = inf_cfg

    async def run(self, query: str) -> dict:
        query_id = str(uuid.uuid4())
        t0 = time.perf_counter()
        vec = self.embedder.embed_one(query)
        retrieval_latency.observe(time.perf_counter() - t0)

        t1 = time.perf_counter()
        results = self.retriever.search(
            vec.tolist(),
            top_k=self.inf_cfg.top_k,
            min_score=self.inf_cfg.min_score,
        )
        retrieval_latency.observe(time.perf_counter() - t1)

        if not results:
            query_total.labels(status="no_results").inc()
            await self.database.save_query(query_id, query, [], "")
            return {
                "query_id": query_id,
                "answer": "I don't have that information.",
                "citations": [],
            }

        t2 = time.perf_counter()
        answer = self.generator.generate(query, results)
        generation_latency.observe(time.perf_counter() - t2)

        citations = [
            {"title": r["title"], "chunk_id": r["chunk_id"], "score": round(r["score"], 3)}
            for r in results
        ]

        retrieved_ids = [c["chunk_id"] for c in citations]
        await self.database.save_query(query_id, query, retrieved_ids, answer)

        query_total.labels(status="success").inc()
        log.info("query_complete: %d results", len(results))

        return {
            "query_id": query_id,
            "answer": answer,
            "citations": citations,
        }
