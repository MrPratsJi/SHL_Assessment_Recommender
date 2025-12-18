from semantic_index.vector_forge import load_index
from semantic_index.embedding_gateway import generate_dense_vectors

_index, _meta = load_index()

def fetch_candidates(query, top_k=30):
    query_vec = generate_dense_vectors([query])[0]
    D, I = _index.search(query_vec.reshape(1, -1), top_k)

    results = []
    for score, idx in zip(D[0], I[0]):
        candidate = dict(_meta[idx])
        candidate["semantic_score"] = float(score)
        results.append(candidate)

    return results
