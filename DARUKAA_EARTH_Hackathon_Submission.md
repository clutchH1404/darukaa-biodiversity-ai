DARUKAA.EARTH

AI Biodiversity Intelligence System & Causal Reasoning Engine

Official Submission Document — AI Biodiversity Intelligence Chatbot Challenge

Executive Command Console Interface

Figure 1: Darukaa.Earth Production Console — 7-Stage Reasoning HUD, Multi-Metric Sliders, Causal Graph, and 10-Point Actionable Protocols.

1. Project Overview

Darukaa.Earth is an enterprise-grade AI environmental scientist and biosphere intelligence platform engineered specifically for the Darukaa.Earth AI Biodiversity Intelligence Chatbot Challenge. The system transforms unstructured field observations and quantitative telemetry into grounded, verifiable, multi-variable ecological interventions.

Unlike generic consumer chatbots that produce single-variable, surface-level advice, Darukaa.Earth executes a 7-stage deterministic reasoning pipeline. It extracts over 20 distinct biophysical variables, actively queries the user for critical missing context before prescribing treatments, retrieves authoritative peer-reviewed evidence from a curated ChromaDB knowledge base, traverses a 29-node directed causal biophysical graph, projects empirical outcomes across 1 to 5-year horizons, and formats recommendations according to a rigorous 10-point actionable protocol.

2. Problem Statement

Modern agricultural and land-management practices face accelerating ecological degradation, including soil carbon loss, water table exhaustion, and wild pollinator collapse. Land managers and conservationists seeking AI guidance encounter three severe failure modes with conventional Large Language Models:

1. Single-Variable Reductionism: Generative models offer simplistic advice like 'nitrogen is low -> apply synthetic N', ignoring that synthetic fertilizers disrupt soil mycorrhizal networks, drive groundwater eutrophication, and fail under low soil organic carbon.
2. Hallucinated Citations: LLMs routinely invent fake academic authors, fictional DOI numbers, and exaggerated recovery percentages.
3. Blind Extrapolation: Recommending moisture-demanding cover crops in arid drylands without termination protocols leads to crop water starvation.

3. Proposed Solution

Darukaa.Earth resolves these failure modes through an auditable, hybrid neuro-symbolic architecture:

• Directed Causal Biophysical Graph: A formal network of 29 biophysical nodes and 26 verified directional relationships modeling ecological feedback loops (e.g., Soil Organic Carbon <-> Water Infiltration Rate <-> Mycorrhizal Guilds).
• Missing Context Interrogation: Rather than guessing critical unstated variables, the system calculates a completeness score and proactively prompts the practitioner for vital telemetry (e.g., soil pH, rainfall regime, land slope).
• Zero-Hallucination Knowledge Retrieval: All recommendations are grounded in 12 authoritative, peer-reviewed global reports (FAO, IPCC, IPBES, Science, Nature) indexed in ChromaDB.
• Bounded Empirical Simulation: An onboard non-linear simulator projects delta changes in SOC (%), water capacity (mm/m), and biodiversity index over multi-year horizons.

4. Key Features

5. System Architecture

Darukaa.Earth employs a decoupled, production-hardened microservice architecture optimized for zero-maintenance deployment:

+-------------------------------------------------------------------------+
|                     CLIENT LAYER: Vercel Cloud                          |
|  React 19 + TypeScript + Vite 6 + Tailwind CSS SPA                      |
|  • 7-Stage Reasoning HUD    • Interactive Causal Graph                 |
|  • Biophysical Sliders      • 10-Point Recommendation Cards            |
+-------------------------------------------------------------------------+
                                     | HTTPS (REST API)
                                     v
