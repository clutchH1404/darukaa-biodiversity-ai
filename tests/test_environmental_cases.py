import pytest
from app.models.environmental_state import EnvironmentalState
from app.reasoning.engine import reasoning_engine
from app.rag.retriever import retrieve_evidence
from app.recommendations.generator import recommendation_generator

def test_case_1_semiarid_monoculture_wheat():
    """
    CASE 1:
    Semi-arid region, Low rainfall, 0.3% SOC, Monoculture wheat, Low biodiversity
    Expected: Detects critical desiccation & structural collapse; recommends cover crops and agroforestry belts.
    """
    case1 = EnvironmentalState(
        region="semi-arid",
        rainfall="low",
        soil_organic_carbon=0.3,
        land_use="monoculture wheat",
        species_richness="low"
    )
    trace, active_vars = reasoning_engine.execute_reasoning(case1)
    evidence = retrieve_evidence("semi-arid wheat soil carbon", active_vars, top_k=3)
    recs = recommendation_generator.generate_recommendations(case1, trace, evidence)

    assert any("Soil Structural Degradation" in b for b in trace.primary_bottlenecks)
    rec_titles = [r.title for r in recs]
    assert any("Cover Cropping" in t or "Agroforestry" in t for t in rec_titles)

def test_case_2_highrain_pesticide_pollinators():
    """
    CASE 2:
    High rainfall, High pesticide intensity, Low pollinator presence
    Expected: Detects ecotoxicological bottleneck; recommends flowering corridors & IPM margins.
    """
    case2 = EnvironmentalState(
        rainfall="high",
        pesticide_intensity="high",
        pollinator_presence="low",
        land_use="fruit orchard"
    )
    trace, active_vars = reasoning_engine.execute_reasoning(case2)
    evidence = retrieve_evidence("pollinators pesticide flowering strips", active_vars, top_k=3)
    recs = recommendation_generator.generate_recommendations(case2, trace, evidence)

    assert any("Ecotoxicological" in b for b in trace.primary_bottlenecks)
    rec_titles = [r.title for r in recs]
    assert any("Flowering Field Margins" in t or "Pollinator Corridors" in t for t in rec_titles)

def test_case_3_urban_fringe_fragmentation():
    """
    CASE 3:
    Urban-fringe land, Habitat fragmentation, Pollution, Low species richness
    Expected: Detects landscape fragmentation & anthropogenic disturbance.
    """
    case3 = EnvironmentalState(
        region="urban-fringe peri-urban",
        habitat_fragmentation="high",
        pollution_level="high",
        species_richness="low"
    )
    trace, active_vars = reasoning_engine.execute_reasoning(case3)
    assert any("Landscape Fragmentation" in b for b in trace.primary_bottlenecks)

def test_case_4_degraded_agricultural_soil():
    """
    CASE 4:
    Degraded agricultural soil, Low organic carbon, Low moisture, High temperature
    Expected: Detects compounding desiccation & severe thermal stress.
    """
    case4 = EnvironmentalState(
        soil_organic_carbon=0.5,
        soil_moisture=12.0,
        temperature=34.0,
        rainfall="low",
        drought_condition="severe"
    )
    trace, active_vars = reasoning_engine.execute_reasoning(case4)
    evidence = retrieve_evidence("dryland degraded soil drought resilience", active_vars, top_k=3)
    recs = recommendation_generator.generate_recommendations(case4, trace, evidence)

    assert len(recs) > 0
    assert any("soil_organic_carbon" in r.variables_involved for r in recs)

def test_case_5_healthy_soil_mixed_cropping():
    """
    CASE 5:
    Healthy soil, High biodiversity, Moderate rainfall, Mixed cropping
    Expected: Recognizes baseline stability and maintains conservation buffers without critical alarms.
    """
    case5 = EnvironmentalState(
        soil_organic_carbon=3.8,
        soil_moisture=38.0,
        species_richness="high",
        pollinator_presence="high",
        rainfall="moderate",
        land_use="mixed polyculture and silvopasture"
    )
    trace, active_vars = reasoning_engine.execute_reasoning(case5)
    evidence = retrieve_evidence("regenerative polyculture conservation", active_vars, top_k=3)
    recs = recommendation_generator.generate_recommendations(case5, trace, evidence)

    assert len(recs) > 0
    assert not any("CRITICAL" in b.upper() for b in trace.primary_bottlenecks)
