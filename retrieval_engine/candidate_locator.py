from semantic_index.vector_forge import locate_candidates

def fetch_candidates(query, top_k=30):
    return locate_candidates(query, top_k=top_k)