+-------------------------------------------------------------------------+
|                    BACKEND LAYER: Render Cloud                          |
|  FastAPI + Uvicorn Async Python 3.11.9 Engine                           |
|  [Security Guard] -> Input Sanitization & Prompt Injection Defense      |
|  [Query Understander] -> 20+ Variable Extraction & Missing Context      |
|  [Session Memory] -> SQLite Dynamic Context Accumulation                |
|  [RAG Pipeline] -> ChromaDB Semantic Retrieval & Keyword Reranker       |
|  [Reasoning Engine] -> 29-Node Causal Biophysical Graph Traversal       |
|  [Simulator] -> Non-linear Empirical Trajectory Projection             |
|  [Recommendation Generator] -> 10-Point Operational Protocol Synthesis  |
+-------------------------------------------------------------------------+
            |                                              |
            v                                              v
+-------------------------------+             +---------------------------+
|   ChromaDB Vector Database    |             |  SQLite Database Service  |
|  12 Peer-Reviewed Documents   |             |  Sessions, Contexts, Log  |
|  Auto-Indexed on Lifespan     |             |  Scientific Sources DB    |
+-------------------------------+             +---------------------------+

6. AI / RAG Pipeline

The AI pipeline processes every user query through 7 deterministic stages:

Stage 1: Observation Ingestion — Parses natural language observations and extracts quantitative parameters.
Stage 2: Missing-Variable Interrogation — Calculates parameter coverage score against a 20-variable taxonomy. If critical baseline data is missing, generates clarifying questions.
Stage 3: Vector Knowledge Retrieval — Executes hybrid semantic retrieval against ChromaDB. Chunks are scored via cosine distance and boosted by variable overlap with the active query.
Stage 4: Multi-Metric Causal Synthesis — Evaluates relationships across soil, water, biodiversity, and land use. Applies mathematical rules from the 29-node biophysical graph.
Stage 5: Non-linear Impact Simulation — Computes empirical deltas for SOC (%), water holding capacity (mm/m), and pollinator abundance across 1, 3, and 5-year horizons.
Stage 6: 10-Point Recommendation Formulation — Synthesizes concrete operational protocols complete with trade-offs, monitoring intervals, and authentic citations.
Stage 7: Response Structuring & Session State Update — Encodes recommendations into verified JSON schema and commits observations to session memory.

7. Scientific Knowledge System

To enforce the hackathon's strict scientific grounding mandate, Darukaa.Earth indexes 12 authentic, peer-reviewed publications from premier environmental organizations. No citations or findings are fabricated.

8. Multi-Metric Reasoning

The hackathon explicitly requires the AI Environmental Scientist to reason across multiple environmental variables rather than issuing single-variable fixes. Darukaa.Earth formally links variables through coupled causal equations:

• Soil Health <-> Water Availability: Every 1% increase in Soil Organic Matter stores an additional 144,000 liters of plant-available water per hectare. Soil compaction reduces infiltration by up to 70%, amplifying surface runoff.
• Water Availability <-> Species Survival: Water stress elevates sap viscosity and lowers nectar production, triggering nutritional deficits in native insect pollinators and collapsing seed set.
• Land Use <-> Habitat Fragmentation: Monoculture acreage with <10% natural vegetation boundaries increases edge effects, raising canopy temperatures and accelerating localized species extinctions.

9. Conversational Intelligence

The conversational engine in Darukaa.Earth maintains state through structured session context. When an incomplete observation is submitted (e.g., 'My corn yield is down and soil is dry'), the Query Understanding module identifies missing variables (rainfall history, slope, current cover crop status) and poses targeted clarifying questions. As the user responds in subsequent conversation turns, the system dynamically merges previous telemetry with new inputs, preserving context across the entire consultation.

10. Recommendation Output

Every recommendation generated by Darukaa.Earth adheres to a 10-point actionable specification:

