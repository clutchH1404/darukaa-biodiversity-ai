# 🌿 DARUKAA.EARTH — AI BIODIVERSITY INTELLIGENCE PLATFORM
### Hackathon Project: AI Biodiversity Intelligence Chatbot

[![CI/CD Pipeline](https://github.com/darukaa-earth/darukaa-biodiversity-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/darukaa-earth/darukaa-biodiversity-ai/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![ChromaDB](https://img.shields.io/badge/vector%20db-ChromaDB-purple.svg)](https://www.trychroma.com/)
[![Tests](https://img.shields.io/badge/tests-33%20passed-brightgreen.svg)](tests/)

---

## 1. Project Overview
**Darukaa.Earth** is an enterprise-grade, conversational environmental intelligence platform designed for ecological scientists, regenerative farmers, land stewards, and conservation authorities. Unlike standard conversational bots that synthesize generic, hallucinated text, Darukaa.Earth functions as an **AI Environmental Scientist**.

It combines:
- A structured multi-metric reasoning engine that couples at least 3 environmental parameters (Soil, Land, Biodiversity, Climate, Human Impact, Water) before generating actionable advice.
- An authoritative Retrieval-Augmented Generation (RAG) pipeline indexed with verified reports from **FAO, IPCC, UNEP, IPBES, CGIAR, and peer-reviewed journals**.
- Dynamic missing-variable detection to prevent superficial conclusions.
- Transparent, factorized scientific confidence scoring.
- Anti-hallucination guardrails and prompt injection isolation.

---

## 2. Problem Statement
Current large language models (LLMs) fail in environmental and ecological decision support:
1. **Generic, Action-Poor Advice**: Default LLMs provide superficial answers like *"plant more trees"* or *"use compost"*, ignoring local soil chemistry, water availability, and landscape fragmentation.
2. **Hallucination of Scientific Data**: LLMs routinely fabricate citations, DOIs, and empirical recovery percentages.
3. **Single-Variable Reductionism**: Most tools evaluate a single metric in isolation (e.g., low nitrogen $\rightarrow$ add synthetic fertilizer), missing the systemic causal cascades connecting soil organic carbon, moisture retention, pollinator habitats, and crop resilience.
4. **Disregard of Biophysical Limits**: Recommending moisture-demanding cover crops in low-rainfall drylands without mulch termination can cause total crop failure.

---

## 3. Solution: Darukaa.Earth
Darukaa.Earth transforms biodiversity reasoning into a rigorous, verifiable biophysical workflow:
1. **Explicit Causal Graph Reasoning**: Traverses a configurable directed graph connecting edaphic, hydrological, microclimatic, and ecological variables.
2. **Real RAG Grounding**: Every recommendation points directly to an authentic scientific publication in the vector store with verifiable URLs.
3. **Conversational Dynamic Inquiries**: If the user's initial inquiry is underspecified, the assistant asks targeted clarifying questions before prescribing interventions.
4. **10-Point Recommendation Schema**: Conforms strictly to a 10-point actionable template (What to do, Why it works, Variables involved, Impacted metrics, Time horizon, Direction of change, Confidence, Evidence, Assumptions, Trade-offs).

---

## 4. Architecture
The system employs a modular, microservice-ready architecture:

```
[ User Query / Structured JSON ]
               │
               ▼
   [ Security Guardrail ] ──> Filter Prompt Injections
               │
               ▼
[ Missing Variable Detector ] ──> Dynamic Inquiries
               │
               ▼
   [ Session Memory Store ] ──> Cumulative SQLite Profile
               │
               ▼
[ Multi-Metric Reasoning ] ──> Causal Graph (≥3 Variables)
               │
               ▼
   [ Authoritative RAG ] ──> ChromaDB Semantic + Hybrid Rank
               │
               ▼
[ Recommendation Engine ] ──> 10-Point Scientific Schema
               │
               ▼
[ Interactive Dashboard ] ──> Streamlit / FastAPI REST API
```

---

## 5. RAG Pipeline
The RAG pipeline operates without mock data:
1. **Ingestion**: Authoritative reports are ingested from `/data/knowledge/scientific_knowledge_seed.json` and `/data/raw/`.
2. **Chunking**: `DocumentChunker` breaks documents into coherent sections while preserving document ID, authoring body, publication year, environmental domain, variables, citations, and URLs.
3. **Embedding & Storage**: Processed chunks are indexed in **ChromaDB** using cosine distance spaces.
4. **Hybrid Retrieval**: `EvidenceRetriever` ranks documents based on:
   - Cosine semantic similarity (60% weight)
   - Source reliability score (20% weight)
   - Variable overlap with active environmental state (up to +20% boost)
   - Geographic context matching (e.g., semi-arid dryland boost)
5. **Passive Data Enclosure**: Retrieved passages are enclosed within `<evidence_item>` tags to prevent prompt injection.

---

## 6. Knowledge Base
The knowledge base covers all 16 required domains:
1. Soil Health | 2. Biodiversity | 3. Agroforestry | 4. Intercropping | 5. Cover Crops
6. Soil Organic Carbon | 7. Soil Moisture | 8. Pollinators | 9. Habitat Fragmentation
10. Land-Use Change | 11. Climate Impacts | 12. Deforestation | 13. Water Availability
14. Sustainable Agriculture | 15. Ecological Restoration | 16. Human Pollution Impacts

Authoritative sources include:
- **FAO (2020)**: *Recarbonizing Global Soils (GSOC)*
- **IPCC (2019)**: *Special Report on Climate Change and Land (SRCCL)*
- **IPBES (2019)**: *Global Assessment Report on Biodiversity and Ecosystem Services*
- **IPBES (2016)**: *Thematic Assessment of Pollinators, Pollination and Food Production*
- **Science Advances (Tamburini et al., 2020)**: *Agricultural diversification promotes multiple ecosystem services*
- **Science (Garibaldi et al., 2016)**: *Targeted habitat strips and wild pollinators boost crop yields*
- **UNEP (2021)**: *Making Peace with Nature*
- **US EPA (2020)**: *Agricultural Nutrient and Sediment Management*
- **Lal, R. (2020)**: *Soil Organic Matter and Water Retention*

---

## 7. Database Schema
Persistent storage is managed via SQLite (`darukaa_biodiversity.db`) with four primary tables:
- `environmental_observations`: Stores over 25 fields including coordinates, region, soil pH, SOC %, soil moisture, land use, species richness, climate variables, and raw JSON.
- `conversations`: Stores multi-turn chat sessions and cumulative environmental state dictionaries.
- `sources_registry`: Maintains the catalog of verified scientific reports and DOIs.
- `recommendation_logs`: Audits generated interventions and associated citations.

---

## 8. Multi-Metric Reasoning Engine
The reasoning engine models compound ecological interactions. It **strictly enforces combining at least 3 environmental variables** before generating major recommendations:

$$\text{Low SOC} + \text{Low Rainfall} + \text{Monoculture Wheat} + \text{Low Biodiversity}$$
$$\Downarrow$$
1. Low SOC ($\le 0.5\%$) limits aggregate stability and reduces Available Water Capacity (AWC).
2. Low rainfall elevates xylem water tension and drives acute matric water stress.
3. Monoculture farming simplifies vegetation strata, inducing spatial homogenization and floral deficits.
4. Loss of floral succession reduces pollinator presence and subterranean mycorrhizal activity.
5. Systemic conclusion: Deploy multi-strata agroforestry windbreaks and roller-crimped legume cover crops to simultaneously buffer moisture, rebuild carbon, and restore ecological niches.

---

## 9. Recommendation Engine (10-Point Schema)
Every generated recommendation adheres strictly to the 10-point schema:
- **A. What to do**: Context-sensitive, actionable intervention.
- **B. Why it works**: Biophysical and ecological mechanisms.
- **C. Environmental variables involved**: $\ge 3$ intersecting variables.
- **D. Impacted metrics**: Quantified or directional metrics supported by empirical literature.
- **E. Time horizon**: Short (1 season), Medium (2–3 years), Long (3+ years).
- **F. Expected direction of change**: (e.g., SOC $\uparrow$, Water Stress $\downarrow$, Pests $\downarrow$).
- **G. Confidence**: High / Medium / Low with transparent formulaic justification.
- **H. Scientific evidence**: Exact citation, organization, year, and URL.
- **I. Important assumptions**: Soil depth, slope, rainfall thresholds.
- **J. Possible trade-offs & risks**: Seed costs, machinery requirements, moisture competition.

---

## 10. Conversation Memory & Missing Information
- **Dynamic Variable Extraction**: Automatically extracts SOC %, pH, rainfall, and land use from natural language user messages.
- **State Merging**: Accumulates observations across turns without asking redundant questions.
- **Targeted Inquiries**: If key parameters are absent, the system inquires about the most critical missing metrics first.

---

## 11. REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Diagnostic status & vector counts |
| `GET` | `/sources` | Catalog of authoritative scientific reports |
| `POST` | `/chat` | Main conversational intelligence endpoint |
| `POST` | `/analyze` | Multi-metric bottleneck discovery |
| `POST` | `/recommend` | Direct 10-point recommendation generator |
| `POST` | `/retrieve` | Vector retrieval with hybrid ranking |
| `POST` | `/environment` | Submit structured environmental JSON |
| `POST` | `/ingest` | Ingest new scientific document into vector DB |
| `GET` | `/conversation/{id}` | Session history and accumulated state |

---

## 12. Local Setup

### Prerequisites
- Python 3.10+ (Tested on Python 3.11, 3.12, and 3.14)
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/darukaa-earth/darukaa-biodiversity-ai.git
cd darukaa-biodiversity-ai

# Install dependencies
pip install -r requirements.txt

# Ingest scientific knowledge base and seed database
python scripts/ingest_documents.py
python scripts/seed_database.py
```

---

## 13. Environment Variables
Create a `.env` file based on `.env.example`:
```env
APP_ENV=development
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_PORT=8501

# LLM Configuration (OpenAI-compatible)
# Leave empty to run with deterministic calibrated scientific synthesis mode (100% offline-ready!)
OPENAI_API_KEY=
OPENAI_API_BASE=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```

---

## 14. Running Instructions

### Option A: Launch Interactive Streamlit Dashboard
```bash
streamlit run frontend/streamlit_app.py
```
*Opens at: `http://localhost:8501`*

### Option B: Launch FastAPI Backend Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
*API docs available at: `http://localhost:8000/docs`*

---

## 15. Testing
The repository contains 33 automated tests covering all 9 required verification areas and the 5 official test cases:
```bash
pytest -v tests/
```

### Test Coverage Highlights:
- `test_json_validation.py`: Pydantic validation of environmental observations.
- `test_missing_variable_detection.py`: Dynamic missing variable discovery.
- `test_multi_metric_reasoning.py`: Causal graph traversal and $\ge 3$ variable enforcement.
- `test_rag_retrieval.py`: ChromaDB semantic search and hybrid ranking.
- `test_citation_generation.py`: Verification that citations correspond to real literature.
- `test_recommendations.py`: Verification of the 10-point schema.
- `test_conversation_memory.py`: Multi-turn state accumulation.
- `test_hallucination_safeguards.py`: Prompt injection isolation.
- `test_api_endpoints.py`: All 9 FastAPI endpoints.
- `test_environmental_cases.py`: The 5 official environmental scenarios.

---

## 16. Docker Instructions

### Build and Run with Docker Compose
```bash
docker-compose up --build
```
- Streamlit UI: `http://localhost:8501`
- FastAPI API: `http://localhost:8000`

---

## 17. Deployment Instructions
- **Frontend**: Deploy `frontend/streamlit_app.py` directly to **Streamlit Community Cloud** (no extra dependencies required).
- **Backend**: Deploy to **Render / Railway / Fly.io** using the provided `Dockerfile`.

---

## 18. Example Queries
1. *"Biodiversity is declining on my land."* (Triggers dynamic missing variable inquiries).
2. *"Our soil organic carbon is 0.3%, annual rainfall is low, and we cultivate monoculture wheat in a semi-arid region. What interventions should we take?"* (Triggers full multi-metric reasoning and cover crop / agroforestry recommendations).
3. *"We have high pesticide application, high rainfall, and low pollinator abundance in an orchard."* (Triggers ecotoxicological bottleneck detection and flowering corridor recommendations).

---

## 19. Demo Scenario (Semi-Arid Monoculture Wheat)
Click the **🚀 Run Hackathon Demo Scenario** button in the Streamlit UI to automatically load and evaluate the official hackathon benchmark:
- **Soil Organic Carbon**: 0.3%
- **Rainfall**: Low
- **Land-Use**: Monoculture Wheat
- **Region**: Semi-arid
- **Outcome**: Detects critical structural collapse and water retention deficit; combines 4 variables; retrieves FAO GSOC (2020) and Lal (2020); outputs 10-point recommendations with citations.

---

## 20. Limitations
- Remote sensing satellite feeds (e.g., Sentinel-2 NDVI, Copernicus soil moisture) are currently ingested as observational records rather than live streaming APIs.
- Calibrated crop growth models (e.g., DSSAT, APSIM) are proxied by empirical meta-analyses rather than real-time daily simulations.

---

## 21. Future Improvements
- Direct integration with Google Earth Engine and ESA Copernicus data APIs for automatic latitude/longitude weather and NDVI extraction.
- Edge deployment for offline field tablet use in remote rural landscapes.
- Multi-lingual farmer interface with voice interaction in local dialects.

---

**Developed for the Darukaa.Earth AI Biodiversity Intelligence Hackathon.**
