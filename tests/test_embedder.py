import numpy as np
import pytest

from app.components.embedder import Embedder


@pytest.fixture
def embedder():
    return Embedder()


def test_embedder_returns_float32(embedder):
    vec = embedder.embed_one("Hello world")
    assert isinstance(vec, np.ndarray)
    assert vec.dtype == np.float32


def test_embedder_output_dimension(embedder):
    vec = embedder.embed_one("Hello world")
    assert vec.shape[0] == 384


def test_embedder_batch(embedder):
    vecs = embedder.embed(["Hello", "World"])
    assert vecs.shape == (2, 384)


def test_similar_sentences_have_higher_cosine(embedder):
    v1 = embedder.embed_one("I love programming in Python")
    v2 = embedder.embed_one("Python is my favorite programming language")
    v3 = embedder.embed_one("The weather is nice today")
    sim_same = float(v1 @ v2)
    sim_diff = float(v1 @ v3)
    assert sim_same > sim_diff
