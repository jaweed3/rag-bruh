# Config

Single source: `configs/serve_config.yaml`, overlaid by env vars.

## Reference

```yaml
postgres:
  dsn: "postgresql://rag:rag@localhost:5432/rag"

qdrant:
  host: localhost
  port: 6333
  collection: library_chunks
  vector_size: 384
  distance: Cosine

redpanda:
  brokers: localhost:19092
  topic: library-ingestion

groq:
  api_key: ""           # or GROQ_API_KEY env
  model: llama3-70b-8192
  max_tokens: 1024
  temperature: 0.3

embedder:
  model_name: BAAI/bge-small-en-v1.5

chunker:
  chunk_size: 512
  chunk_overlap: 64

inference:
  top_k: 5
  min_score: 0.5

server:
  host: 0.0.0.0
  port: 8080
  max_file_size_mb: 10
```

## Env Overrides

| env | overrides |
|---|---|
| `GROQ_API_KEY` | groq.api_key |
| `GROQ_MODEL` | groq.model |
| `QDRANT_HOST` | qdrant.host |
| `QDRANT_PORT` | qdrant.port |
| `POSTGRES_DSN` | postgres.dsn |
| `REDPANDA_BROKERS` | redpanda.brokers |
| `API_KEY` | auth (empty = no auth) |
