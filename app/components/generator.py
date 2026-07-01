from __future__ import annotations

import time

import httpx

from core.config import GroqConfig, NvidiaConfig
from core.logger import get_logger

log = get_logger("generator")

SYSTEM_PROMPT = """You are a librarian assistant for a campus library.
Answer based ONLY on the retrieved context below.
If the context doesn't contain the answer, say "I don't have that information."
Cite the document title for each claim."""

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MAX_RETRIES = 3


class Generator:
    def __init__(self, nvidia: NvidiaConfig | None = None, groq: GroqConfig | None = None) -> None:
        self._fallback = None
        if nvidia and nvidia.api_key:
            self.api_key = nvidia.api_key
            self._chat_url = f"{nvidia.base_url}/chat/completions"
            self.model = nvidia.model
            self.max_tokens = nvidia.max_tokens
            self.temperature = nvidia.temperature
            if groq and groq.api_key:
                self._fallback = Generator(nvidia=None, groq=groq)
                log.info("nvidia_fallback_groq_ready")
        elif groq and groq.api_key:
            self.api_key = groq.api_key
            self._chat_url = GROQ_URL
            self.model = groq.model
            self.max_tokens = groq.max_tokens
            self.temperature = groq.temperature
        else:
            self.api_key = ""
            self._chat_url = ""
            self.model = ""
            self.max_tokens = 0
            self.temperature = 0.0
        if self.api_key:
            log.info("generator_ready: %s", self.model)

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def generate(self, query: str, context: list[dict]) -> str:
        context_str = "\n\n".join(f"[{c['title']}] {c['text']}" for c in context)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context_str}\n\nQuestion: {query}"},
        ]
        return self._call_with_retry(messages)

    def _call_with_retry(self, messages: list[dict], attempt: int = 1) -> str:
        try:
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
                timeout=120,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except httpx.TimeoutException:
            log.warning("llm_timeout attempt=%d/%d", attempt, MAX_RETRIES)
        except httpx.HTTPStatusError as e:
            log.warning("llm_http_error attempt=%d/%d: %s", attempt, MAX_RETRIES, e)
        except Exception as e:
            log.error("llm_error attempt=%d/%d: %s", attempt, MAX_RETRIES, e)

        if attempt < MAX_RETRIES:
            time.sleep(2**attempt)
            return self._call_with_retry(messages, attempt + 1)

        if self._fallback:
            log.info("llm_fallback_to_groq")
            return self._fallback._call_with_retry(messages)

        return "I'm sorry, I couldn't generate an answer right now. Please try again later."
