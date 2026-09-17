from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class KnowledgeDocument(BaseModel):
    """
    Authoritative scientific document knowledge schema.
    Conforms to hackathon requirements: no fabricated citations or fake metrics.
    """
    document_id: str = Field(..., description="Unique persistent identifier, e.g. DOC-FAO-2021-01")
    title: str = Field(..., description="Full formal publication title")
    organization: str = Field(..., description="Publishing body: FAO, IPCC, UNEP, IPBES, CGIAR, etc.")
    publication_year: int = Field(..., description="Year of publication")
    source_type: str = Field(..., description="e.g. Assessment Report, Meta-Analysis, Peer-Reviewed Article")
    environmental_domain: str = Field(..., description="Primary domain: Soil Health, Agroforestry, Biodiversity, etc.")
    variables: List[str] = Field(default_factory=list, description="List of related environmental variables")
    geographic_scope: str = Field(..., description="Geographic applicability (e.g. Global, Semi-arid croplands)")
    text: str = Field(..., description="Authoritative scientific excerpt and empirical findings")
    citation: str = Field(..., description="Full academic citation")
    url: str = Field(..., description="Authoritative source or DOI URL")
    reliability_score: float = Field(default=0.95, ge=0.0, le=1.0, description="Source authority index")

class RetrievedEvidence(BaseModel):
    """
    Result of a RAG vector retrieval call with similarity ranking and metadata.
    """
    document_id: str
    title: str
    organization: str
    publication_year: int
    environmental_domain: str
    variables: List[str]
    excerpt: str
    similarity_score: float = Field(..., description="Cosine similarity score (0-1)")
    citation: str
    url: str
    reliability_score: float

class CitationItem(BaseModel):
    """
    Structured citation reference for an AI recommendation.
    """
    source_organization: str
    title: str
    year: int
    citation: str
    url: str
    relevant_evidence: str
