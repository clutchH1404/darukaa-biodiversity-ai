import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["vector_store_documents"] > 0

def test_get_sources():
    response = client.get("/sources")
    assert response.status_code == 200
    sources = response.json()
    assert len(sources) > 0
    assert "document_id" in sources[0]

def test_post_retrieve():
    payload = {
        "query": "soil organic carbon",
        "environmental_variables": ["soil_organic_carbon"],
        "top_k": 2
    }
    response = client.post("/retrieve", json=payload)
    assert response.status_code == 200
    evidence = response.json()
    assert len(evidence) <= 2
    assert len(evidence) > 0
    assert "similarity_score" in evidence[0]

def test_post_environment_observation():
    obs_payload = {
        "location_name": "API Test Field",
        "region": "semi-arid",
        "soil_organic_carbon": 0.45,
        "soil_ph": 7.1,
        "rainfall": "low",
        "land_use": "monoculture barley"
    }
    response = client.post("/environment", json=obs_payload)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["soil_organic_carbon"] == 0.45
    assert res_data["id"] is not None

def test_post_analyze():
    analyze_payload = {
        "environmental_state": {
            "soil_organic_carbon": 0.3,
            "rainfall": "low",
            "land_use": "monoculture wheat"
        }
    }
    response = client.post("/analyze", json=analyze_payload)
    assert response.status_code == 200
    data = response.json()
    assert "bottlenecks" in data
    assert len(data["bottlenecks"]) > 0

def test_post_recommend():
    state_payload = {
        "soil_organic_carbon": 0.3,
        "rainfall": "low",
        "land_use": "monoculture wheat"
    }
    response = client.post("/recommend", json=state_payload)
    assert response.status_code == 200
    recs = response.json()
    assert len(recs) > 0
    assert "what_to_do" in recs[0]
    assert len(recs[0]["variables_involved"]) >= 3

def test_post_chat_and_conversation_lookup():
    chat_payload = {
        "message": "Biodiversity is severely declining on my semi-arid monoculture wheat field with 0.3% SOC.",
        "environmental_state": {
            "region": "semi-arid",
            "soil_organic_carbon": 0.3,
            "rainfall": "low"
        }
    }
    response = client.post("/chat", json=chat_payload)
    assert response.status_code == 200
    chat_data = response.json()
    assert "formatted_response" in chat_data
    assert "recommendations" in chat_data
    assert len(chat_data["recommendations"]) > 0
    cid = chat_data["conversation_id"]

    # Verify conversation history lookup
    lookup = client.get(f"/conversation/{cid}")
    assert lookup.status_code == 200
    convo_data = lookup.json()
    assert convo_data["conversation_id"] == cid
    assert len(convo_data["messages_history"]) >= 2

def test_post_understand():
    payload = {"query": "My farm in Maharashtra has low soil organic carbon 0.4 percent SOC and declining pollinators."}
    response = client.post("/understand", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "soil_organic_matter" in data["detected_variables"] or "soil_organic_carbon" in data["detected_variables"]
    assert "missing_variables" in data
    assert len(data["missing_context_questions"]) > 0
    assert data["location"]["name"] == "Maharashtra, India"

def test_get_and_post_graph():
    # Test GET
    get_res = client.get("/graph")
    assert get_res.status_code == 200
    g_data = get_res.json()
    assert "nodes" in g_data
    assert "edges" in g_data
    assert len(g_data["nodes"]) >= 20
    assert len(g_data["edges"]) >= 20

    # Test POST with state
    post_res = client.post("/graph", json={"environmental_state": {"soil_organic_carbon": 0.4, "rainfall": "low"}})
    assert post_res.status_code == 200
    p_data = post_res.json()
    soc_node = next((n for n in p_data["nodes"] if n["id"] == "soil_organic_carbon"), None)
    assert soc_node is not None
    assert soc_node["current_state"] == "0.4"
    assert soc_node["trend"] == "depleted / stressed"

def test_post_simulate_supported_and_unsupported():
    # Supported
    sup_payload = {
        "intervention_type": "soil_organic_restoration",
        "intensity": 0.75,
        "time_horizon_years": 5,
        "baseline_state": {"soil_organic_carbon": 0.5}
    }
    sup_res = client.post("/simulate", json=sup_payload)
    assert sup_res.status_code == 200
    sup_data = sup_res.json()
    assert sup_data["status"] == "modeled"
    assert len(sup_data["projected_deltas"]) >= 3
    assert len(sup_data["scientific_basis"]) >= 1

    # Unsupported
    unsup_payload = {
        "intervention_type": "hypothetical_nano_clouds",
        "intensity": 0.5,
        "time_horizon_years": 5
    }
    unsup_res = client.post("/simulate", json=unsup_payload)
    assert unsup_res.status_code == 200
    unsup_data = unsup_res.json()
    assert unsup_data["status"] == "unavailable"
    assert "unavailable" in unsup_data["ecological_summary"].lower()

def test_get_session_structured_context():
    # First create a turn
    chat_payload = {
        "message": "My agricultural farm is located in Maharashtra with 0.3% SOC.",
        "environmental_state": {"soil_organic_carbon": 0.3, "region": "semi-arid"}
    }
    chat_res = client.post("/chat", json=chat_payload)
    cid = chat_res.json()["conversation_id"]

    # Get structured context
    ctx_res = client.get(f"/session/{cid}/context")
    assert ctx_res.status_code == 200
    ctx = ctx_res.json()
    assert "soil" in ctx
    assert ctx["soil"]["soil_organic_carbon"] == 0.3
    assert "conversation_history" in ctx
