from __future__ import annotations

import asyncpg

from core.config import PostgreSQLConfig
from core.logger import get_logger

log = get_logger("database")


class Database:
    def __init__(self, cfg: PostgreSQLConfig) -> None:
        self._dsn = cfg.dsn
        self._pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        self._pool = await asyncpg.create_pool(self._dsn, min_size=1, max_size=4)
        log.info("postgres_pool_ready")

    async def close(self) -> None:
        if self._pool:
            await self._pool.close()

    async def save_document(
        self, doc_id: str, source: str, title: str, author: str, total_chunks: int
    ) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO documents (doc_id, source, title, author, total_chunks) "
                "VALUES ($1, $2, $3, $4, $5) ON CONFLICT (doc_id) DO NOTHING",
                doc_id,
                source,
                title,
                author,
                total_chunks,
            )

    async def save_chunks(
        self,
        chunks: list[dict],
    ) -> None:
        async with self._pool.acquire() as conn:
            await conn.executemany(
                "INSERT INTO chunks (chunk_id, doc_id, chunk_idx, text) "
                "VALUES ($1, $2, $3, $4) ON CONFLICT (chunk_id) DO NOTHING",
                [(c["chunk_id"], c["doc_id"], c["chunk_idx"], c["text"]) for c in chunks],
            )

    async def save_query(
        self, query_id: str, query_text: str, retrieved: list[str], response: str
    ) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO queries (query_id, query_text, retrieved_chunks, response) "
                "VALUES ($1, $2, $3, $4)",
                query_id,
                query_text,
                retrieved,
                response,
            )

    async def save_feedback(self, query_id: str, rating: int, corrected_response: str) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO feedback (query_id, rating, corrected_response) VALUES ($1, $2, $3)",
                query_id,
                rating,
                corrected_response,
            )

    async def get_document_count(self) -> int:
        async with self._pool.acquire() as conn:
            row = await conn.fetchval("SELECT COUNT(*) FROM documents")
            return row or 0

    async def get_all_documents(self) -> list[dict]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM documents ORDER BY created_at DESC")
            return [dict(r) for r in rows]
