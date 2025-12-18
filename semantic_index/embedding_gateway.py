import numpy as np
from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device="cpu"
        )
    return _model

def generate_dense_vectors(texts):
    model = get_model()
    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False
    )
    return np.array(vectors, dtype="float32")
