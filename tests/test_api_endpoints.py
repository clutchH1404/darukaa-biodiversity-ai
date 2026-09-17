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
