# Architecture

```
Data Sources ──► Redpanda ──► Chunker ──► Embedder ──► Qdrant
                    │                                         │
                    │                              ┌──────────┘
                    ▼                              ▼
            PostgreSQL (metadata)        Query API (FastAPI)
                                                │
                                        ┌───────┴───────┐
                                        ▼               ▼
                                    Retriever       Reranker
                                        │               │
                                        └───────┬───────┘
                                                ▼
                                            Generator (Groq)
                                                │
                                                ▼
                                        Response + Citations

Observability: Prometheus + Grafana
```

## Components

| Component | Role |
|---|---|
| **Redpanda** | Kafka-compatible message queue for streaming ingestion |
| **Chunker** | Splits documents into chunks (recursive + semantic) |
| **Embedder** | ONNX MiniLM via fastembed, 384-dim vectors |
| **Qdrant** | Vector DB — cosine similarity search |
| **PostgreSQL** | Metadata store (docs, chunks, queries, feedback) |
| **Retriever** | Qdrant search wrapper |
| **Generator** | Groq API (Llama 3 70B) — context-aware answer |
| **Reranker** | (optional) Cohere rerank |
