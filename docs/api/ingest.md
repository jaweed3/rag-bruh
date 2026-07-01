# POST /ingest

Upload a document for indexing.

## Request

```json
{
  "title": "Python Programming for Beginners",
  "author": "John Smith",
  "source": "library-catalog",
  "text": "Python is a high-level, interpreted programming language..."
}
```

## Response

```json
{
  "doc_id": "uuid",
  "chunks": 12,
  "message": "Indexed 12 chunks"
}
```

## Flow

1. Document → Redpanda topic
2. Consumer → recursive chunker → embedder → Qdrant upsert
3. Metadata → PostgreSQL

See [Ingestion Pipeline](../pipeline/ingestion.md).
