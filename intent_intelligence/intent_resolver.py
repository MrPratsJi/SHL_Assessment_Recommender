import json
import os

SCHEMA_PATH = os.path.join(
    os.path.dirname(__file__),
    "intent_schema.json"
)

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    SCHEMA = json.load(f)

def resolve_intent(query):
    q = query.lower()
    hard = sum(1 for k in SCHEMA["hard_skills"] if k in q)
    soft = sum(1 for k in SCHEMA["soft_skills"] if k in q)

    if hard > 0 and soft > 0:
        intent = "mixed"
    elif soft > hard:
        intent = "soft"
    else:
        intent = "hard"

    return {
        "intent": intent,
        "hard_score": hard,
        "soft_score": soft
    }
