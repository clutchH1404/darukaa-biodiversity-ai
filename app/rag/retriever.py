from typing import List, Dict, Any, Optional
from .vector_store import vector_store, ChromaVectorStore
from ..models.knowledge_schema import RetrievedEvidence

class EvidenceRetriever:
    """
    Intelligent evidence retrieval and hybrid ranking engine.
    Integrates semantic vector search, environmental variable matching,
    geographic scoping, and authoritative source reliability weighting.
    """

    def __init__(self, store: Optional[ChromaVectorStore] = None):
        self.store = store or vector_store

    def retrieve_evidence(
        self,
        query: str,
        environmental_variables: Optional[List[str]] = None,
        geographic_context: Optional[Dict[str, Any]] = None,
        top_k: int = 5
    ) -> List[RetrievedEvidence]:
        """
        Retrieves and ranks evidence documents traceable to authoritative sources.
        """
        env_vars = [v.lower() for v in (environmental_variables or [])]
        region_query = ""
        if geographic_context:
            region = geographic_context.get("region") or geographic_context.get("climate_zone") or ""
            if region:
                region_query = f" in {region} ecosystem"

        augmented_query = f"{query}{region_query}"
        if env_vars:
            augmented_query += f" focusing on {', '.join(env_vars)}"

        # 1. Vector Search
        raw_results = self.store.search(
            query=augmented_query,
            n_results=top_k * 2
        )

        if not raw_results:
            return []

        # 2. Hybrid Evidence Re-ranking
        ranked = []
        for r in raw_results:
            sim_score = r.get("similarity_score", 0.5)
            rel_score = r.get("reliability_score", 0.95)
            doc_vars = [v.lower() for v in r.get("variables", [])]

            # Variable overlap bonus
            overlap_count = sum(1 for ev in env_vars if any(ev in dv for dv in doc_vars))
            overlap_boost = min(0.20, overlap_count * 0.08)

            # Geographic scope boost
            geo_boost = 0.0
            if geographic_context:
                region_str = str(geographic_context.get("region", "")).lower()
                doc_geo = str(r.get("geographic_scope", "")).lower()
                if region_str and (region_str in doc_geo or "global" in doc_geo):
                    geo_boost = 0.05

            final_score = (sim_score * 0.60) + (rel_score * 0.20) + overlap_boost + geo_boost
            ranked.append((final_score, r))

        # Sort descending by composite score
        ranked.sort(key=lambda x: x[0], reverse=True)

        # De-duplicate by document_id so we don't return 4 chunks of the same paper
        seen_docs = set()
        evidence_items: List[RetrievedEvidence] = []

        for final_score, item in ranked:
            doc_id = item["document_id"]
            if doc_id in seen_docs and len(evidence_items) < top_k:
                continue
            seen_docs.add(doc_id)

            evidence_items.append(
                RetrievedEvidence(
                    document_id=item["document_id"],
                    title=item["title"],
                    organization=item["organization"],
                    publication_year=int(item["publication_year"]),
                    environmental_domain=item["environmental_domain"],
                    variables=item.get("variables", []),
                    excerpt=item["excerpt"],
                    similarity_score=round(item["similarity_score"], 4),
                    citation=item["citation"],
                    url=item["url"],
                    reliability_score=round(item["reliability_score"], 2)
                )
            )

            if len(evidence_items) >= top_k:
                break

        return evidence_items

evidence_retriever = EvidenceRetriever()

def retrieve_evidence(
    query: str,
    environmental_variables: Optional[List[str]] = None,
    geographic_context: Optional[Dict[str, Any]] = None,
    top_k: int = 5
) -> List[RetrievedEvidence]:
    """Convenience top-level retrieval function conforming to hackathon specification."""
    return evidence_retriever.retrieve_evidence(
        query=query,
        environmental_variables=environmental_variables,
        geographic_context=geographic_context,
        top_k=top_k
    )
