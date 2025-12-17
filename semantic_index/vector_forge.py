import os
import faiss
import json
from semantic_index.embedding_gateway import generate_dense_vectors

INDEX_DIR = "semantic_index/index_artifacts"
INDEX_PATH = os.path.join(INDEX_DIR, "shl_faiss.index")
META_PATH = os.path.join(INDEX_DIR, "shl_meta.json")
CATALOG_PATH = "artifacts/shl_individual_assessments.json"

def build_index():
    os.makedirs(INDEX_DIR, exist_ok=True)

    with open(CATALOG_PATH, "r") as f:
        catalog = json.load(f)

    texts = [c["semantic_profile_text"] for c in catalog]
    vectors = generate_dense_vectors(texts)

    dim = len(vectors[0])
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "w") as f:
        json.dump(
            [{"name": c["name"], "url": c["url"], "test_types": c["test_types"]}
             for c in catalog],
            f
        )

def load_index():
    if not os.path.exists(INDEX_PATH):
        print("FAISS index not found. Building index...")
        build_index()

    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "r") as f:
        meta = json.load(f)

    return index, meta
