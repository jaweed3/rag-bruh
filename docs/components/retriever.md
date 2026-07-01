# Retriever

Qdrant vector search wrapper.

## Setup

Collection auto-created on first use with 384-dim Cosine vectors.

## Methods

| method | what |
|---|---|
| `search(vector, top_k, min_score)` | Returns `[{chunk_id, text, title, author, source, score}]` |
| `upsert(points)` | Batch insert PointStruct |
| `delete_by_doc_id(doc_id)` | Delete all chunks for a doc |
| `count()` | Total indexed chunks |

## Config

```yaml
qdrant:
  host: localhost
  port: 6333
  collection: library_chunks
```
