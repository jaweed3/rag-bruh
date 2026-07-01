# Setup

## Prerequisites

- Python >= 3.10
- Docker + Docker Compose
- [uv](https://docs.astral.sh/uv/)
- Groq API key ([groq.com](https://groq.com))

## Quick Start

```bash
git clone <repo> && cd library-rag
cp .env.example .env   # edit GROQ_API_KEY

# install + run infra
make install-dev
docker compose up -d       # redpanda, qdrant, postgres, prometheus, grafana

# run app
make run                   # uvicorn --reload :8080

# seed sample data
make seed
```

## Makefile

| target | what |
|---|---|
| `install-dev` | uv sync (dev group) |
| `run` | uvicorn --reload |
| `up` / `down` | docker compose |
| `test` | pytest + coverage |
| `quality` | ruff + mypy |
| `seed` | seed sample documents |
| `build` | docker build |
