import os
import sys
import json
import uuid
import streamlit as st
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import settings
from app.models.environmental_state import EnvironmentalState
from app.reasoning.engine import reasoning_engine
from app.rag.retriever import retrieve_evidence
from app.recommendations.generator import recommendation_generator
from app.services.confidence_service import confidence_service
from app.services.db_service import db_service
from app.memory.session_memory import session_memory
from app.memory.missing_variable_detector import missing_variable_detector

from frontend.styles import DARK_THEME_CSS
from frontend.components.charts import (
    render_soil_health_chart,
    render_biodiversity_indicators,
    render_relationship_graph
)
from frontend.components.debug_panel import render_debug_observability_panel

# Set page config
st.set_page_config(
    page_title="DARUKAA.EARTH | AI Biodiversity Intelligence",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply CSS
st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)

# Initialize Session State
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_env_state" not in st.session_state:
    st.session_state.current_env_state = {
        "region": "semi-arid",
        "soil_organic_carbon": 0.3,
        "soil_ph": 6.8,
        "soil_moisture": 18.0,
        "rainfall": "low",
        "land_use": "monoculture wheat",
        "monoculture_or_polyculture": "monoculture",
        "temperature": 31.0,
        "species_richness": "low",
        "pollinator_presence": "low",
        "pollution_level": "moderate"
    }
if "latest_response" not in st.session_state:
    st.session_state.latest_response = None
if "latest_debug" not in st.session_state:
    st.session_state.latest_debug = None
if "active_demo_flow" not in st.session_state:
    st.session_state.active_demo_flow = False

