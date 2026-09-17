import pytest
from app.models.environmental_state import EnvironmentalState
from app.reasoning.relationship_graph import relationship_graph
from app.reasoning.bottleneck_detector import bottleneck_detector
from app.reasoning.engine import reasoning_engine

def test_enforces_three_or_more_variables():
    state = EnvironmentalState(
        soil_organic_carbon=0.3,
        rainfall="low",
        land_use="monoculture wheat"
    )
    trace, active_vars = reasoning_engine.execute_reasoning(state)
    assert len(active_vars) >= 3
    assert len(trace.interacting_variables) >= 3

def test_relationship_graph_pathway():
    # Verify pathway from soil_organic_carbon to biodiversity
    paths = relationship_graph.trace_pathways("soil_organic_carbon", "biodiversity")
    assert len(paths) > 0
    shortest = min(paths, key=len)
    chain_str = relationship_graph.explain_chain(shortest)
    assert "soil structure" in chain_str
    assert "water retention" in chain_str

def test_bottleneck_detection_compound_stress():
    state = EnvironmentalState(
        soil_organic_carbon=0.3,
        rainfall="low",
        land_use="monoculture wheat",
        species_richness="low"
    )
    bottlenecks = bottleneck_detector.analyze_bottlenecks(state)
    names = [b["name"] for b in bottlenecks]
    assert any("Soil Structural Degradation" in n for n in names)
    assert any("Spatial Homogenization" in n for n in names)
