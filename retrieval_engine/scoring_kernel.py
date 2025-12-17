def score_and_rank(candidates):
    return sorted(
        candidates,
        key=lambda x: x["semantic_score"],
        reverse=True
    )
