CREATE TABLE IF NOT EXISTS documents (
    doc_id UUID PRIMARY KEY,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    author TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT now(),
    total_chunks INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS chunks (
    chunk_id UUID PRIMARY KEY,
    doc_id UUID REFERENCES documents(doc_id) ON DELETE CASCADE,
    chunk_idx INT NOT NULL,
    text TEXT NOT NULL,
    strategy TEXT DEFAULT 'recursive'
);

CREATE TABLE IF NOT EXISTS queries (
    query_id UUID PRIMARY KEY,
    query_text TEXT NOT NULL,
    retrieved_chunks TEXT[] DEFAULT '{}',
    response TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS feedback (
    query_id UUID REFERENCES queries(query_id) ON DELETE CASCADE,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    corrected_response TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT now()
);
