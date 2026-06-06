"""Tests for VecDB benchmark runner"""
import numpy as np
import pytest

def test_generate_vectors_unit_norm():
    from src.benchmarks.run import generate_vectors
    vecs = generate_vectors(100, dim=64)
    norms = np.linalg.norm(vecs, axis=1)
    np.testing.assert_allclose(norms, 1.0, atol=1e-5)

def test_generate_vectors_shape():
    from src.benchmarks.run import generate_vectors
    vecs = generate_vectors(500, dim=128)
    assert vecs.shape == (500, 128)
