import numpy as np
from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_dense_vectors(texts):
    vectors = _model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )
    return np.array(vectors, dtype="float32")
