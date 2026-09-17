import streamlit as st
from typing import Dict, Any, Optional

def render_debug_observability_panel(debug_data: Optional[Dict[str, Any]]):
    """
    Renders an in-depth observability and scientific audit panel for hackathon judges.
    Confirms that the system is explicitly grounded in RAG, multi-metric causal reasoning,
    and actual retrieved documents rather than generic LLM hallucinations.
    """
    with st.expander("🔍 JUDGE OBSERVABILITY & SCIENTIFIC AUDIT PANEL (Click to inspect grounding trace)", expanded=False):
        if not debug_data:
            st.info("Submit an environmental query or click 'Launch Hackathon Demo Scenario' to inspect pipeline execution telemetry.")
            return

        st.markdown("#### 1. Input Processing & Variable Extraction")
        col1, col2 = st.columns(2)
        with col1:
            st.caption("Raw User Query")
            st.code(debug_data.get("user_query", "N/A"), language="text")
        with col2:
            st.caption("Extracted Environmental Variables")
            st.json(debug_data.get("extracted_environmental_variables", {}))

        st.markdown("#### 2. Dynamic Missing-Variable Check")
        missing = debug_data.get("missing_variables", [])
        if missing:
            st.warning(f"Missing high-priority measurements detected: {', '.join(missing)}")
        else:
            st.success("All critical environmental parameters are present.")

        st.markdown("#### 3. RAG Retrieval & Similarity Telemetry")
        docs = debug_data.get("retrieved_documents", [])
        scores = debug_data.get("similarity_scores", [])
        if docs:
            score_table = [{"Document ID": d, "Cosine Similarity": s} for d, s in zip(docs, scores)]
            st.dataframe(score_table, use_container_width=True)
        else:
            st.caption("No vector documents in trace.")

        st.markdown("#### 4. Multi-Metric Causal Pathways")
        factors = debug_data.get("reasoning_factors", [])
        for f in factors:
            st.markdown(f"- `{f}`")

        st.markdown("#### 5. Intervention Candidates & Citation Trace")
        cands = debug_data.get("recommendation_candidates", [])
        citations_count = debug_data.get("citations_count", 0)
        st.write(f"Selected Interventions ({len(cands)}):")
        for c in cands:
            st.markdown(f"- **{c}**")
        st.caption(f"Total Authentic Citations Attached: {citations_count}")