1. Specific Operational Action (exact agroecological procedure)
2. Biophysical Mechanism (how the biological/physical system responds)
3. Quantitative Metric Impact (target delta in SOC, moisture, or biodiversity)
4. Projected Time Horizon (Immediate <3mo, Intermediate 1-3yr, Strategic 5yr)
5. Ecological & Operational Trade-offs (labor demands, moisture consumption during establishment)
6. Required Monitoring Indicators (measurable verification parameters)
7. Confidence Score (derived from scientific evidence density, 0.0 - 1.0)
8. Authentic Scientific Citation (Author, Organization, Year, Publication)
9. Implementation Readiness Tier (Immediate, Conditional on Rain, Phased)
10. Co-Benefits Profile (carbon sequestration, groundwater recharge, pest suppression)

11. Technology Stack

12. Database / Schema

The relational layer uses SQLite (`data/darukaa_biodiversity.db`) for lightweight, zero-latency state management:

13. API Architecture

14. Local Setup & Installation

To run Darukaa.Earth locally for evaluation or development:

# 1. Clone Repository
git clone https://github.com/clutchH1404/darukaa-biodiversity-ai.git
cd darukaa-biodiversity-ai

# 2. Python Virtual Environment
python -m venv .venv
.venv\Scripts\activate  # Windows (or: source .venv/bin/activate on Linux/macOS)
pip install -r requirements.txt

# 3. Seed Knowledge Base and SQLite Database
python scripts/ingest_documents.py
python scripts/seed_database.py

# 4. Launch FastAPI Backend (Port 8000)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 5. Launch React Console (In a new terminal, Port 3000)
cd web
npm install
npm run dev

15. Environment Variables

All variables are documented in `.env.example` with zero secrets committed:

16. CI/CD & Deployment

Darukaa.Earth features continuous automated deployment triggered by Git push to `main`:

• Backend (Render Cloud): Managed via `render.yaml` infrastructure-as-code blueprint. Upon push, Render pulls Python 3.11.9, executes document ingestion, and launches uvicorn. Ephemeral restarts automatically re-index the 12 scientific papers via the FastAPI lifespan context manager in under 1.5 seconds.
• Frontend (Vercel Cloud): Managed via `web/vercel.json` and root `vercel.json`. Configured with SPA rewrite rules (`/(.*) -> /index.html`) and asset caching headers (`max-age=31536000`). Root `.vercelignore` strictly prevents Vercel from attempting to bundle or execute Python backend dependencies.
• Automated Test Suite: GitHub Actions CI workflow runs pytest across Python 3.11, 3.12, and 3.14 on every commit.

17. Judge Demo Scenarios

Four comprehensive ecological crisis presets are built into the Command Console for instant judging evaluation:

18. Testing & Verification

The project includes 37 automated unit and integration tests executed with pytest. All tests pass with zero failures.

19. Security Audit & Hardening

Darukaa.Earth implements defense-in-depth security standards:

• Zero Secrets in Source Code: All configuration is managed via environment variables. `.gitignore` strictly excludes `.env`, `node_modules`, `.venv`, and `.db` binaries.
• Regex-Constrained CORS: Rather than a permissive wildcard, the backend restricts CORS to `https://*.vercel.app` and local debugging ports.
• Input Sanitization: `SecurityGuard.sanitize_user_input()` intercepts SQL injection strings, script injection tags, and adversarial prompt injections.
• Deterministic Offline Execution: The platform does not require an active external LLM API key to perform multi-metric reasoning or generate grounded recommendations.

20. Limitations & Future Scope

Transparently Disclosed Limitations:
1. Geographic Specialization: The current knowledge base emphasizes tropical and semi-arid agroecosystems (Amazon, Cerrado, Sub-Saharan drylands). Boreal and polar tundra ecosystems require additional literature indexing.
2. Simulation Linearity Bounds: While empirical non-linear decay curves are used, extreme multi-year climate tipping points (e.g., total monsoon failure) require coupling with GCM satellite models.

Future Scope:
• Direct Sentinel-2 / Landsat NDVI satellite raster ingestion for real-time spatial vegetation anomaly detection.
• On-farm IoT sensor streaming (LoRaWAN soil moisture probes) feeding real-time telemetry into the causal graph.
• Expansion of ChromaDB vector corpus to 5,000+ open-access agroecology papers via automated arXiv / BioRxiv scrapers.

