import pytest
from app.rag.retriever import retrieve_evidence
from app.rag.vector_store import vector_store

def test_vector_store_populated():
    assert vector_store.count() >= 10

def test_retrieve_evidence_structure():
    evidence = retrieve_evidence(
        query="soil organic carbon and water retention in drylands",
        environmental_variables=["soil_organic_carbon", "rainfall"],
        top_k=3
    )
    assert len(evidence) <= 3
    assert len(evidence) > 0
    top_doc = evidence[0]
    assert top_doc.document_id.startswith("DOC-")
    assert top_doc.title is not None
    assert top_doc.similarity_score > 0.0
    assert "http" in top_doc.url
    assert top_doc.citation is not None
    assert len(top_doc.excerpt) > 20

def test_retrieval_relevance_matching():
    # Pollinator specific query should rank pollinator assessment at top
    evidence = retrieve_evidence(
        query="wild pollinators and pesticide reduction",
        environmental_variables=["pollinator_presence", "pesticide_intensity"],
        top_k=2
    )
    assert len(evidence) > 0
    doc_ids = [e.document_id for e in evidence]
    assert any("POLLINATOR" in d or "GARIBALDI" in d or "IPBES" in d for d in doc_ids)
