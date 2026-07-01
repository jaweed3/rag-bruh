# Ingestion Pipeline

Document → Redpanda → Chunker → Embedder → Qdrant + PostgreSQL.

## Sync Flow (via API)

```
POST /ingest
  → IngestionPipeline.process_document()
    → recursive_split(text, chunk_size, overlap)
    → embedder.embed(texts)
    → retriever.upsert(PointStruct[])
    → PostgreSQL (metadata)
```

## Async Flow (via Redpanda Consumer)

```
Redpanda topic "library-ingestion"
  → AIOKafkaConsumer (background task)
    → process_document() for each message
```

## Redpanda Message

```json
{
  "doc_id": "uuid",
  "title": "Title",
  "author": "Author",
  "source": "webhook",
  "text": "full document text"
}
```

## Config

```yaml
redpanda:
  brokers: localhost:19092
  topic: library-ingestion

chunker:
  chunk_size: 512
  chunk_overlap: 64
```
