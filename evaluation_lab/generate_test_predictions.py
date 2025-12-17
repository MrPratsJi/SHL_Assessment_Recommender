import pandas as pd
from intent_intelligence.intent_resolver import resolve_intent
from retrieval_engine.candidate_locator import fetch_candidates
from retrieval_engine.balance_orchestrator import balance_candidates
from retrieval_engine.scoring_kernel import score_and_rank

def generate_from_queries(queries, output_path):
    rows = []

    for query in queries:
        intent = resolve_intent(query)
        candidates = fetch_candidates(query, top_k=50)
        balanced = balance_candidates(candidates, intent["intent"], final_k=10)
        ranked = score_and_rank(balanced)

        for r in ranked:
            rows.append({
                "Query": query,
                "Assessment_url": r["url"]
            })

    pd.DataFrame(rows).to_csv(output_path, index=False)

if __name__ == "__main__":
    pd.DataFrame(columns=["Query", "Assessment_url"]).to_csv(
        "artifacts/prediction_output.csv",
        index=False
    )
