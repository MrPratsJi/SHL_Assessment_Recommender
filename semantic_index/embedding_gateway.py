import os
import numpy as np

_MODEL = None

def _load_model():
    global _MODEL
    if _MODEL is None:
        from sentence_transformers import SentenceTransformer
        _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _MODEL


def generate_dense_vectors(texts):
    if os.getenv("EMBEDDINGS_ENABLED", "false").lower() != "true":
        raise RuntimeError(
            "Embedding generation is disabled in production. "
            "Use prebuilt FAISS index."
        )

    model = _load_model()
    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )
    return np.array(vectors, dtype="float32")
