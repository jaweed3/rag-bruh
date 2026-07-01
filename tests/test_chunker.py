from app.components.chunker import recursive_split


def test_recursive_split_returns_chunks():
    text = "Hello world. This is a test. " * 50
    chunks = recursive_split(text, chunk_size=100, overlap=10)
    assert len(chunks) > 1
    assert all(c["strategy"] == "recursive" for c in chunks)
    assert all(c["text"] for c in chunks)


def test_recursive_split_single_chunk():
    text = "Short text."
    chunks = recursive_split(text, chunk_size=500, overlap=10)
    assert len(chunks) == 1


def test_recursive_split_respects_order():
    text = "First. Second. Third."
    chunks = recursive_split(text, chunk_size=500, overlap=10)
    assert chunks[0]["chunk_idx"] == 0
