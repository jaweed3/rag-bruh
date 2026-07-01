from prometheus_client import Counter, Gauge, Histogram

retrieval_latency = Histogram(
    "rag_retrieval_latency_seconds",
    "Retrieval latency",
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0),
)
embedding_latency = Histogram(
    "rag_embedding_latency_seconds",
    "Embedding latency",
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0),
)
generation_latency = Histogram(
    "rag_generation_latency_seconds",
    "LLM generation latency",
    buckets=(0.5, 1.0, 2.0, 5.0, 10.0),
)
query_total = Counter("rag_queries_total", "Total number of queries", ["status"])
chunks_indexed = Gauge("rag_chunks_indexed_total", "Total chunks in vector store")
indexed_documents = Gauge("rag_documents_indexed_total", "Total documents indexed")
http_requests_total = Counter(
    "rag_http_requests_total", "Total HTTP requests", ["method", "path", "status"]
)
