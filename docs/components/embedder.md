# Embedder

ONNX embedding via `fastembed` — no PyTorch, no GPU needed.

## Model

`BAAI/bge-small-en-v1.5` → 384-dim vectors, ~250 docs/sec on CPU.

Downloads once on first use (~70 MB), cached locally.

## Usage

```python
embedder = Embedder()
vec = embedder.embed_one("hello world")       # np.ndarray (384,)
vecs = embedder.embed(["hello", "world"])      # np.ndarray (2, 384)
```

## Why ONNX

| vs PyTorch | vs API |
|---|---|
| 80 MB vs 500+ MB | No latency |
| No GPU needed | No rate limit |
| 250 docs/sec | No cost |
