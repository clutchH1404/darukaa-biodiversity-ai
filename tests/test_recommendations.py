import pytest
from app.models.environmental_state import EnvironmentalState
from app.reasoning.engine import reasoning_engine
from app.rag.retriever import retrieve_evidence
from app.recommendations.generator import recommendation_generator

def test_recommendation_ten_point_schema():
    state = EnvironmentalState(
        soil_organic_carbon=0.3,
        rainfall="low",
        land_use="monoculture wheat",
        region="semi-arid"
    )
    trace, active_vars = reasoning_engine.execute_reasoning(state)
    evidence = retrieve_evidence("semi-arid wheat agroecology", active_vars, top_k=3)
    recs = recommendation_generator.generate_recommendations(state, trace, evidence)

    assert len(recs) >= 1
    for r in recs:
        # A. What to do
        assert len(r.what_to_do) > 20
        # B. Why it works
        assert len(r.why_it_works) > 20
        # C. Variables involved (>=3)
        assert len(r.variables_involved) >= 3
        # D. Impacted metrics
        assert len(r.impacted_metrics) >= 2
        # E. Time horizon
        assert any(h in r.time_horizon for h in ["Short", "Medium", "Long"])
        # F. Expected direction
        assert len(r.expected_direction) > 0
        # G. Confidence
        assert r.confidence in ["High", "Medium", "Low"]
        assert len(r.confidence_reason) > 5
        # H. Scientific evidence
        assert len(r.scientific_evidence) > 0
        # I. Assumptions
        assert len(r.important_assumptions) > 0
        # J. Trade-offs
        assert len(r.possible_trade_offs) > 0
