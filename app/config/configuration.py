import os
from pathlib import Path

import yaml

from app.constant import CONFIG_FILE_PATH
from core.config import (
    ChunkerConfig,
    EmbedderConfig,
    GroqConfig,
    InferenceConfig,
    NvidiaConfig,
    PostgreSQLConfig,
    QdrantConfig,
    RedpandaConfig,
    ServeConfig,
    ServerConfig,
)


class ConfigurationManager:
    def __init__(self, config_path: Path = CONFIG_FILE_PATH) -> None:
        raw = self._load(config_path)
        self._cfg = ServeConfig(**raw)
        self._cfg.nvidia = self._nvidia_with_env_overlay(self._cfg.nvidia)
        self._cfg.groq = self._groq_with_env_overlay(self._cfg.groq)
        self._cfg.postgres = self._pg_with_env_overlay(self._cfg.postgres)
        self._cfg.qdrant = self._qdrant_with_env_overlay(self._cfg.qdrant)
        self._cfg.redpanda = self._rp_with_env_overlay(self._cfg.redpanda)

    @staticmethod
    def _load(path: Path) -> dict:
        if not path.exists():
            raise FileNotFoundError(f"Serve config not found: {path}")
        return yaml.safe_load(path.read_text())

    @staticmethod
    def _nvidia_with_env_overlay(cfg: NvidiaConfig) -> NvidiaConfig:
        return NvidiaConfig(
            api_key=os.environ.get("NVIDIA_API_KEY", cfg.api_key),
            model=os.environ.get("NVIDIA_MODEL", cfg.model),
            base_url=os.environ.get("NVIDIA_BASE_URL", cfg.base_url),
            max_tokens=int(os.environ.get("NVIDIA_MAX_TOKENS", cfg.max_tokens)),
            temperature=float(os.environ.get("NVIDIA_TEMPERATURE", cfg.temperature)),
        )

    @staticmethod
    def _groq_with_env_overlay(cfg: GroqConfig) -> GroqConfig:
        return GroqConfig(
            api_key=os.environ.get("GROQ_API_KEY", cfg.api_key),
            model=os.environ.get("GROQ_MODEL", cfg.model),
            max_tokens=int(os.environ.get("GROQ_MAX_TOKENS", cfg.max_tokens)),
            temperature=float(os.environ.get("GROQ_TEMPERATURE", cfg.temperature)),
        )

    @staticmethod
    def _pg_with_env_overlay(cfg: PostgreSQLConfig) -> PostgreSQLConfig:
        return PostgreSQLConfig(
            dsn=os.environ.get("POSTGRES_DSN", cfg.dsn),
        )

    @staticmethod
    def _qdrant_with_env_overlay(cfg: QdrantConfig) -> QdrantConfig:
        return QdrantConfig(
            host=os.environ.get("QDRANT_HOST", cfg.host),
            port=int(os.environ.get("QDRANT_PORT", cfg.port)),
            collection=os.environ.get("QDRANT_COLLECTION", cfg.collection),
        )

    @staticmethod
    def _rp_with_env_overlay(cfg: RedpandaConfig) -> RedpandaConfig:
        return RedpandaConfig(
            brokers=os.environ.get("REDPANDA_BROKERS", cfg.brokers),
            topic=os.environ.get("REDPANDA_TOPIC", cfg.topic),
        )

    def get_postgres_config(self) -> PostgreSQLConfig:
        return self._cfg.postgres

    def get_qdrant_config(self) -> QdrantConfig:
        return self._cfg.qdrant

    def get_redpanda_config(self) -> RedpandaConfig:
        return self._cfg.redpanda

    def get_nvidia_config(self) -> NvidiaConfig:
        return self._cfg.nvidia

    def get_groq_config(self) -> GroqConfig:
        return self._cfg.groq

    def get_embedder_config(self) -> EmbedderConfig:
        return self._cfg.embedder

    def get_chunker_config(self) -> ChunkerConfig:
        return self._cfg.chunker

    def get_inference_config(self) -> InferenceConfig:
        return self._cfg.inference

    def get_server_config(self) -> ServerConfig:
        return self._cfg.server
