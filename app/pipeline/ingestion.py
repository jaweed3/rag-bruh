from __future__ import annotations

import json
import uuid

from qdrant_client.models import PointStruct

from app.components.chunker import recursive_split
from app.components.database import Database
from app.components.embedder import Embedder
from app.components.metrics import chunks_indexed, indexed_documents
from app.components.retriever import Retriever
from core.config import ChunkerConfig, RedpandaConfig
from core.logger import get_logger

log = get_logger("ingestion")


class IngestionPipeline:
    def __init__(
        self,
        embedder: Embedder,
        retriever: Retriever,
        database: Database,
        rp_cfg: RedpandaConfig,
        chunker_cfg: ChunkerConfig,
    ) -> None:
        self.embedder = embedder
        self.retriever = retriever
        self.database = database
        self.rp_cfg = rp_cfg
        self.chunker_cfg = chunker_cfg

    async def process_document(
        self,
        doc_id: str,
        title: str,
        author: str,
        source: str,
        text: str,
    ) -> int:
        chunks = recursive_split(text, self.chunker_cfg.chunk_size, self.chunker_cfg.chunk_overlap)
        texts = [c["text"] for c in chunks]
        vectors = self.embedder.embed(texts)
        points = []
        db_chunks = []
        for i, chunk in enumerate(chunks):
            chunk_id = str(uuid.uuid4())
            points.append(
                PointStruct(
                    id=chunk_id,
                    vector=vectors[i].tolist(),
                    payload={
                        "chunk_id": chunk_id,
                        "doc_id": doc_id,
                        "title": title,
                        "author": author,
                        "source": source,
                        "chunk_idx": i,
                        "text": chunk["text"],
                    },
                )
            )
            db_chunks.append(
                {
                    "chunk_id": chunk_id,
                    "doc_id": doc_id,
                    "chunk_idx": i,
                    "text": chunk["text"],
                }
            )
        self.retriever.upsert(points)
        await self.database.save_document(doc_id, source, title, author, len(chunks))
        await self.database.save_chunks(db_chunks)
        chunks_indexed.set(self.retriever.count())
        indexed_documents.inc()
        log.info("document_indexed: %s (%d chunks)", doc_id, len(chunks))
        return len(chunks)

    async def run_consumer(self) -> None:
        try:
            from aiokafka import AIOKafkaConsumer
        except ImportError:
            log.warning("aiokafka not installed; consumer disabled")
            return

        consumer = AIOKafkaConsumer(
            self.rp_cfg.topic,
            bootstrap_servers=self.rp_cfg.brokers,
            group_id="library-rag-ingestion",
            value_deserializer=lambda v: json.loads(v.decode()),
        )
        await consumer.start()
        try:
            async for msg in consumer:
                data = msg.value
                await self.process_document(
                    doc_id=data.get("doc_id", str(uuid.uuid4())),
                    title=data.get("title", "Untitled"),
                    author=data.get("author", ""),
                    source=data.get("source", "webhook"),
                    text=data.get("text", ""),
                )
        finally:
            await consumer.stop()
