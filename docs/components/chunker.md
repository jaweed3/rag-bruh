# Chunker

Splits document text into chunks for embedding.

## Strategies

### Recursive Split (`app/components/chunker.py:recursive_split`)

Split by `\n\n` → `\n` → `.` → ` ` → char, respecting `chunk_size` and `overlap`.

```
Input:  long document text
Output: [{chunk_id, text, chunk_idx, strategy: "recursive"}, ...]
```

### Semantic Split (`app/components/chunker.py:semantic_split`)

Split sentences by cosine similarity threshold. Same-sentiment sentences stay together.

```
Input:  text, embedder, threshold
Output: [{chunk_id, text, chunk_idx, strategy: "semantic"}, ...]
```

## Config

```yaml
chunker:
  chunk_size: 512
  chunk_overlap: 64
```

Ponytail: recursive is the default for MVP. Semantic added for A/B comparison (Fase 3).