21. Hackathon Evaluation Alignment

22. Final Submission Checklist

[x] GitHub Repository Created & Pushed with Clean History

[x] Production Backend Deployed & Verified Live on Render Cloud

[x] Production Frontend Configured & Build Tested for Vercel Cloud

[x] ChromaDB Vector Store Seeded with 12 Peer-Reviewed Scientific Papers

[x] Startup Lifespan Auto-Ingestion Configured for Ephemeral Restarts

[x] Multi-Metric Causal Reasoning Engine Connecting >=3 Environmental Variables

[x] Missing-Variable Detection and Clarifying Question Formulation

[x] Rigorous 10-Point Operational Recommendation Protocol Specification

[x] Zero Hardcoded Localhost URLs in Production Client Code

[x] Defense-in-Depth Input Sanitization & Prompt Injection Protection

[x] All 37 Automated Pytest Unit & Integration Tests Passing (100% Pass Rate)

[x] Production Vite React Build Succeeds with 0 Errors

[x] Professional Hackathon Submission Word Document Generated (.docx)

| VERIFIED PROJECT SUBMISSION LINKS:
• GitHub Repository: https://github.com/clutchH1404/darukaa-biodiversity-ai
• Production Live Demo: https://darukaa-biodiversity-ai.vercel.app
• Production Backend API: https://darukaa-biodiversity-backend.onrender.com
• Interactive Swagger Docs: https://darukaa-biodiversity-backend.onrender.com/docs
• API Health Verification: https://darukaa-biodiversity-backend.onrender.com/health |
| --- |

| Feature Category | Implemented Capability | Challenge Alignment |
| --- | --- | --- |
| Conversational Intelligence | Multi-turn session memory maintaining cumulative ecological state across 7 categories. | Context preservation across long consultations |
| Missing-Variable Detection | Identifies incomplete queries (<60% coverage) and generates clarifying questions. | Prevents hazardous actions based on partial data |
| RAG Knowledge Retrieval | ChromaDB vector store with 12 authentic papers; semantic search + keyword re-ranking. | Strict zero-hallucination policy with verifiable DOIs |
| Multi-Metric Reasoning | Simultaneously balances >=3 coupled variables (Soil Health, Water, Biodiversity, Land Use). | Core hackathon mandate for holistic systems modeling |
| 10-Point Protocols | Standardized output: Action, Mechanism, Metrics, Horizon, Trade-offs, Scientific Citation. | Actionable, auditable operational recommendations |
| Intervention Simulator | Non-linear biophysical equations simulating 1-5 year recovery trajectory. | Quantitative prediction of regenerative interventions |
| Causal Graph Viewer | Interactive 29-node directed graph visualizing active ecological stress pathways. | Deep explainability for agricultural practitioners |
| Judge Demo Presets | 4 pre-configured real-world ecological emergency cases (Amazon, Cerrado, Rift Valley, Atlantic Forest). | Instant reproducibility during judging evaluation |

| Doc ID | Authoritative Source | Domain | Key Scientific Grounding |
| --- | --- | --- | --- |
| DOC-FAO-2020-GSOC | FAO (2020) Recarbonizing Global Soils | Soil Health | Crop residue retention + diverse cover crops increase SOC by 0.2-0.8 t C/ha/yr. |
| DOC-IPCC-2019-SRCCL | IPCC (2019) Climate Change and Land | Climate & Land | Conservation agriculture with mulch reduces soil surface evaporation by 20-35%. |
| DOC-IPBES-2019-GLOBAL | IPBES (2019) Global Biodiversity Assessment | Biodiversity | 75% of terrestrial environment severely altered; wild pollinators require floral buffers. |
| DOC-NATURE-2012-TILMAN | Tilman et al. (Nature 2012) | Biodiversity | High plant species richness enhances drought resistance and biomass stability. |
| DOC-SCIENCE-2020-DIAZ | Díaz et al. (Science 2020) | Ecosystem Services | Functional diversity across trophic levels stabilizes ecosystem resilience. |
| DOC-FAO-2018-AGROECO | FAO (2018) Agroecology 10 Elements | Agroecology | Diversified crop rotations and livestock integration maximize circular bio-economy. |