# App Header
st.markdown("""
<div class="darukaa-header">
    <div class="darukaa-title">🌿 DARUKAA.EARTH</div>
    <div class="darukaa-subtitle">AI Biodiversity & Environmental Intelligence System — Multi-Metric Causal Reasoning & Authoritative RAG</div>
    <div style="margin-top: 10px;">
        <span class="badge badge-emerald">FAO / IPCC / IPBES Grounded</span>
        <span class="badge badge-cyan">Multi-Metric Causal Graph (≥3 Variables)</span>
        <span class="badge badge-amber">Anti-Hallucination Guardrails</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Hackathon Demo Mode Bar
demo_col1, demo_col2 = st.columns([3, 1])
with demo_col1:
    st.info("💡 **Hackathon Evaluator Quick-Start**: Click the Demo Scenario button to automatically execute the official benchmark scenario: *Semi-Arid Monoculture Wheat (0.3% SOC, Low Rainfall, Low Biodiversity)*.")
with demo_col2:
    if st.button("🚀 Run Hackathon Demo Scenario", use_container_width=True, type="primary"):
        st.session_state.current_env_state = {
            "region": "semi-arid",
            "soil_organic_carbon": 0.3,
            "soil_ph": 6.8,
            "soil_moisture": 18.0,
            "rainfall": "low",
            "rainfall_variability": "high",
            "land_use": "monoculture wheat",
            "monoculture_or_polyculture": "monoculture",
            "temperature": 31.0,
            "species_richness": "low",
            "pollinator_presence": "low",
            "pollution_level": "moderate",
            "drought_condition": "active"
        }
        st.session_state.active_demo_flow = True
        st.rerun()

# Visibly demonstrate pipeline if Demo is active
if st.session_state.active_demo_flow:
    st.markdown("### ⚡ Live Causal Pipeline Execution")
    cols = st.columns(8)
    steps = [
        "1. USER INPUT",
        "2. ENV STATE",
        "3. MISSING CHECK",
        "4. CAUSAL REASONING",
        "5. RAG RETRIEVAL",
        "6. EVIDENCE RANKING",
        "7. 10-PT RECOMMENDATIONS",
        "8. CONFIDENCE"
    ]
    for col, step in zip(cols, steps):
        col.markdown(f'<div class="pipeline-step">{step}</div>', unsafe_allow_html=True)
    st.divider()

# Sidebar: Environmental Profile & Input Methods
with st.sidebar:
    st.subheader("📊 1. Environmental Profile")
    
    tab_form, tab_json = st.tabs(["Sliders & Form", "Structured JSON"])
    
    with tab_form:
        soc_input = st.slider("Soil Organic Carbon (% SOC)", 0.1, 5.0, float(st.session_state.current_env_state.get("soil_organic_carbon") or 0.3), 0.1)
        ph_input = st.slider("Soil pH", 4.0, 9.5, float(st.session_state.current_env_state.get("soil_ph") or 6.8), 0.1)
        moist_input = st.slider("Soil Moisture (%)", 5.0, 60.0, float(st.session_state.current_env_state.get("soil_moisture") or 18.0), 1.0)
        temp_input = st.slider("Temperature (°C)", 5.0, 45.0, float(st.session_state.current_env_state.get("temperature") or 31.0), 1.0)
        
        rainfall_input = st.selectbox("Rainfall Level", ["low", "moderate", "high"], index=0 if st.session_state.current_env_state.get("rainfall") == "low" else 1)
        land_use_input = st.selectbox("Land-Use Type", ["monoculture wheat", "crop rotation", "agroforestry", "pasture"], index=0)
        mono_poly = st.selectbox("System Structure", ["monoculture", "polyculture"], index=0)
        richness_input = st.selectbox("Species Richness", ["low", "moderate", "high"], index=0)
        pollinator_input = st.selectbox("Pollinator Presence", ["low", "moderate", "high"], index=0)
        region_input = st.text_input("Region / Climate Zone", value=st.session_state.current_env_state.get("region") or "semi-arid")

        if st.button("Apply Form Parameters", use_container_width=True):
            st.session_state.current_env_state.update({
                "soil_organic_carbon": soc_input,
                "soil_ph": ph_input,
                "soil_moisture": moist_input,
                "temperature": temp_input,
                "rainfall": rainfall_input,
                "land_use": land_use_input,
                "monoculture_or_polyculture": mono_poly,
                "species_richness": richness_input,
                "pollinator_presence": pollinator_input,
                "region": region_input
            })
            st.success("Environmental profile updated.")
            st.rerun()

    with tab_json:
        st.caption("Submit structured environmental JSON payload:")
        default_json_str = json.dumps(st.session_state.current_env_state, indent=2)
        user_json = st.text_area("JSON Input", value=default_json_str, height=220)
        if st.button("Validate & Apply JSON", use_container_width=True):
            try:
                parsed = json.loads(user_json)
                validated = EnvironmentalState(**parsed)
                st.session_state.current_env_state = validated.model_dump(exclude_none=True)
                st.success("Valid Environmental State JSON applied!")
                st.rerun()
            except Exception as err:
                st.error(f"JSON Validation Error: {err}")

    st.divider()
    st.subheader("📚 Knowledge Base Status")
    all_sources = db_service.get_all_sources()
    st.write(f"**Authoritative Sources Indexed:** {len(all_sources)}")
    with st.expander("Inspect Source Registry"):
        for s in all_sources[:6]:
            st.caption(f"**[{s['document_id']}]** {s['organization']} ({s['publication_year']})\n*{s['title']}*")

# Main Content Tabs
tab_consult, tab_relationships, tab_recommendations, tab_evidence, tab_history = st.tabs([
    "💬 Ask Environmental Scientist",
    "🕸️ Causal Relationships Graph",
    "📋 10-Point Recommendations",
    "📑 Evidence & Citations",
    "🕒 Conversation History"
])

# Process query function
def process_reasoning_pipeline(user_query: str):
    env_state = EnvironmentalState(**st.session_state.current_env_state)
    
    # 1. Missing variable detection
    missing_vars = missing_variable_detector.detect_missing(env_state)

    # 2. Multi-metric reasoning
    trace, active_vars = reasoning_engine.execute_reasoning(env_state)

    # 3. Retrieve RAG evidence
    evidence = retrieve_evidence(
        query=user_query,
        environmental_variables=active_vars,
        geographic_context={"region": env_state.region},
        top_k=settings.MAX_RETRIEVAL_RESULTS
    )

    # 4. Generate recommendations
    recs = recommendation_generator.generate_recommendations(
        state=env_state,
        reasoning_trace=trace,
        retrieved_evidence=evidence
    )

    # 5. Confidence
    conf = confidence_service.evaluate_confidence(
        environmental_state=env_state,
        evidence_list=[e.model_dump() for e in evidence],
        variables_used=active_vars
    )

    debug_trace = {
        "user_query": user_query,
        "extracted_environmental_variables": env_state.get_known_variables(),
        "missing_variables": [q.variable_name for q in missing_vars],
        "retrieved_documents": [e.document_id for e in evidence],
        "similarity_scores": [e.similarity_score for e in evidence],
        "reasoning_factors": trace.causal_chains,
        "recommendation_candidates": [r.title for r in recs],
        "citations_count": sum(len(r.scientific_evidence) for r in recs)
    }

    st.session_state.latest_response = {
        "query": user_query,
        "state": env_state,
        "trace": trace,
        "active_vars": active_vars,
        "missing_vars": missing_vars,
        "evidence": evidence,
        "recommendations": recs,
        "confidence": conf
    }
    st.session_state.latest_debug = debug_trace

    # Save to chat history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_query
    })
    st.session_state.chat_history.append({
        "role": "assistant",
        "response": st.session_state.latest_response
    })

# If demo was triggered, run automatically
if st.session_state.active_demo_flow and not st.session_state.latest_response:
    process_reasoning_pipeline("Biodiversity is severely declining under semi-arid monoculture wheat with 0.3% soil organic carbon. What interventions should be taken?")
    st.session_state.active_demo_flow = False

# TAB 1: Consult AI Environmental Scientist
with tab_consult:
    st.markdown("### 2. Conversational Environmental Intelligence")
    st.caption("Ask complex questions regarding soil, water, biodiversity bottlenecks, and agroecological transitions.")

    user_query = st.chat_input("Ask the AI Environmental Scientist (e.g., 'What interventions can reverse soil and biodiversity loss on my semi-arid wheat land?')")
    if user_query:
        process_reasoning_pipeline(user_query)
        st.rerun()

    if st.session_state.latest_response:
        res = st.session_state.latest_response
        trace = res["trace"]
        conf = res["confidence"]
        
        # Display Environmental Assessment & Multi-Metric Reasoning
        st.markdown("#### 🔬 Environmental Assessment")
        st.markdown(f"""
        <div class="metric-card">
            <b>Systemic Assessment:</b> Evaluated <b>{len(res['active_vars'])} interconnected environmental variables</b> ({', '.join(res['active_vars'][:4])}).<br>
            <b>Soil Organic Carbon:</b> <code>{res['state'].soil_organic_carbon}%</code> &nbsp;|&nbsp; 
            <b>Precipitation:</b> <code>{res['state'].rainfall}</code> &nbsp;|&nbsp; 
            <b>Land-Use:</b> <code>{res['state'].land_use}</code> &nbsp;|&nbsp; 
            <b>System Confidence:</b> <span class="badge badge-emerald">{conf['rating']} ({conf['score']:.2f})</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### ⚠️ Key Environmental Bottlenecks Detected")
        for b in trace.primary_bottlenecks:
            st.markdown(f"- 🔴 **{b}**")

        st.markdown("#### 🔗 Multi-Metric Causal Reasoning (≥3 Variables)")
        st.markdown(f"> *{trace.ecological_narrative}*")

        st.markdown("##### Causal Pathways Explored:")
        for c in trace.causal_chains[:3]:
            st.markdown(f"- `{c}`")

        # Missing information
        if res["missing_vars"]:
            st.markdown("#### ❓ Clarifying Questions for Incomplete Parameters")
            st.warning("To refine precise biophysical impact estimates and species selection, please provide:")
            for q in res["missing_vars"]:
                st.markdown(f"- **{q.variable_name.replace('_', ' ').title()}**: {q.question_text}")

        st.divider()
        # Visual Charts
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.altair_chart(render_soil_health_chart(st.session_state.current_env_state), use_container_width=True)
        with col_c2:
            st.altair_chart(render_biodiversity_indicators(st.session_state.current_env_state), use_container_width=True)

    else:
        st.info("👋 Enter an environmental query or click **Run Hackathon Demo Scenario** above to begin analysis.")

# TAB 2: Causal Relationships Graph
with tab_relationships:
    st.markdown("### 5. Configurable Environmental Relationship Graph")
    st.caption("Visual representation of biophysical interactions across Soil Organic Carbon, Hydrology, Land-Use Intensity, and Biodiversity.")
    dot_graph = render_relationship_graph()
    st.graphviz_chart(dot_graph)

# TAB 3: Recommendations
with tab_recommendations:
    st.markdown("### 6. Actionable Scientific Recommendations (10-Point Schema)")
    st.caption("Each recommendation is context-sensitive, non-obvious, and backed by retrieved scientific citations.")

    if st.session_state.latest_response:
        recs = st.session_state.latest_response["recommendations"]
        for i, r in enumerate(recs, 1):
            with st.container():
                st.markdown(f"""
                <div class="recommendation-card">
                    <div style="font-size: 1.25rem; font-weight: 700; color: #38BDF8; margin-bottom: 8px;">
                        Recommendation {i}: {r.title}
                    </div>
                    <p><b>A. What to do:</b> {r.what_to_do}</p>
                    <p><b>B. Why it works:</b> {r.why_it_works}</p>
                    <p><b>C. Environmental variables involved:</b> <code>{', '.join(r.variables_involved)}</code></p>
                    <p><b>D. Impacted metrics:</b></p>
                    <ul>
                        {''.join([f'<li>{m}</li>' for m in r.impacted_metrics])}
                    </ul>
                    <p><b>E. Time horizon:</b> {r.time_horizon}</p>
                    <p><b>F. Expected direction of change:</b> <code>{r.expected_direction}</code></p>
                    <p><b>G. Confidence:</b> <b>{r.confidence}</b> — <i>{r.confidence_reason}</i></p>
                    <p><b>I. Important assumptions:</b></p>
                    <ul>
                        {''.join([f'<li>{a}</li>' for a in r.important_assumptions])}
                    </ul>
                    <p><b>J. Possible trade-offs & risks:</b></p>
                    <ul>
                        {''.join([f'<li>{t}</li>' for t in r.possible_trade_offs])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)

                if r.scientific_evidence:
                    st.markdown("**H. Supporting Scientific Evidence:**")
                    for cit in r.scientific_evidence:
                        st.markdown(f"""
                        <div class="citation-box">
                            <b>Source:</b> {cit.source_organization} ({cit.year}) | <b>Title:</b> {cit.title}<br>
                            <b>Excerpt:</b> "{cit.relevant_evidence}"<br>
                            <b>URL:</b> <a href="{cit.url}" target="_blank">{cit.url}</a>
                        </div>
                        """, unsafe_allow_html=True)
                st.write("")
    else:
        st.info("Execute an inquiry or demo scenario to view generated scientific recommendations.")

# TAB 4: Evidence & Citations
with tab_evidence:
    st.markdown("### 4. Retrieved Scientific Evidence (RAG Pipeline)")
    st.caption("Actual empirical excerpts retrieved from ChromaDB vector database, ranked by semantic similarity and variable overlap.")
    
    if st.session_state.latest_response:
        evidence = st.session_state.latest_response["evidence"]
        for ev in evidence:
            with st.expander(f"[{ev.document_id}] {ev.organization} ({ev.publication_year}) — Similarity: {ev.similarity_score:.3f}"):
                st.markdown(f"**Title:** *{ev.title}*")
                st.markdown(f"**Domain:** `{ev.environmental_domain}` | **Scope:** `{ev.geographic_scope}`")
                st.markdown(f"**Variables Addressed:** `{', '.join(ev.variables)}`")
                st.markdown(f"**Empirical Excerpt:**\n> {ev.excerpt}")
                st.markdown(f"**Official Citation:** {ev.citation}")
                st.markdown(f"**Authoritative URL:** [{ev.url}]({ev.url})")
                st.caption(f"Source Reliability Score: {ev.reliability_score}")
    else:
        st.info("No active retrieval trace. Run an analysis to inspect retrieved documents.")

# TAB 5: Conversation History
with tab_history:
    st.markdown("### 10. Multi-Turn Conversation Context")
    st.caption(f"Session ID: `{st.session_state.conversation_id}`")
    
    if st.session_state.chat_history:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.write(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(f"Analyzed query: *{msg['response']['query']}*")
                    st.caption(f"Generated {len(msg['response']['recommendations'])} scientific recommendations.")
    else:
        st.caption("No previous messages in this session.")

# Render Observability / Audit Panel at bottom
render_debug_observability_panel(st.session_state.latest_debug)
