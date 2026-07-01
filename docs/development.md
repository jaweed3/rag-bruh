# Development

## Tests

```bash
make test              # all tests
uv run pytest tests/ -v --cov=app --cov=core
```

CI gated: ruff → mypy → pytest. See `.github/workflows/pipeline.yml`.

## Code Style

```bash
make quality            # ruff check + format + mypy
uv run ruff check .
uv run ruff format .
```

Config in `pyproject.toml`: line-length 100, double quotes.

## Adding a New Endpoint

1. Define schema in `app/schema/`
2. Add router in `app/router/`
3. Register in `app/main.py`
4. Add test in `tests/`
5. Update `docs/api/`

## Adding a New Component

Components are pure functions or stateless classes in `app/components/`.
They take config objects and return data — no side effects beyond the
infrastructure layer (Qdrant, Groq, etc).

## CI Pipeline

`.github/workflows/pipeline.yml`:

1. quality (ruff lint + format + mypy)
2. test (pytest + coverage)
3. docker build & push
