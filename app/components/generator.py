from __future__ import annotations

import httpx

from core.config import GroqConfig, NvidiaConfig

SYSTEM_PROMPT = """You are a librarian assistant for a campus library.
Answer based ONLY on the retrieved context below.
If the context doesn't contain the answer, say "I don't have that information."
Cite the document title for each claim."""

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


class Generator:
    def __init__(self, nvidia: NvidiaConfig | None = None, groq: GroqConfig | None = None) -> None:
        if nvidia and nvidia.api_key:
            self.api_key = nvidia.api_key
            self._chat_url = f"{nvidia.base_url}/chat/completions"
            self.model = nvidia.model
            self.max_tokens = nvidia.max_tokens
            self.temperature = nvidia.temperature
        elif groq and groq.api_key:
            self.api_key = groq.api_key
            self._chat_url = "https://api.groq.com/openai/v1/chat/completions"
            self.model = groq.model
            self.max_tokens = groq.max_tokens
            self.temperature = groq.temperature
        else:
            self.api_key = ""
            self._chat_url = ""
            self.model = ""
            self.max_tokens = 0
            self.temperature = 0.0

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def generate(self, query: str, context: list[dict]) -> str:
        context_str = "\n\n".join(f"[{c['title']}] {c['text']}" for c in context)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context_str}\n\nQuestion: {query}"},
        ]
        resp = httpx.post(
            self._chat_url,
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
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
