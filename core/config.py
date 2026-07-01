from pydantic import BaseModel


class PostgreSQLConfig(BaseModel):
    dsn: str = "postgresql://rag:rag@localhost:5432/rag"


class QdrantConfig(BaseModel):
    host: str = "localhost"
    port: int = 6333
    collection: str = "library_chunks"
    vector_size: int = 384
    distance: str = "Cosine"


class RedpandaConfig(BaseModel):
    brokers: str = "localhost:19092"
    topic: str = "library-ingestion"


class GroqConfig(BaseModel):
    api_key: str = ""
    model: str = "llama3-70b-8192"
    max_tokens: int = 1024
    temperature: float = 0.3


class EmbedderConfig(BaseModel):
    model_name: str = "BAAI/bge-small-en-v1.5"


class ChunkerConfig(BaseModel):
    chunk_size: int = 512
    chunk_overlap: int = 64


class InferenceConfig(BaseModel):
    top_k: int = 5
    min_score: float = 0.5


class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080
    max_file_size_mb: int = 10


class ServeConfig(BaseModel):
    postgres: PostgreSQLConfig = PostgreSQLConfig()
    qdrant: QdrantConfig = QdrantConfig()
    redpanda: RedpandaConfig = RedpandaConfig()
    groq: GroqConfig = GroqConfig()
    embedder: EmbedderConfig = EmbedderConfig()
    chunker: ChunkerConfig = ChunkerConfig()
    inference: InferenceConfig = InferenceConfig()
    server: ServerConfig = ServerConfig()
