# Query Pipeline

Question → Embedder → Retriever → Generator → Answer + Citations.

## Flow

```
POST /query {"query": "..."}
  → embedder.embed_one(query)          # 384-dim vector
  → retriever.search(vector, top_k=5)  # Qdrant cosine search
  → generator.generate(query, context) # Groq Llama 3 70B
  → { answer, citations }
```

## Query Result

```json
{
  "query_id": "uuid",
  "answer": "Based on available documents...",
  "citations": [
    { "title": "Python Programming", "chunk_id": "...", "score": 0.92 }
  ]
}
```

## Config

```yaml
inference:
  top_k: 5
  min_score: 0.5
```

## Metrics

| metric | type |
|---|---|
| `rag_retrieval_latency` | Histogram |
| `rag_embedding_latency` | Histogram |
| `rag_generation_latency` | Histogram |
| `rag_queries_total` | Counter (status: success/no_results) |
