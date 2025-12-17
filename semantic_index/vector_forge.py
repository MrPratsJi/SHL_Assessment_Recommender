import json
import os
import faiss
import numpy as np
from semantic_index.embedding_gateway import generate_dense_vectors

CATALOG_PATH = "artifacts/shl_individual_assessments.json"
INDEX_PATH = "semantic_index/index_artifacts/shl_faiss.index"

os.makedirs("semantic_index/index_artifacts", exist_ok=True)

def load_catalog():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def build_index():
    catalog = load_catalog()
    texts = [item["semantic_profile_text"] for item in catalog]
    vectors = generate_dense_vectors(texts)
    dimension = vectors.shape[1]
    index = faiss.IndexFlatIP(dimension)
    faiss.normalize_L2(vectors)
    index.add(vectors)
    faiss.write_index(index, INDEX_PATH)
    return index, catalog

def load_index():
    index = faiss.read_index(INDEX_PATH)
    catalog = load_catalog()
    return index, catalog

def locate_candidates(query_text, top_k=40):
    index, catalog = load_index()
    query_vector = generate_dense_vectors([query_text])
    faiss.normalize_L2(query_vector)
    scores, indices = index.search(query_vector, top_k)
    results = []
    for score, idx in zip(scores[0], indices[0]):
        record = catalog[idx]
        results.append({
            "assessment_id": record["assessment_id"],
            "url": record["url"],
            "name": record["name"],
            "test_types": record["test_types"],
            "semantic_score": float(score)
        })
    return results

if __name__ == "__main__":
    build_index()
    print("FAISS index built and persisted")
