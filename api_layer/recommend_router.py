from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from intent_intelligence.intent_resolver import resolve_intent
from retrieval_engine.candidate_locator import fetch_candidates
from retrieval_engine.balance_orchestrator import balance_candidates
from retrieval_engine.scoring_kernel import score_and_rank

router = APIRouter()

class RecommendRequest(BaseModel):
    query: str

@router.post("/recommend")
def recommend(req: RecommendRequest):
    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Empty query")

    intent = resolve_intent(query)
    candidates = fetch_candidates(query, top_k=30)
    balanced = balance_candidates(candidates, intent["intent"], final_k=10)
    final = score_and_rank(balanced)

    return {
        "recommendations": [
            {
                "assessment_name": c["name"],
                "assessment_url": c["url"]
            }
            for c in final
        ]
    }
