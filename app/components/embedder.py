from __future__ import annotations

import time

import numpy as np
from fastembed import TextEmbedding

from app.components.metrics import embedding_latency
from core.logger import get_logger

log = get_logger("embedder")


class Embedder:
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5") -> None:
        self.model = TextEmbedding(model_name=model_name, max_length=256)
        log.info("embedder_loaded: %s", model_name)

    def embed(self, texts: list[str]) -> np.ndarray:
        t0 = time.perf_counter()
        result = np.array(list(self.model.embed(texts)), dtype=np.float32)
        embedding_latency.observe(time.perf_counter() - t0)
        return result

    def embed_one(self, text: str) -> np.ndarray:
        return self.embed([text])[0]
