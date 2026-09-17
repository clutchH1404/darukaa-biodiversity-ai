import pytest
import uuid
from app.memory.session_memory import session_memory
from app.memory.missing_variable_detector import missing_variable_detector

def test_multi_turn_state_accumulation():
    cid = f"test-turn-{uuid.uuid4()}"

    # Turn 1: User provides region and crop
    turn1_text = "I farm monoculture wheat in a semi-arid region."
    extracted1 = missing_variable_detector.extract_variables_from_text(turn1_text)
    state1 = session_memory.update_session_state(cid, extracted1)
    
    assert state1.land_use == "monoculture wheat"
    assert state1.region == "semi-arid"
    assert state1.soil_organic_carbon is None

    # Turn 2: User responds with SOC and pH measurements
    turn2_text = "Our measured soil organic carbon is 0.3% and pH is 6.8."
    extracted2 = missing_variable_detector.extract_variables_from_text(turn2_text)
    state2 = session_memory.update_session_state(cid, extracted2)

    # State2 must preserve Turn 1 + Turn 2
    assert state2.land_use == "monoculture wheat"
    assert state2.region == "semi-arid"
    assert state2.soil_organic_carbon == 0.3
    assert state2.soil_ph == 6.8

def test_conversation_history_persistence():
    cid = f"test-hist-{uuid.uuid4()}"
    session_memory.record_turn(cid, "User: High pesticide", "Assistant: Recommended flowering buffers")
    session = session_memory.get_or_create_session(cid)
    assert len(session["messages"]) == 2
    assert session["messages"][0]["content"] == "User: High pesticide"
