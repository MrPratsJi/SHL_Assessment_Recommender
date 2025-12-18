import numpy as np
from sentence_transformers import SentenceTransformer

_MODEL_NAME = "all-MiniLM-L6-v2"
_model = None

def init_vectorizer():
    global _model
    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)

def generate_dense_vectors(texts):
    init_vectorizer()
    vectors = _model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False
    )
    return np.array(vectors, dtype="float32")
