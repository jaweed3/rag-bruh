# LibraryRAG

RAG pipeline for campus library. Ingest docs → vector search → LLM answer.

```
docker compose up -d
curl -X POST http://localhost:8080/ingest \
  -H "Content-Type: application/json" \
  -d '{"title":"test","text":"hello world"}'
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"query":"hello?"}'
```

**Stack:** FastAPI · Qdrant · PostgreSQL · Redpanda · NVIDIA NIM / Groq · Prometheus · Grafana

`.env` → set `NVIDIA_API_KEY` or `GROQ_API_KEY`.

| Endpoint | What |
|----------|------|
| `GET /health` | liveness |
| `GET /ready` | dep check |
| `POST /ingest` | add doc |
| `POST /query` | ask |
| `GET /documents` | list |
| `GET /metrics` | prom |

```bash
make install-dev   # uv sync + dev deps
make run           # uvicorn :8080
make test          # pytest + coverage
make quality       # ruff + mypy
```
