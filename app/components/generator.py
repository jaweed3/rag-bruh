from __future__ import annotations

import httpx

from core.config import GroqConfig

SYSTEM_PROMPT = """You are a librarian assistant for a campus library.
Answer based ONLY on the retrieved context below.
If the context doesn't contain the answer, say "I don't have that information."
Cite the document title for each claim."""


class Generator:
    def __init__(self, cfg: GroqConfig) -> None:
        self.api_key = cfg.api_key
        self.model = cfg.model
        self.max_tokens = cfg.max_tokens
        self.temperature = cfg.temperature

    def generate(self, query: str, context: list[dict]) -> str:
        context_str = "\n\n".join(f"[{c['title']}] {c['text']}" for c in context)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context_str}\n\nQuestion: {query}"},
        ]
        resp = httpx.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
            },
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
