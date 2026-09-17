# Darukaa.Earth REST API Reference

The FastAPI backend exposes 9 REST endpoints with automatic OpenAPI documentation available at `/docs` or `/redoc`.

Base URL: `http://localhost:8000`

---

## Endpoint Summary

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Diagnostic status, vector store counts, DB connectivity |
| `GET` | `/sources` | Catalog of authoritative scientific literature in registry |
| `POST` | `/chat` | Main conversational endpoint with multi-turn memory & RAG |
| `POST` | `/analyze` | Multi-metric bottleneck assessment & causal path discovery |
| `POST` | `/recommend` | Direct generation of 10-point scientific recommendations |
| `POST` | `/retrieve` | Semantic vector retrieval with variable-aware hybrid ranking |
| `POST` | `/environment` | Validates & saves structured environmental observation JSON |
| `POST` | `/ingest` | Dynamically ingests a new scientific knowledge document |
| `GET` | `/conversation/{id}`| Retrieves full multi-turn conversation and environmental state |

---

## 1. POST /chat
The primary conversational endpoint for interacting with the AI Environmental Scientist.

### Request Body:
```json
{
  "message": "Biodiversity is severely declining on my semi-arid monoculture wheat field with 0.3% SOC.",
  "conversation_id": "optional-uuid-string",
  "environmental_state": {
    "region": "semi-arid",
    "soil_organic_carbon": 0.3,
    "rainfall": "low",
    "land_use": "monoculture wheat"
  },
  "geographic_context": {
    "region": "semi-arid"
  }
}
```

### Response Body:
Returns `ChatResponse` containing:
- `conversation_id`: Active session ID.
- `formatted_response`: Structured Markdown conforming to Hackathon Section 14.
- `environmental_assessment`: Biophysical evaluation narrative.
- `key_drivers`: List of detected limiting bottlenecks.
- `multi_metric_reasoning`: Causal explanation combining $\ge 3$ variables.
- `recommendations`: Array of 10-point recommendations (A through J).
- `trade_offs_and_risks`: Agroecological constraints.
- `evidence_retrieved`: Array of retrieved scientific documents with similarity scores.
- `missing_variables_detected`: Array of clarifying questions for missing data.
- `confidence_summary`: Multi-factor confidence rating and breakdown.
- `debug_trace`: Full pipeline telemetry for hackathon judges.

---

## 2. POST /environment
Submit field measurements in structured JSON format.

### Request Body:
```json
{
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
```

### Response Body:
```json
{
  "id": "e2f09d84-c89b-43a9-83c9-0263f972b226",
  "region": "semi-arid",
  "soil_organic_carbon": 0.3,
  "soil_ph": 6.8,
  "soil_moisture": 18.0,
  "rainfall": "low",
  "land_use": "monoculture wheat",
  "created_at": "2026-09-17 15:52:32"
}
```

---

## 3. POST /retrieve
Inspect semantic retrieval and hybrid ranking directly.

### Request Body:
```json
{
  "query": "soil moisture retention in semi-arid soils",
  "environmental_variables": ["soil_organic_carbon", "soil_moisture", "rainfall"],
  "top_k": 3
}
```

### Response Body:
```json
[
  {
    "document_id": "DOC-FAO-2020-GSOC",
    "title": "Recarbonizing Global Soils: A Technical Manual of Recommended Management Practices (Vol 1-6)",
    "organization": "Food and Agriculture Organization of the United Nations (FAO)",
    "publication_year": 2020,
    "environmental_domain": "Soil Health & Soil Organic Carbon",
    "variables": ["soil_organic_carbon", "soil_moisture", "land_use", "biodiversity"],
    "similarity_score": 0.884,
    "url": "https://www.fao.org/documents/card/en/c/cb6386en"
  }
]
```
