import pytest
from app.models.environmental_state import EnvironmentalState
from app.memory.missing_variable_detector import missing_variable_detector

def test_vague_query_detection():
    # Empty environmental state simulates generic query: "Biodiversity is declining on my land"
    state = EnvironmentalState()
    missing = missing_variable_detector.detect_missing(state)
    
    missing_names = [q.variable_name for q in missing]
    assert "soil_organic_carbon" in missing_names
    assert "rainfall" in missing_names
    assert "land_use" in missing_names
    assert len(missing) > 0

def test_no_redundant_questions_when_data_present():
    state = EnvironmentalState(
        soil_organic_carbon=0.3,
        rainfall="low",
        land_use="monoculture wheat",
        soil_ph=6.8,
        region="semi-arid"
    )
    missing = missing_variable_detector.detect_missing(state)
    missing_names = [q.variable_name for q in missing]
    
    assert "soil_organic_carbon" not in missing_names
    assert "rainfall" not in missing_names
    assert "land_use" not in missing_names
    assert "soil_ph" not in missing_names
    assert "region" not in missing_names

def test_natural_language_extraction():
    text = "We have 0.3% SOC and low rainfall in a semi-arid monoculture wheat field with soil pH 6.8."
    extracted = missing_variable_detector.extract_variables_from_text(text)
    
    assert extracted.get("soil_organic_carbon") == 0.3
    assert extracted.get("rainfall") == "low"
    assert extracted.get("region") == "semi-arid"
    assert extracted.get("land_use") == "monoculture wheat"
    assert extracted.get("soil_ph") == 6.8
