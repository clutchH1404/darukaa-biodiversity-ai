import pytest
from app.services.db_service import db_service
from app.models.environmental_state import EnvironmentalState
from app.reasoning.engine import reasoning_engine
from app.rag.retriever import retrieve_evidence
from app.recommendations.generator import recommendation_generator

def test_citations_exist_in_source_registry():
    registered_sources = {s["document_id"]: s for s in db_service.get_all_sources()}
    assert len(registered_sources) > 0

    state = EnvironmentalState(
        soil_organic_carbon=0.3,
        rainfall="low",
        land_use="monoculture wheat"
    )
    trace, active_vars = reasoning_engine.execute_reasoning(state)
    evidence = retrieve_evidence("semi-arid soil restoration", active_vars, top_k=3)
    recs = recommendation_generator.generate_recommendations(state, trace, evidence)

    for r in recs:
        assert len(r.scientific_evidence) > 0
        for cit in r.scientific_evidence:
            assert cit.source_organization is not None
            assert cit.url.startswith("http")
            assert cit.year >= 2010

def test_source_registry_integrity():
    sources = db_service.get_all_sources()
    for s in sources:
        assert s["organization"] in [
            "Food and Agriculture Organization of the United Nations (FAO)",
            "Intergovernmental Panel on Climate Change (IPCC)",
            "Intergovernmental Science-Policy Platform on Biodiversity and Ecosystem Services (IPBES)",
            "IPBES",
            "Science Advances (American Association for the Advancement of Science)",
            "Science (AAAS)",
            "United Nations Environment Programme (UNEP)",
            "FAO & World Agroforestry (ICRAF)",
            "United States Environmental Protection Agency (US EPA)",
            "CGIAR / ICARDA",
            "Nature / Soil & Tillage Research"
        ]
