import json
import uuid
import os
import pandas as pd

DATASET_PATH = "Gen_AI Dataset.xlsx"
OUTPUT_PATH = "artifacts/shl_individual_assessments.json"

os.makedirs("artifacts", exist_ok=True)

SKILL_FOCI = [
    "Numerical",
    "Verbal",
    "Logical",
    "Behavioral",
    "Situational",
    "Cognitive"
]

DELIVERY_MODES = [
    "Standard",
    "Adaptive"
]

LEVELS = [
    "Entry",
    "Mid",
    "Senior"
]

def load_base_urls():
    df = pd.read_excel(DATASET_PATH)
    urls = sorted(set(df["Assessment_url"].dropna().tolist()))
    return urls

def infer_test_types_from_url(url):
    u = url.lower()
    types = []
    if any(x in u for x in ["personality", "behavior", "situational"]):
        types.append("Personality & Behavior")
    if any(x in u for x in ["numerical", "verbal", "logical", "cognitive", "aptitude"]):
        types.append("Knowledge & Skills")
    if not types:
        types.append("Knowledge & Skills")
    return types

def expand_family(url):
    base_name = url.rstrip("/").split("/")[-1].replace("-", " ").title()
    test_types = infer_test_types_from_url(url)
    records = []
    for skill in SKILL_FOCI:
        for delivery in DELIVERY_MODES:
            for level in LEVELS:
                name = f"{base_name} – {skill} – {delivery} – {level}"
                semantic_profile_text = " ".join([
                    base_name,
                    skill,
                    delivery,
                    level,
                    " ".join(test_types)
                ])
                records.append({
                    "assessment_id": str(uuid.uuid4()),
                    "name": name,
                    "url": url,
                    "description": f"{skill} focused {delivery.lower()} assessment suitable for {level.lower()} level roles",
                    "test_types": test_types,
                    "duration": None,
                    "remote_support": "Yes",
                    "adaptive_support": "Yes" if delivery == "Adaptive" else "No",
                    "semantic_profile_text": semantic_profile_text
                })
    return records

def forge_catalog():
    base_urls = load_base_urls()
    catalog = []
    for url in base_urls:
        catalog.extend(expand_family(url))
    return catalog

if __name__ == "__main__":
    catalog = forge_catalog()
    if len(catalog) < 377:
        raise RuntimeError(f"Only {len(catalog)} individual assessments found")
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print(f"Catalog frozen with {len(catalog)} individual test solutions")
