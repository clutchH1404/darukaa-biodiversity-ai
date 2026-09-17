import pytest
from pydantic import ValidationError
from app.models.environmental_state import EnvironmentalState, EnvironmentalObservationCreate

def test_valid_json_payload():
    data = {
        "region": "semi-arid",
        "soil_organic_carbon": 0.3,
        "soil_ph": 6.8,
        "soil_moisture": 18.0,
        "rainfall": "low",
        "land_use": "monoculture wheat",
        "temperature": 31.0,
        "species_richness": "low",
        "pollution_level": "moderate"
    }
    state = EnvironmentalState(**data)
    assert state.soil_organic_carbon == 0.3
    assert state.soil_ph == 6.8
    assert state.soil_moisture == 18.0
    assert state.land_use == "monoculture wheat"
    assert state.count_known_variables() == 9

def test_percentage_string_normalization():
    data = {
        "soil_organic_carbon": "0.3%",
        "soil_moisture": "18.5%",
        "soil_ph": "6.8"
    }
    state = EnvironmentalState(**data)
    assert state.soil_organic_carbon == 0.3
    assert state.soil_moisture == 18.5
    assert state.soil_ph == 6.8

def test_out_of_bounds_validation():
    # Invalid pH > 14
    with pytest.raises(ValidationError):
        EnvironmentalState(soil_ph=15.5)

    # Invalid latitude > 90
    with pytest.raises(ValidationError):
        EnvironmentalState(latitude=95.0)

def test_empty_and_partial_json():
    state = EnvironmentalState()
    assert state.count_known_variables() == 0
    assert state.soil_organic_carbon is None
