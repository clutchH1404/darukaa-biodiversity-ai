# 🌿 DARUKAA.EARTH
## AI Biodiversity Intelligence & Ecological Causal Reasoning Console
### Darukaa.Earth AI Biodiversity Intelligence Chatbot Challenge

[![CI/CD Pipeline](https://github.com/clutchH1404/darukaa-biodiversity-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/clutchH1404/darukaa-biodiversity-ai)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/frontend-React%2019%20%2B%20Vite%206-61DAFB.svg)](web/)
[![ChromaDB](https://img.shields.io/badge/vector%20db-ChromaDB-purple.svg)](https://www.trychroma.com/)
[![Tests](https://img.shields.io/badge/tests-37%20passed-brightgreen.svg)](tests/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 1. Project Overview

**Darukaa.Earth** is an enterprise-grade AI environmental scientist and biosphere intelligence command console. It is engineered specifically for the **Darukaa.Earth AI Biodiversity Intelligence Chatbot Challenge** to solve the fundamental failure mode of generic conversational AI in ecological management: superficial, single-variable reductionism and hallucinated scientific claims.

### What the System Does
Darukaa.Earth ingests unstructured natural-language field observations and structured environmental measurements. It dynamically extracts relevant environmental metrics, identifies missing critical context, inquiries about missing measurements to avoid guessing, executes semantic vector retrieval against peer-reviewed literature, performs multi-variable causal reasoning across $\ge 3$ interconnected biophysical variables, projects empirical intervention outcomes, and issues 10-point actionable agroecological protocols backed by verifiable citations.

### The Problem It Solves
Standard generative chatbots routinely output hazardous ecological advice:
- Recommending moisture-demanding cover crops in low-rainfall drylands without mulch termination, driving acute crop failure.
- Suggesting monoculture tree planting in natural grasslands, destroying endemic floral biodiversity.
- Fabricating citations, DOIs, and empirical recovery percentages.
- Treating complex living ecosystems as single isolated variables (e.g., "nitrogen is low $\to$ add synthetic fertilizer"), ignoring the systemic cascades connecting soil organic carbon, moisture retention, pollinator habitats, and crop resilience.

### How Darukaa.Earth Solves It
Darukaa.Earth fuses **conversational intelligence**, **authoritative RAG**, an **explicit directed causal relationship graph**, and **bounded empirical simulation models** into a unified, auditable intelligence console.

---

## 2. Hackathon Problem

The hackathon challenges participants to build an **AI Environmental Scientist** capable of understanding the intricate interdependencies governing ecosystems, land use, climate, and biodiversity.

Key challenge dimensions addressed:
- **Ecosystem Understanding**: Grounded modeling of soil chemistry, hydrology, vegetation structure, and multi-trophic guilds.
- **Land/Environment Context**: Differentiating between intensive monoculture, agroforestry, pastoral grazing, and fragmented remnants.
- **Climate/Environmental Variables**: Coupling rainfall variability, vapor pressure deficit, drought status, and temperature extremes.
- **Biodiversity Preservation**: Prioritizing wild pollinators, soil microbial respiration, and landscape dispersal corridors.
- **Scientific Grounding**: Strict zero-hallucination policy where citations originate from authentic intergovernmental reports and journals.
- **Actionable Recommendations**: Standardized 10-point protocols specifying operational actions, mechanisms, impacted metrics, time horizons, and trade-offs.
- **Multi-Variable Reasoning**: Coupling at least 3 environmental variables to formulate holistic interventions.

---

## 3. Key Features

Only features implemented and verified in the codebase are documented below:

1. **Conversational Environmental Intelligence**: Natural language comprehension parsing complex field notes into structured environmental states.
2. **Dynamic Missing-Variable Detection**: Diagnoses when user observations lack critical context (e.g. unknown water availability or land-use pattern) and generates targeted clarifying questions before prescribing interventions.
3. **Multi-Turn Session Memory**: Preserves cumulative environmental profiles segmented across 7 biophysical domains across multi-turn dialogues.
4. **Authoritative RAG Knowledge Retrieval**: ChromaDB vector store populated with 12 peer-reviewed scientific reports from **FAO, IPCC, IPBES, Science, and Nature**.
5. **Multi-Metric Causal Reasoning Engine**: Enforces that interventions must be reasoned across $\ge 3$ interacting environmental variables.
6. **Directed Biophysical Relationship Graph**: 29 nodes and 26 directed edges mapping edaphic, hydrological, and vegetative cascades with biophysical mechanism annotations.
7. **10-Point Recommendation Protocols**: Operational templates with actions, biophysical justifications, impacted metric sets, time horizons, directions, assumptions, trade-offs, and citations.
8. **Biophysical Intervention Simulator**: Empirical transfer models projecting multi-year trajectories for cover crops, agroforestry, swales, and corridors; transparently returns `"Simulation model unavailable"` for unsupported methods.
9. **Sentinel-2 Multispectral HUD**: Spatial Earth observation HUD overlay with coordinate telemetry and spectral layer toggles.
10. **Judge Demo Presets**: 4 preconfigured evaluation scenarios (Amazon Basin, Cerrado Fringe, Rift Valley, Atlantic Forest) executing the live backend pipeline.

---

## 4. System Architecture

```
                             DARUKAA.EARTH ECOSYSTEM
                                        │
           ┌────────────────────────────┴────────────────────────────┐
           ▼                                                         ▼
   FASTAPI REST BACKEND (:8000)                             REACT COMMAND CONSOLE (:3000)
┌────────────────────────────────────────┐             ┌─────────────────────────────────────────┐
│ • Security & Prompt Injection Guard    │             │ • WebGL Multi-Octave Atmospheric Canvas │
│ • Query Understander (20+ Variables)   │ <────────── │ • 7-Stage Animated Reasoning HUD        │
│ • Dynamic Missing Variable Detector    │             │ • AI Scientist Multi-Turn Console       │
│ • Multi-Metric Causal Reasoning Engine │             │ • Interactive SVG Biophysical Graph     │
│ • Directed Biophysical Graph (29 nodes)│             │ • 10-Point Recommendation Protocols     │
│ • ChromaDB Persistent Vector Store     │             │ • RAG Evidence Drawer with Similarity   │
│ • Biophysical Simulation Engine        │             │ • Intervention Scenario Simulator       │
│ • SQLite Persistent Session Memory     │             │ • Sentinel-2 Multispectral HUD Overlay  │
└────────────────────────────────────────┘             └─────────────────────────────────────────┘
```

---

## 5. AI Pipeline

The platform visibly executes and exposes the complete 7-stage environmental intelligence chain:

```
[01 INTAKE] Field Observation Ingestion & Sanitization
     │
     ▼
[02 PARSE] Variable Detection across 20+ Ecological Metrics
     │
     ▼
[03 CONTEXT] Missing Variable Analysis & Targeted Clarification Questions
     │
     ▼
[04 RAG] ChromaDB Semantic Retrieval & Hybrid Variable Re-Ranking
     │
     ▼
[05 GRAPH] Multi-Metric Causal Synthesis across ≥3 Coupled Variables
     │
     ▼
[06 ACTIONS] 10-Point Recommendation Protocol Generation
     │
     ▼
[07 AUDIT] Grounded Evidence Verification & Similarity Auditing
```

---

## 6. Knowledge & RAG System

### Source Literature & Storage
The knowledge base indexes 12 peer-reviewed reports stored in `data/knowledge/scientific_knowledge_seed.json` and processed into `data/processed/knowledge_chunks.json`.

Authoritative sources include:
- **FAO (2020)**: *Recarbonizing Global Soils (GSOC)* — Technical Manual Vol 1-6.
- **IPCC (2019)**: *Special Report on Climate Change and Land (SRCCL)* — Chapter 5: Food Security.
- **IPBES (2019)**: *Global Assessment Report on Biodiversity and Ecosystem Services*.
- **IPBES (2016)**: *Thematic Assessment on Pollinators, Pollination and Food Production*.
- **Science Advances (Tamburini et al., 2020)**: *Agricultural diversification promotes multiple ecosystem services*.
- **Science (Garibaldi et al., 2016)**: *Targeted habitat strips and wild pollinators boost crop yields*.
- **Nature (Hooper et al., 2012)**: *A global synthesis reveals biodiversity loss is a major driver of ecosystem change*.
- **UNEP (2019)**: *Global Environment Outlook (GEO-6)*: Terrestrial ecosystems and land restoration.

### Chunking & Embedding Strategy
`app/rag/chunker.py` segments documents into structured chunks preserving metadata: `document_id`, `organization`, `publication_year`, `environmental_domain`, `variables`, `citation`, `url`, and `reliability_score`. Chunks are embedded and stored in **ChromaDB** using cosine distance spaces.

### Hybrid Retrieval & Re-ranking
`app/rag/retriever.py` implements a hybrid ranking algorithm:
$$\text{Score} = 0.60 \times \text{CosineSimilarity} + 0.20 \times \text{ReliabilityScore} + \text{VariableOverlapBoost} + \text{GeographicBoost}$$

### Production Persistence Safeguard
On startup, `app/main.py` checks `vector_store.count()`. If the vector store is empty (e.g. after a clean container build or cloud redeployment), it automatically and idempotently re-indexes the entire knowledge base from `scientific_knowledge_seed.json` within seconds. The knowledge base never disappears.

---

## 7. Multi-Metric Reasoning

The multi-metric reasoning engine (`app/reasoning/engine.py`) models biophysical dependencies across 29 ecological nodes and 26 directed causal pathways (`app/reasoning/relationship_graph.py`).

### Implemented Causal Pathways:
1. **Soil-Hydrology-Habitat Cascade**:
   $$\text{Soil Organic Carbon} \xrightarrow{+} \text{Soil Structure} \xrightarrow{+} \text{Water Retention Capacity} \xrightarrow{+} \text{Root Zone Moisture} \xrightarrow{+} \text{Plant Resilience} \xrightarrow{+} \text{Habitat Quality} \xrightarrow{+} \text{Biodiversity}$$
2. **Rainfall-Hydraulic Stress Cascade**:
   $$\text{Rainfall} \xrightarrow{-} \text{Water Stress} \xrightarrow{-} \text{Plant Survival} \xrightarrow{+} \text{Primary Productivity}$$
3. **Landscape Fragmentation Cascade**:
   $$\text{Monoculture Intensity} \xrightarrow{+} \text{Habitat Fragmentation} \xrightarrow{-} \text{Corridors} \xrightarrow{-} \text{Species Movement} \xrightarrow{-} \text{Species Richness}$$
4. **Ecotoxicological Cascade**:
   $$\text{Pesticide Intensity} \xrightarrow{+} \text{Non-Target Toxicity} \xrightarrow{-} \text{Pollinator Abundance} \xrightarrow{-} \text{Angiosperm Seed Set}$$

The engine requires coupling **at least 3 variables** before generating systemic interventions.

---

## 8. Conversational Intelligence

- **Query Understanding** (`app/memory/query_understander.py`): Dynamically extracts 20+ variables (soil health, SOC %, soil degradation, water availability, water stress, rainfall, temperature, vegetation cover, fragmentation, land use, pollinators, wildlife, connectivity).
- **Missing Variable Discovery** (`app/memory/missing_variable_detector.py`): Identifies unstated critical measurements and formulates specific clarifying questions.
- **Segmented Session Memory** (`app/memory/session_memory.py`): Stores accumulated state segmented into `location`, `soil`, `water`, `vegetation`, `land_use`, `biodiversity`, `climate`, and `conversation_history`.

---

## 9. Recommendation Output

Every recommendation generated by `app/recommendations/generator.py` conforms to the standardized 10-point schema:
1. **Title & Identifier** (e.g., `REC-1-INT-COV-01`)
2. **Action / What to do** (Operational instructions)
3. **Why it works** (Biophysical mechanism)
4. **Variables involved** (Coupled multi-metric set, $\ge 3$)
5. **Impacted environmental metrics** (e.g., SOC %, Infiltration, Pollinators)
6. **Expected time horizon** (e.g., `1 - 3 years`)
7. **Expected direction of change** (e.g., `Increase Available Water Holding Capacity`)
8. **Calculated scientific confidence** (`HIGH`, `MEDIUM-HIGH`, or `MODERATE` with transparent rationale)
9. **Scientific citations** (Authentic literature provenance with direct URLs)
10. **Assumptions & Trade-offs** (Prerequisites and operational constraints)

---

## 10. Technology Stack

| Layer | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Frontend Framework** | React + Vite | React 19, Vite 6 | NASA/Palantir-style Command Console |
| **Frontend Language** | TypeScript | 5.6+ | Type safety matching Pydantic schemas |
| **Styling** | Tailwind CSS | 3.4+ | Stitch-inspired dark biosphere palette |
| **Visual FX / Shader** | WebGL | Native 1.0/2.0 | Multi-octave simplex atmospheric canvas |
| **Backend Framework** | FastAPI | 0.115+ | High-performance RESTful API |
| **Backend Language** | Python | 3.11 / 3.14 | Scientific computing and reasoning runtime |
| **Vector Database** | ChromaDB | 0.5+ | Local persistent vector storage with cosine metric |
| **Relational Database** | SQLite | 3.x | Persistent observation and session storage |
| **Validation** | Pydantic | v2.10+ | Strict bidirectional schema validation |
| **Testing** | Pytest | 8.4+ | Automated test suite (37 tests) |
| **Deployment** | Vercel / Render / Docker | Multi-cloud | Production deployment manifests |

---

## 11. Project Structure

```
darukaa-biodiversity-ai/
├── app/                                 # FastAPI Backend Architecture
│   ├── core/
│   │   ├── config.py                    # Environment settings, dynamic PORT, CORS
│   │   └── security.py                  # Input sanitization & prompt injection guardrails
│   ├── models/
│   │   ├── environmental_state.py       # Comprehensive 6-domain environmental schema
│   │   ├── knowledge_schema.py          # Knowledge document & retrieved chunk schemas
│   │   └── response_models.py           # 10-point recommendation & reasoning trace schemas
│   ├── memory/
│   │   ├── query_understander.py        # 20+ variable detection & spatial parser
│   │   ├── missing_variable_detector.py # Dynamic missing context discovery
│   │   └── session_memory.py            # Segmented multi-turn context memory
│   ├── rag/
│   │   ├── chunker.py                   # Context-preserving scientific document chunker
│   │   ├── retriever.py                 # Hybrid vector retrieval & re-ranking engine
│   │   └── vector_store.py              # ChromaDB vector store wrapper
│   ├── reasoning/
│   │   ├── bottleneck_detector.py       # Ecological bottleneck discovery
│   │   ├── engine.py                    # Multi-metric causal reasoning engine (≥3 vars)
│   │   └── relationship_graph.py        # 29-node directed biophysical graph
│   ├── recommendations/
│   │   ├── generator.py                 # 10-point recommendation protocol generator
│   │   └── intervention_library.py      # Agroecological intervention catalog
│   ├── simulation/
│   │   ├── __init__.py
│   │   └── simulator.py                 # Biophysical simulation & transparent refusal engine
│   ├── services/
│   │   ├── confidence_service.py        # Factorized confidence scoring
│   │   ├── db_service.py                # SQLite persistence service
│   │   └── llm_service.py               # LLM integration & offline fallback
│   └── main.py                          # FastAPI application & lifespan startup seeder
├── data/
│   ├── chroma_db/                       # ChromaDB persistent collection
│   ├── darukaa_biodiversity.db          # SQLite persistent database
│   ├── knowledge/
│   │   └── scientific_knowledge_seed.json # 12 peer-reviewed source documents
│   └── processed/
│       └── knowledge_chunks.json        # Processed chunks
├── frontend/
│   └── streamlit_app.py                 # Fallback exploratory Streamlit dashboard
├── web/                                 # React 19 + TypeScript Command Console
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── vercel.json                      # Vercel deployment manifest
│   ├── .env.example
│   └── src/
│       ├── components/
│       │   ├── background/              # WebGL atmospheric shader & tactical grid
│       │   ├── hero/                    # 7-stage Reasoning HUD & mission banner
│       │   ├── scientist/               # Conversational scientist & missing context deck
│       │   ├── graph/                   # Interactive SVG causal relationship graph
│       │   ├── recommendations/         # 10-point protocol cards & metrics grid
│       │   ├── evidence/                # RAG evidence slide-over drawer
│       │   ├── simulator/               # Biophysical scenario simulator
│       │   ├── map/                     # Sentinel-2 multispectral HUD overlay
│       │   └── layout/                  # Top mission bar, sidebar, and footer
│       ├── services/
│       │   └── api.ts                   # Unified REST API client
│       └── types/                       # Pydantic-compatible TypeScript types
├── scripts/
│   ├── build_vector_index.py            # Vector re-indexing utility
│   ├── ingest_documents.py              # Full ingestion pipeline
│   └── seed_database.py                 # 5 benchmark observation cases seeder
├── tests/                               # 37 automated unit & integration tests
├── Dockerfile                           # Multi-stage production container
├── docker-compose.yml                   # Multi-service local stack
├── Procfile                             # Production process declaration
├── railway.json                         # Railway deployment configuration
├── render.yaml                          # Render infrastructure-as-code manifest
├── requirements.txt                     # Python dependencies
└── .env.example                         # Environment variable template
```

---

## 12. Database / Schema

### SQLite Relational Database (`data/darukaa_biodiversity.db`)
Managed by `app/services/db_service.py` with 3 core tables:
1. `observations`:
   - `id` (TEXT PRIMARY KEY): Unique identifier.
   - `data_json` (TEXT): Complete serialized `EnvironmentalState`.
   - `created_at` (TIMESTAMP): UTC recording time.
2. `conversations`:
   - `conversation_id` (TEXT PRIMARY KEY): UUID session identifier.
   - `accumulated_state_json` (TEXT): Cumulative environmental parameters.
   - `messages_json` (TEXT): Full dialogue trajectory.
   - `updated_at` (TIMESTAMP): Last activity time.
3. `sources`:
   - `document_id` (TEXT PRIMARY KEY): Source ID (e.g. `DOC-FAO-2020-GSOC`).
   - `title` (TEXT), `organization` (TEXT), `publication_year` (INTEGER), `citation` (TEXT), `url` (TEXT).

---

## 13. Local Installation

```bash
# 1. Clone repository
git clone https://github.com/clutchH1404/darukaa-biodiversity-ai.git
cd darukaa-biodiversity-ai

# 2. Set up Python virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Ingest knowledge base & seed database
python scripts/ingest_documents.py
python scripts/seed_database.py

# 5. Start FastAPI Backend (Port 8000)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 6. Start React Command Console (in a new terminal, Port 3000)
cd web
npm install
npm run dev
```

---

## 14. Environment Variables

All variables are defined with defaults in `.env.example`:

| Variable | Description | Secret? | Default |
| :--- | :--- | :--- | :--- |
| `APP_ENV` | Environment (`development` or `production`) | No | `development` |
| `PORT` / `API_PORT` | Backend listening port | No | `8000` |
| `FRONTEND_URL` | Deployed frontend URL for CORS | No | Empty (Local dev allowed) |
| `ALLOWED_ORIGINS` | Comma-separated CORS allowed origins | No | `http://localhost:3000,http://localhost:5173` |
| `OPENAI_API_KEY` | Optional LLM key (offline rules work without it) | **Yes** | Empty |
| `CHROMA_PERSIST_DIR`| Path to ChromaDB directory | No | `data/chroma_db` |
| `SQLITE_DB_PATH` | Path to SQLite database | No | `data/darukaa_biodiversity.db` |
| `VITE_API_URL` | (Frontend) Backend URL for API calls | No | Empty (uses local proxy) |

---

## 15. API Documentation

Interactive OpenAPI / Swagger documentation is available live at `http://localhost:8000/docs`.

### Key Endpoints:
- `GET /health`: Diagnostic metrics (`{"status": "healthy", "vector_store_documents": 12, ...}`).
- `POST /understand`: Accepts `{"query": "..."}`, returns detected variables, missing context questions, and spatial/temporal tags.
- `GET /graph`: Exports baseline directed biophysical graph (29 nodes, 26 edges).
- `POST /graph`: Accepts `{"environmental_state": {...}}`, returns state-calibrated biophysical graph with stress indicators.
- `POST /simulate`: Accepts `{"intervention_type": "...", "intensity": 0.75, "time_horizon_years": 5}`, returns empirical deltas.
- `POST /retrieve`: Accepts `{"query": "...", "environmental_variables": [...]}`, returns ranked evidence chunks with similarity scores.
- `POST /chat`: Primary conversational endpoint; takes message and environmental state, executes the full 7-stage pipeline, returns 10-point recommendations.
- `GET /session/{id}/context`: Segmented cumulative state across 7 domains.

---

## 16. Running with Docker

```bash
# Build and run backend + frontend stack
docker-compose up --build
```
- **Backend**: `http://localhost:8000`
- **Streamlit**: `http://localhost:8501`

---

## 17. Deployment Architecture

The application is architected for zero-maintenance production deployment:

### Backend Deployment (Render or Railway)
- **Manifest**: `render.yaml` or `railway.json` / `Procfile`.
- **Build Command**: `pip install -r requirements.txt && python scripts/ingest_documents.py && python scripts/seed_database.py`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Health Check Path**: `/health`

### Frontend Deployment (Vercel)
- **Root Directory**: `web`
- **Framework**: `Vite`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Manifest**: `web/vercel.json` (includes SPA rewrite rules)
- **Environment Variable**: `VITE_API_URL` set to the deployed backend URL.

---

## 18. Demo Scenarios

The system includes 4 judge demo scenarios:

1. **Amazon Basin Sector 04B** (`amazon-04b`):
   - *Observation*: Avian and pollinator biodiversity collapse, acute topsoil desiccation (0.3% SOC), buffer fragmentation.
   - *Reasoning*: Superimposes depleted carbon, water stress, and fragmentation; identifies that synthetic fertilizer would fail; prescribes multi-species cover crops and native hedgerows.
2. **Cerrado Agricultural Fringe** (`cerrado-c12`):
   - *Observation*: Topsoil compaction and SOC oxidation in soybean monoculture.
   - *Reasoning*: Disrupted mycorrhizal networks and 3.8x runoff increase; prescribes contour agroforestry and biological pest corridors.
3. **Rift Valley Water Deficit** (`rift-valley-water`):
   - *Observation*: Severe drought and upstream irrigation diversion drying wetlands.
   - *Reasoning*: Baseflow reduction (-61%) driving riparian collapse; prescribes micro-catchment swales and water retention recharge.
4. **Atlantic Forest Fragment #8** (`atlantic-fragment-8`):
   - *Observation*: Matrix isolation of arboreal primates in patches $<25$ ha.
   - *Reasoning*: Perimeter edge microclimate exposure (+240% tree mortality); prescribes riparian stepping stones and connectivity corridors.

---

## 19. Hackathon Evaluation Alignment

| Evaluation Area | System Implementation | Verification Evidence |
| :--- | :--- | :--- |
| **A. Depth of Reasoning** | Multi-metric reasoning engine enforcing $\ge 3$ coupled variables. Directed 29-node causal graph explaining feedback loops. | `app/reasoning/engine.py`, `app/reasoning/relationship_graph.py`, `test_multi_metric_reasoning.py` (Passed) |
| **B. Scientific Grounding** | Strictly zero hallucinated citations. Authentic citations from FAO (2020), IPCC (2019), IPBES (2019), Science (2020), Nature (2012). | `data/knowledge/scientific_knowledge_seed.json`, `app/recommendations/generator.py`, `test_citation_generation.py` (Passed) |
| **C. Knowledge System** | ChromaDB persistent vector store with 12 authoritative reports; hybrid semantic and variable overlap re-ranking. | `app/rag/retriever.py`, `app/rag/vector_store.py`, `test_rag_retrieval.py` (Passed) |
| **D. Conversational Intelligence** | Dynamic missing context detection; 20+ variable query parsing; segmented multi-turn session context. | `app/memory/query_understander.py`, `app/memory/session_memory.py`, `test_conversation_memory.py` (Passed) |
| **E. Output Clarity** | 10-point recommendation schema; 7-stage Reasoning HUD; interactive biophysical graph; empirical simulation engine. | `web/src/components/`, `app/simulation/simulator.py`, `test_api_endpoints.py` (Passed) |

---

## 20. Security

- **Prompt Injection Isolation**: `SecurityGuard.sanitize_user_input()` strips malicious delimiters and encloses RAG evidence within inert `<evidence_item>` tags.
- **CORS Protection**: Dynamic origin validation restricting production requests to authorized frontend domains.
- **Secret Hygiene**: Zero committed `.env` files; API keys and database credentials are read exclusively from environment variables.
- **Input Validation**: Strongly typed Pydantic models validate all JSON payloads against bounded ranges (e.g., pH 0–14, SOC 0–100%).

---

## 21. Testing

37 automated unit and integration tests covering all critical pipelines:
```bash
pytest -v tests/
```

- `test_api_endpoints.py`: All 12 REST API endpoints.
- `test_multi_metric_reasoning.py`: Causal graph traversal & $\ge 3$ variable enforcement.
- `test_missing_variable_detection.py`: Dynamic clarifying questions.
- `test_rag_retrieval.py`: Semantic vector search and hybrid re-ranking.
- `test_citation_generation.py`: Literature provenance validation.
- `test_hallucination_safeguards.py`: Prompt injection resistance.
- `test_environmental_cases.py`: The 5 official environmental benchmark cases.

---

## 22. Limitations

1. **Empirical Simulation Bounding**: Intervention simulation uses empirical transfer models from peer-reviewed literature. Speculative methods transparently return `"Simulation model unavailable"` to prevent fabricated predictions.
2. **Satellite Telemetry**: Multispectral Sentinel-2 layers are ingested as calibrated regional observations rather than real-time daily orbital streaming.

---

## 23. Future Scope

- Direct integration with Google Earth Engine API for automated real-time Sentinel-2 NDVI and surface temperature extraction.
- Edge deployment for offline field tablet use in remote agricultural cooperatives.
- Multi-lingual farmer interface supporting voice queries in regional dialects.

---

## 24. Hackathon Submission Links

- **GitHub Repository**: [https://github.com/clutchH1404/darukaa-biodiversity-ai](https://github.com/clutchH1404/darukaa-biodiversity-ai)
- **Local Web Console**: `http://localhost:3000`
- **FastAPI Documentation**: `http://localhost:8000/docs`
- **Streamlit Dashboard**: `http://localhost:8501`

---

**Developed for the Darukaa.Earth AI Biodiversity Intelligence Chatbot Challenge.**
