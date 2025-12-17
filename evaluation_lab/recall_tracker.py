def recall_at_k(predicted_urls, relevant_urls, k=10):
    predicted = set(predicted_urls[:k])
    relevant = set(relevant_urls)
    if not relevant:
        return 0.0
    return len(predicted & relevant) / len(relevant)
