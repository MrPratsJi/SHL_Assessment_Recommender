import pandas as pd
from intent_intelligence.intent_resolver import resolve_intent
from retrieval_engine.candidate_locator import fetch_candidates
from retrieval_engine.balance_orchestrator import balance_candidates
from retrieval_engine.scoring_kernel import score_and_rank
from evaluation_lab.recall_tracker import recall_at_k


def evaluate(train_csv_path):
    df = pd.read_csv(train_csv_path)
    grouped = df.groupby("Query")["Assessment_url"].apply(list)

    scores = []

    for query, relevant_urls in grouped.items():
        intent = resolve_intent(query)
        candidates = fetch_candidates(query, top_k=50)
        balanced = balance_candidates(candidates, intent["intent"], final_k=10)
        final = score_and_rank(balanced)

        predicted_urls = [c["url"] for c in final]
        score = recall_at_k(predicted_urls, relevant_urls, k=10)
        scores.append(score)

    return sum(scores) / len(scores)