| Layer | Technology | Version | Production Role |
| --- | --- | --- | --- |
| Frontend UI | React + TypeScript | 19.0.0 | Reactive command console with 7-stage Reasoning HUD |
| Styling | Tailwind CSS | 3.4.17 | High-density dark-mode environmental command aesthetics |
| Frontend Build | Vite | 6.4.3 | Optimized production bundle with SPA rewriting |
| Backend API | FastAPI + Uvicorn | 0.115.0 | Asynchronous high-performance REST API |
| Data Validation | Pydantic | 2.10.6 | Strict runtime schema enforcement and validation |
| Vector Database | ChromaDB | 0.6.3 | Persistent document embedding storage and semantic search |
| Relational DB | SQLite / SQLAlchemy | 3.x / 2.0.38 | Session state, conversation history, and scientific sources |
| AI / LLM Layer | OpenAI / Claude API | v1 / v3 | LLM reasoning with offline rule-based deterministic fallback |
| Backend Cloud | Render Web Service | Python 3.11.9 | Auto-indexing container with dynamic PORT and health checks |
| Frontend Cloud | Vercel | Vite Framework | Global edge CDN with automated HTTPS and asset caching |

| Table Name | Primary Purpose | Key Columns | Relationships |
| --- | --- | --- | --- |
| sessions | Tracks active user sessions | id, created_at, last_active, user_metadata | 1-to-many with messages & contexts |
| messages | Chronological chat history | id, session_id, role, content, timestamp, token_count | Belongs to session |
| session_contexts | Segmented cumulative ecological state | id, session_id, soil_data, climate_data, vegetation_data | Belongs to session |
| sources | Master catalog of scientific papers | id, doc_id, title, organization, year, doi, verified | Referenced by recommendations |
| interventions | Catalog of tested ecological interventions | id, name, domain, intensity, expected_soc_delta, citations | Used in simulation engine |

| Method | Endpoint | Functionality | Status on Render |
| --- | --- | --- | --- |
| GET | / | Root discovery path returning service metadata and documentation links | 200 OK Live |
| GET | /health | Health diagnostic returning vector doc count and DB status | 200 OK Live |
| POST | /understand | Parses query, extracts 20+ variables, generates missing questions | 200 OK Live |
| GET | /graph | Returns default 29-node biophysical directed causal relationship graph | 200 OK Live |
| POST | /graph | Returns state-calibrated graph with active stress paths highlighted | 200 OK Live |
| POST | /simulate | Runs non-linear empirical simulation across 1-5 year horizons | 200 OK Live |
| POST | /retrieve | ChromaDB hybrid retrieval returning ranked evidence chunks with scores | 200 OK Live |
| POST | /chat | Primary conversational endpoint executing full 7-stage reasoning flow | 200 OK Live |
| GET | /sources | Returns catalog of peer-reviewed scientific sources and DOIs | 200 OK Live |
| GET | /session/{id}/context | Fetches segmented multi-turn context across 7 categories | 200 OK Live |

| Variable Name | Description | Required? | Default Value |
| --- | --- | --- | --- |
| APP_ENV | Runtime environment (development | production) | No | development |
| PORT | Listening port for uvicorn (Render sets dynamically) | No | 8000 |
| FRONTEND_URL | Target frontend URL for CORS origin allowance | No | https://darukaa-biodiversity-ai.vercel.app |
| ALLOWED_ORIGINS | Comma-separated CORS origins (wildcards supported) | No | https://*.vercel.app,http://localhost:3000 |
| OPENAI_API_KEY | Optional LLM key (offline deterministic mode operates if empty) | No | None (Fully functional offline) |
| CHROMA_PERSIST_DIR | Storage path for ChromaDB vector embeddings | No | data/chroma_db |
| VITE_API_URL | Frontend environment variable targeting Render backend | Yes (Prod) | https://darukaa-biodiversity-backend.onrender.com |

