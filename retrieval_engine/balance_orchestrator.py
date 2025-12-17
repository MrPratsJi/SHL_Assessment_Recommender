def classify_candidate(candidate):
    joined = " ".join(candidate["test_types"]).lower()
    if any(k in joined for k in ["personality", "behavior"]):
        return "soft"
    return "hard"


def balance_candidates(candidates, intent, final_k=10):
    hard = []
    soft = []

    for c in candidates:
        if classify_candidate(c) == "soft":
            soft.append(c)
        else:
            hard.append(c)

    if intent == "hard":
        primary, secondary = hard, soft
    elif intent == "soft":
        primary, secondary = soft, hard
    else:
        half = final_k // 2
        mixed = hard[:half] + soft[:final_k - half]
        if len(mixed) < final_k:
            remainder = [
                c for c in candidates if c not in mixed
            ]
            mixed.extend(remainder[: final_k - len(mixed)])
        return mixed

    result = primary[:final_k]
    if len(result) < final_k:
        result.extend(secondary[: final_k - len(result)])

    return result
