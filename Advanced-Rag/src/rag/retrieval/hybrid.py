from typing import TypedDict


class RankedDocument(TypedDict):
    id: int
    score: float
    content: str
    metadata: dict


def reciprocal_rank_fusion(
    dense_results: list[tuple[int, float]],
    sparse_results: list[tuple[int, float]],
    k: int = 60,
) -> dict[int, float]:
    """Combine dense and sparse results using RRF (Reciprocal Rank Fusion).

    Args:
        dense_results: list of (doc_id, score) from dense retrieval
        sparse_results: list of (doc_id, score) from sparse retrieval
        k: constant for RRF formula (default 60)

    Returns:
        dict mapping doc_id to RRF score
    """
    rrf_scores: dict[int, float] = {}

    # Process dense results
    for rank, (doc_id, _) in enumerate(dense_results, start=1):
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1 / (k + rank)

    # Process sparse results
    for rank, (doc_id, _) in enumerate(sparse_results, start=1):
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1 / (k + rank)

    return rrf_scores


def merge_results(dense_results: list[dict], sparse_results: list[dict]) -> list[dict]:
    """Merge and rank dense + sparse results using RRF."""
    dense_tuples = [(r["id"], r.get("score", 0)) for r in dense_results]
    sparse_tuples = [(r["id"], r.get("score", 0)) for r in sparse_results]

    rrf_scores = reciprocal_rank_fusion(dense_tuples, sparse_tuples)

    # Reconstruct with RRF scores
    merged = {}
    for result in dense_results + sparse_results:
        doc_id = result["id"]
        if doc_id not in merged:
            merged[doc_id] = result
        merged[doc_id]["rrf_score"] = rrf_scores.get(doc_id, 0)

    # Sort by RRF score
    sorted_results = sorted(merged.values(), key=lambda x: x["rrf_score"], reverse=True)
    return sorted_results
