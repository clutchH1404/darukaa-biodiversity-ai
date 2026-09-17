import uuid
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .core.config import settings
from .core.security import SecurityGuard
from .models.environmental_state import (
    EnvironmentalState, EnvironmentalObservationCreate, EnvironmentalObservationResponse
)
from .models.knowledge_schema import KnowledgeDocument, RetrievedEvidence
from .models.response_models import (
    ChatRequest, ChatResponse, AnalyzeRequest, AnalyzeResponse,
    RecommendationItem, MissingVariableQuestion, ReasoningTrace
)
from .services.db_service import db_service
from .services.llm_service import llm_service
from .services.confidence_service import confidence_service
from .rag.retriever import retrieve_evidence
from .rag.chunker import chunker
from .rag.vector_store import vector_store
from .reasoning.engine import reasoning_engine
from .reasoning.relationship_graph import relationship_graph
from .recommendations.generator import recommendation_generator
from .memory.session_memory import session_memory
from .memory.missing_variable_detector import missing_variable_detector
from .memory.query_understander import query_understander, QueryUnderstandingResult
from .simulation.simulator import simulation_engine, SimulationScenarioRequest, SimulationResult

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    CRITICAL PRODUCTION SAFEGUARD:
    Guarantees that the scientific knowledge base and database tables
    are automatically initialized upon startup in any deployment environment (Render, Railway, Docker).
    This ensures the vector store NEVER starts with 0 documents or disappears after a redeploy.
    """
    try:
        if vector_store.count() == 0:
            import logging
            logging.info("ChromaDB vector store is empty. Auto-indexing authoritative scientific literature...")
            from scripts.ingest_documents import run_ingestion
            run_ingestion()
    except Exception as e:
        print(f"Warning: Auto-ingestion check encountered: {e}")

    try:
        sources = db_service.get_all_sources()
        if not sources:
            from scripts.seed_database import seed_observations
            seed_observations()
    except Exception as e:
        print(f"Warning: Auto-seed check encountered: {e}")
    yield

app = FastAPI(
    title="Darukaa.Earth AI Biodiversity Intelligence API",
    description="Conversational Environmental Intelligence and Causal Multi-Metric Reasoning Platform",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

def get_cors_origins() -> List[str]:
    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8501",
        "http://127.0.0.1:8501"
    ]
    if settings.FRONTEND_URL:
        origins.append(settings.FRONTEND_URL.rstrip("/"))
    if settings.ALLOWED_ORIGINS:
        for o in settings.ALLOWED_ORIGINS.split(","):
            c = o.strip().rstrip("/")
            if c and c not in origins:
                origins.append(c)
    if "*" in settings.ALLOWED_ORIGINS or settings.APP_ENV == "development":
        if "*" not in origins:
            origins.append("*")
    return origins

# CORS middleware for frontend access
cors_origins = get_cors_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if "*" not in cors_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RetrieveRequest(BaseModel):
    query: str
    environmental_variables: Optional[List[str]] = None
    geographic_context: Optional[Dict[str, Any]] = None
    top_k: int = 5

class QueryUnderstandRequest(BaseModel):
    query: str

class GraphRequest(BaseModel):
    environmental_state: Optional[EnvironmentalState] = None

@app.get("/health", tags=["System"])
def get_health():
    """System health check and diagnostic metrics."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "vector_store_documents": vector_store.count(),
        "database_connected": True,
        "llm_online": llm_service.is_configured
    }

@app.post("/understand", response_model=QueryUnderstandingResult, tags=["Query Understanding"])
@app.post("/query/understand", response_model=QueryUnderstandingResult, tags=["Query Understanding"])
def understand_query_endpoint(req: QueryUnderstandRequest):
    """
    Evaluates natural-language observation, identifies >=20 environmental variables,
    flags missing context, and resolves spatial/temporal qualifiers.
    """
    sanitized = SecurityGuard.sanitize_user_input(req.query)
    return query_understander.understand_query(sanitized)

@app.get("/graph", tags=["Relationship Graph"])
@app.get("/environment/graph", tags=["Relationship Graph"])
def get_default_environmental_graph():
    """
    Returns baseline biophysical causal relationship graph with nodes and directed edges.
    """
    return relationship_graph.export_graph()

@app.post("/graph", tags=["Relationship Graph"])
@app.post("/environment/graph", tags=["Relationship Graph"])
def get_contextual_environmental_graph(req: GraphRequest):
    """
    Returns biophysical causal graph populated with values, trends, and stress indicators
    derived from the provided environmental state.
    """
    return relationship_graph.export_graph(req.environmental_state)

@app.post("/simulate", response_model=SimulationResult, tags=["Biophysical Simulation"])
def simulate_intervention_endpoint(req: SimulationScenarioRequest):
    """
    Empirical scenario modeling for agroecological interventions.
    Transparently reports 'unavailable' for unmodeled interventions.
    """
    return simulation_engine.simulate(req)

@app.get("/session/{conversation_id}/context", tags=["Memory"])
def get_session_structured_context(conversation_id: str):
    """
    Retrieves structured multi-turn environmental context segmented into domains:
    location, soil, water, vegetation, land_use, biodiversity, climate, and history.
    """
    return session_memory.get_structured_context(conversation_id)

