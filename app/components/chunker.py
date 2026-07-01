from __future__ import annotations

import uuid
from typing import Any


def recursive_split(text: str, chunk_size: int = 512, overlap: int = 64) -> list[dict[str, Any]]:
    separators = ["\n\n", "\n", ".", " ", ""]
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        if end < n:
            for sep in separators:
                idx = text.rfind(sep, start + 1, end)
                if idx != -1:
                    end = idx + len(sep)
                    break
        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append(
                {
                    "chunk_id": str(uuid.uuid4()),
                    "text": chunk_text,
                    "chunk_idx": len(chunks),
                    "strategy": "recursive",
                }
            )
        if end >= n:
            break
        start = end - overlap
    return chunks


def semantic_split(text: str, embedder: Any, threshold: float = 0.7) -> list[dict[str, Any]]:
    sentences = [s.strip() for s in text.replace("\n", " ").split(". ") if s.strip()]
    if not sentences:
        return []
    chunks = []
    current = [sentences[0]]
    current_emb = embedder.embed([sentences[0]])[0]
    for sent in sentences[1:]:
        sent_emb = embedder.embed([sent])[0]
        sim = float(current_emb @ sent_emb)
        if sim >= threshold:
            current.append(sent)
        else:
            chunks.append(
                {
                    "chunk_id": str(uuid.uuid4()),
                    "text": ". ".join(current) + ".",
                    "chunk_idx": len(chunks),
                    "strategy": "semantic",
                }
            )
            current = [sent]
            current_emb = sent_emb
    if current:
        chunks.append(
            {
                "chunk_id": str(uuid.uuid4()),
                "text": ". ".join(current) + ".",
                "chunk_idx": len(chunks),
                "strategy": "semantic",
            }
        )
    return chunks
