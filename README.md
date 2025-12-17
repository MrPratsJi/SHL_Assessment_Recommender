# 🧠 SHL GenAI Assessment Recommendation System

An **intent-aware, retrieval-based system** that maps natural-language hiring queries to **relevant and balanced SHL individual assessments**. Built as a **production pipeline**, not a prompt demo.

---

## 🎯 Goal

Replace brittle keyword filtering with a system that:
- understands **hiring intent**
- retrieves **relevant assessments**
- enforces **hard + soft skill balance** when required

Input: natural language query or JD  
Output: 5–10 **SHL individual test solutions**

---

## 🏗️ Architecture

       Query
        ↓
    Intent Resolver
        ↓
    Semantic Retrieval (FAISS)
        ↓
    Intent-Aware Balancing
        ↓
    Final Scoring
        ↓
    API / Web UI

---

## 📦 Data Ingestion

- Source: SHL Product Catalog  
- Scope: **Individual Test Solutions only**  
- Pre-packaged solutions excluded

Each assessment is normalized into a canonical schema and expanded into variants.

---

## Result:

**1944 individual assessments**

A controlled `semantic_profile_text` (name, description, test type, skills) is embedded.

---

## 📁 Source of truth: 

`artifacts/shl_individual_assessments.json` Generated once, never edited manually.

---

## 🔍 Two-Stage Retrieval

**Stage 1 – Semantic Retrieval**

- Query embedding + FAISS search (top-50)
- Goal: **maximize recall**

**Stage 2 – Intent-Aware Ranking**

- Structured intent extraction
- Test-type balancing
- Final relevance scoring

This separation improves **accuracy, explainability, and tunability**.

---

## 🧩 Intent Intelligence

Each query is converted into structured intent:
- `hard skills`  
- `soft skills`
- `desired test types`  
- `seniority hint`  
- `domain hint`  

This enables explicit balancing and predictable behavior.

Prompt iterations tracked in: `artifacts/prompt_versions/`

---

## ⚖️ Balancing Strategy

For mixed queries (e.g. **Java + collaboration**):

- candidates grouped by test type  
- quotas allocated per intent  
- ensures coverage of:
  - `Knowledge & Skills`  
  - `Personality & Behavior`  

Prevents over-indexing on one dimension.

---

## 📊 Scoring

Final ranking combines:
- `semantic` similarity  
- `skill overlap with intent`  
- `test-type alignment`  

Weights configurable via: `config/runtime.yaml`

---

## 🧪 Evaluation

**Metric:** Mean Recall@10  
**Dataset:** SHL-provided labeled train set

| Approach | Recall@10 |
|----------|-----------|
| Semantic-only | **~0.11** |
| Intent-aware + balanced | **0.1878** |

Improvements driven by:

- structured intent
- explicit balancing
- richer semantic profiles

📁 `evaluation_lab/metrics_report.json`

---

## 🔌 API

**Health**

- GET /health → `{ "status": "healthy" }`

**Recommend**

- POST /recommend → `{ "query": "Need a Java developer who can collaborate with business stakeholders" }`
  
  - Returns 5–10 assessment names + URLs (exact spec).

---

## 🖥️ Web UI

Minimal UI for manual testing:

- query input
- calls `/recommend`
- renders table
- No frontend frameworks.

---

## 🚀 Run

- pip install -r requirements.txt
 
- python catalog_ingestion/shl_forge.py

- python -m semantic_index.vector_forge
 
- uvicorn api_layer.service_bootstrap:app --port 8000

- uvicorn web_client.app:app --port 8080