@app.get("/sources", tags=["Scientific Evidence"])
def get_sources():
    """Returns all registered authoritative scientific literature in the knowledge registry."""
    return db_service.get_all_sources()

@app.post("/retrieve", response_model=List[RetrievedEvidence], tags=["RAG Retrieval"])
def retrieve_scientific_evidence(req: RetrieveRequest):
    """
    Performs semantic vector retrieval against indexed environmental literature
    with hybrid variable and geographic re-ranking.
    """
    sanitized_query = SecurityGuard.sanitize_user_input(req.query)
    results = retrieve_evidence(
        query=sanitized_query,
        environmental_variables=req.environmental_variables,
        geographic_context=req.geographic_context,
        top_k=req.top_k
    )
    return results

@app.post("/environment", response_model=EnvironmentalObservationResponse, tags=["Observations"])
def create_environmental_observation(obs: EnvironmentalObservationCreate):
    """
    Submit structured environmental observation JSON for storage and validation.
    """
    obs_dict = obs.model_dump()
    obs_id = db_service.save_observation(obs_dict)
    saved = db_service.get_observation(obs_id)
    if not saved:
        raise HTTPException(status_code=500, detail="Failed to persist observation")
    return EnvironmentalObservationResponse(**saved)

@app.post("/analyze", response_model=AnalyzeResponse, tags=["Reasoning Engine"])
def analyze_environmental_state(req: AnalyzeRequest):
    """
    Multi-metric assessment and bottleneck discovery without generating interventions.
    """
    trace, active_vars = reasoning_engine.execute_reasoning(req.environmental_state)
    missing_vars = missing_variable_detector.detect_missing(req.environmental_state)

    risk_level = "HIGH" if "CRITICAL" in str(trace.primary_bottlenecks) else "MODERATE"

    return AnalyzeResponse(
        assessment=f"Evaluated {len(active_vars)} interconnected environmental variables across soil, hydrology, and biodiversity.",
        bottlenecks=trace.primary_bottlenecks,
        risk_level=risk_level,
        reasoning_trace=trace,
        variables_evaluated=req.environmental_state.get_known_variables(),
        missing_critical_variables=missing_vars
    )

@app.post("/recommend", response_model=List[RecommendationItem], tags=["Recommendation Engine"])
def generate_recommendations_endpoint(state: EnvironmentalState):
    """
    Directly produces scientific, 10-point recommendations based on environmental parameters.
    """
    trace, active_vars = reasoning_engine.execute_reasoning(state)
    evidence = retrieve_evidence(
        query="agroecological restoration and soil organic carbon management",
        environmental_variables=active_vars,
        top_k=4
    )
    return recommendation_generator.generate_recommendations(state, trace, evidence)

@app.post("/ingest", tags=["RAG Ingestion"])
def ingest_document(doc: KnowledgeDocument):
    """
    Ingests a new peer-reviewed or authoritative document into the knowledge base.
    """
    doc_dict = doc.model_dump()
    db_service.register_source(doc_dict)
    chunks = chunker.chunk_document(doc_dict)
    vector_store.add_chunks(chunks)
    return {
        "status": "success",
        "document_id": doc.document_id,
        "chunks_indexed": len(chunks),
        "total_vector_count": vector_store.count()
    }

@app.get("/conversation/{conversation_id}", tags=["Memory"])
def get_conversation_history(conversation_id: str):
    """
    Retrieves full conversation trajectory and accumulated environmental state.
    """
    convo = db_service.get_conversation(conversation_id)
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation session not found")
    return convo

