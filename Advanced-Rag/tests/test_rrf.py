import pytest
from rag.retrieval.hybrid import reciprocal_rank_fusion


def test_rrf_basic():
    """RRF should score documents higher if they appear in both lists."""
    dense = [(1, 0.9), (2, 0.8), (3, 0.7)]
    sparse = [(1, 0.85), (4, 0.75)]

    scores = reciprocal_rank_fusion(dense, sparse)

    # Doc 1 in both lists should score highest
    assert scores[1] > scores[2]
    assert scores[1] > scores[3]
    assert scores[1] > scores[4]


def test_rrf_single_list():
    """RRF should work with documents appearing in only one list."""
    dense = [(1, 0.9), (2, 0.8)]
    sparse = []

    scores = reciprocal_rank_fusion(dense, sparse)

    assert len(scores) == 2
    assert scores[1] > scores[2]


def test_rrf_empty_lists():
    """RRF should handle empty input gracefully."""
    scores = reciprocal_rank_fusion([], [])
    assert len(scores) == 0


def test_rrf_k_parameter():
    """Different k values should affect scores."""
    dense = [(1, 0.9)]
    sparse = [(1, 0.8)]

    scores_k60 = reciprocal_rank_fusion(dense, sparse, k=60)
    scores_k100 = reciprocal_rank_fusion(dense, sparse, k=100)

    # Both should have doc 1, but scores differ
    assert 1 in scores_k60 and 1 in scores_k100
    assert scores_k60[1] != scores_k100[1]
