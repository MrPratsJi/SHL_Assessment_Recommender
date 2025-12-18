import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

_vectorizer = None

def init_vectorizer(corpus_texts):
    global _vectorizer
    _vectorizer = TfidfVectorizer(
        max_features=4096,
        ngram_range=(1, 2),
        stop_words="english"
    )
    _vectorizer.fit(corpus_texts)

def generate_dense_vectors(texts):
    if _vectorizer is None:
        raise RuntimeError("TF-IDF vectorizer not initialized")

    vectors = _vectorizer.transform(texts).toarray()
    return np.asarray(vectors, dtype="float32")