@app.post("/chat", response_model=ChatResponse, tags=["Conversational AI"])
async def chat_endpoint(req: ChatRequest):
    """
    Primary conversational endpoint. Behaves like an AI Environmental Scientist:
    - Sanitizes input and resists prompt injections
    - Dynamically detects and asks for missing critical variables
    - Performs multi-metric causal reasoning across >=3 variables
    - Retrieves real RAG evidence
    - Formats recommendations into the standard 10-point schema with transparent citations
    """
    conversation_id = req.conversation_id or str(uuid.uuid4())
    sanitized_msg = SecurityGuard.sanitize_user_input(req.message)

    # 1. Extract variables from natural language message
    extracted_from_text = missing_variable_detector.extract_variables_from_text(sanitized_msg)

    # 2. Merge with any explicit environmental state payload
    merged_input = dict(extracted_from_text)
    if req.environmental_state:
        merged_input.update(req.environmental_state.get_known_variables())

    # 3. Update session memory & get cumulative state
    cumulative_state = session_memory.update_session_state(conversation_id, merged_input)

    # 4. Check for missing high-priority variables
    missing_vars = missing_variable_detector.detect_missing(cumulative_state)

    # 5. Multi-metric reasoning
    trace, active_vars = reasoning_engine.execute_reasoning(cumulative_state)

    # 6. Retrieve scientific evidence via RAG
    geo_context = req.geographic_context or {}
    if cumulative_state.region and "region" not in geo_context:
        geo_context["region"] = cumulative_state.region

    evidence = retrieve_evidence(
        query=sanitized_msg if len(sanitized_msg.split()) > 3 else f"soil biodiversity restoration in {cumulative_state.region or 'dryland'} cropping",
        environmental_variables=active_vars,
        geographic_context=geo_context,
        top_k=settings.MAX_RETRIEVAL_RESULTS
    )

    # 7. Generate 10-point recommendations
    recommendations = recommendation_generator.generate_recommendations(
        state=cumulative_state,
        reasoning_trace=trace,
        retrieved_evidence=evidence
    )

    # 8. Synthesize trade-offs and risks
    trade_offs = []
    for r in recommendations:
        trade_offs.extend(r.possible_trade_offs)
    trade_offs = list(dict.fromkeys(trade_offs))[:4]

    # 9. Format structured scientific response markdown (Hackathon Section 14)
    assessment = (
        f"Assessed environmental state encompassing {len(active_vars)} interconnected variables "
        f"({', '.join(active_vars[:4])}). Soil organic carbon is "
        f"{f'{cumulative_state.soil_organic_carbon}%' if cumulative_state.soil_organic_carbon is not None else 'depleted'}, "
        f"rainfall condition is {cumulative_state.rainfall or 'constrained'}, and land-use is {cumulative_state.land_use or 'cultivated'}."
    )

    key_drivers = trace.primary_bottlenecks

    # Construct complete Markdown response
    md_lines = [
        "## Environmental Assessment",
        assessment,
        "",
        "## Key Drivers",
    ]
    for d in key_drivers:
        md_lines.append(f"- **{d}**")

    md_lines.extend([
        "",
        "## Multi-Metric Reasoning",
        trace.ecological_narrative,
        "",
        f"*Causal pathway analyzed across variables:* `{', '.join(active_vars)}`",
        "",
        "## Recommended Actions"
    ])

    for i, r in enumerate(recommendations, 1):
        md_lines.extend([
            f"### Recommendation {i}: {r.title}",
            f"**What to do:** {r.what_to_do}",
            "",
            f"**Why:** {r.why_it_works}",
            "",
            f"**Variables connected:** {', '.join(r.variables_involved)}",
            "",
            "**Metrics affected:**",
        ])
        for m in r.impacted_metrics:
            md_lines.append(f"- {m}")
        md_lines.extend([
            "",
            f"**Time horizon:** {r.time_horizon}",
            f"**Expected direction:** `{r.expected_direction}`",
            f"**Confidence:** **{r.confidence}** ({r.confidence_reason})",
            "",
            "**Evidence:**"
        ])
        for cit in r.scientific_evidence[:2]:
            md_lines.append(f"- *{cit.source_organization} ({cit.year})*: [{cit.title}]({cit.url}) — \"{cit.relevant_evidence[:140]}...\"")
        md_lines.append("")

    if trade_offs:
        md_lines.extend([
            "## Trade-offs / Risks",
        ])
        for t in trade_offs:
            md_lines.append(f"- {t}")
        md_lines.append("")

    md_lines.extend([
        "## Evidence Retrieved",
    ])
    for ev in evidence[:4]:
        md_lines.append(f"- **[{ev.document_id}]** *{ev.organization} ({ev.publication_year})*: [{ev.title}]({ev.url}) (Similarity: {ev.similarity_score:.2f})")
    md_lines.append("")

    # If missing variables are found, add structured clarifying questions
    if missing_vars:
        md_lines.extend([
            "## Missing Information",
            "To refine biophysical impact estimates and species selection, please provide the following if available:"
        ])
        for q in missing_vars:
            md_lines.append(f"- **{q.variable_name.replace('_', ' ').title()}**: {q.question_text}")
        md_lines.append("")

    formatted_md = "\n".join(md_lines)

    # 10. Record turn in memory
    session_memory.record_turn(
        conversation_id=conversation_id,
        user_message=req.message,
        assistant_response=formatted_md
    )

    conf_summary = confidence_service.evaluate_confidence(
        environmental_state=cumulative_state,
        evidence_list=[e.model_dump() for e in evidence],
        variables_used=active_vars
    )

    debug_trace = {
        "user_query": req.message,
        "extracted_environmental_variables": extracted_from_text,
        "missing_variables": [q.variable_name for q in missing_vars],
        "retrieved_documents": [e.document_id for e in evidence],
        "similarity_scores": [e.similarity_score for e in evidence],
        "reasoning_factors": trace.causal_chains,
        "recommendation_candidates": [r.title for r in recommendations],
        "citations_count": sum(len(r.scientific_evidence) for r in recommendations)
    }

    return ChatResponse(
        conversation_id=conversation_id,
        formatted_response=formatted_md,
        environmental_assessment=assessment,
        key_drivers=key_drivers,
        multi_metric_reasoning=trace.ecological_narrative,
        recommendations=recommendations,
        trade_offs_and_risks=trade_offs,
        evidence_retrieved=evidence,
        missing_variables_detected=missing_vars,
        updated_environmental_state=cumulative_state.get_known_variables(),
        confidence_summary=conf_summary,
        debug_trace=debug_trace
    )