| Scenario Name | Region & Context | Environmental Crisis | Prescribed 10-Point Protocol |
| --- | --- | --- | --- |
| Amazon Basin Sector 04B | Amazon Basin (Brazil) | SOC depleted to 0.3%, water retention -58%, severe pollinator habitat loss. | Multi-species legume cover crop + riparian hedgerow buffer + biochar retention swales. |
| Cerrado Fringe C-12 | Cerrado Savannah (Brazil) | Heavy topsoil compaction, runoff +280%, monoculture soybean soil oxidation. | Contour subsoiling without inversion + native perennial corridor + mycorrhizal inoculation. |
| Rift Valley Water Deficit | Rift Valley (East Africa) | Baseflow dried by upstream extraction, severe drought, wetland shrinkage. | Micro-catchment check dams + vetiver grass contour hedges + rainwater recharge wells. |
| Atlantic Forest Fragment #8 | Atlantic Forest (Brazil) | Isolated forest patches <25ha, severe canopy edge drying, tree mortality +240%. | Riparian stepping-stone reforestation + native fruit canopy corridors for primate transit. |

| Test Suite File | Test Count | Key Verifications | Result |
| --- | --- | --- | --- |
| test_api_endpoints.py | 11 tests | /health, /understand, /graph, /simulate, /retrieve, /chat, /sources | 11/11 PASSED |
| test_citation_generation.py | 2 tests | Verifies that citations reference authentic DOIs and real organizations | 2/2 PASSED |
| test_conversation_memory.py | 2 tests | Tests multi-turn context accumulation and session state retention | 2/2 PASSED |
| test_environmental_cases.py | 5 tests | Validates the 4 judge demo emergency scenarios and preset loading | 5/5 PASSED |
| test_hallucination_safeguards.py | 3 tests | Ensures zero hallucinated citations and rejection of prompt injections | 3/3 PASSED |
| test_json_validation.py | 4 tests | Pydantic v2 schema compliance for all request and response models | 4/4 PASSED |
| test_missing_variable_detection.py | 3 tests | Evaluates incomplete query scoring and clarifying question generation | 3/3 PASSED |
| test_multi_metric_reasoning.py | 3 tests | Enforces simultaneous coupling of >=3 biophysical variables | 3/3 PASSED |
| test_rag_retrieval.py | 3 tests | Tests ChromaDB cosine distance ranking and variable overlap boosting | 3/3 PASSED |
| test_recommendations.py | 1 test | Verifies 10-point recommendation schema compliance and trade-off fields | 1/1 PASSED |

| Evaluation Area | How DARUKAA.EARTH Solves It | Verification File |
| --- | --- | --- |
| A. Depth of Reasoning | Multi-metric causal engine coupling >=3 environmental variables through a 29-node directed graph. | app/reasoning/engine.py |
| B. Scientific Grounding | Strict zero-hallucination policy. 12 peer-reviewed publications from FAO, IPCC, IPBES, Nature, Science. | data/knowledge/scientific_knowledge_seed.json |
| C. Knowledge System | ChromaDB vector store with hybrid semantic retrieval and variable-overlap re-ranking. | app/rag/retriever.py |
| D. Conversational Intelligence | Missing-variable interrogation; 20+ variable query parsing; multi-turn context accumulation. | app/memory/query_understander.py |
| E. Output Clarity | Rigorous 10-point actionable protocol cards, 7-stage Reasoning HUD, and interactive graph. | web/src/components/RecommendationCard.tsx |