# POST /query

Ask a question. Returns answer + source citations.

## Request

```json
{
  "query": "buku python apa aja yang ada?"
}
```

## Response

```json
{
  "query_id": "uuid",
  "answer": "Berdasarkan koleksi perpustakaan, tersedia 'Python Programming for Beginners' oleh John Smith...",
  "citations": [
    { "title": "Python Programming for Beginners", "chunk_id": "...", "score": 0.89 }
  ]
}
```

## Flow

1. Query → Embedder (384-dim vector)
2. Vector → Qdrant top-k search
3. Results → Generator (Groq) → answer with citation

See [Query Pipeline](../pipeline/query.md).
