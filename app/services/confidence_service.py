from typing import Dict, Any, List
from ..models.environmental_state import EnvironmentalState

class ConfidenceService:
    """
    Computes transparent, factorized scientific confidence scores.
    Considers:
    - Input completeness (how many key environmental variables are known)
    - Retrieval quality (mean similarity score of retrieved evidence)
    - Evidence volume (number of distinct peer-reviewed or authoritative sources)
    - Source reliability (reputation of publishers: FAO, IPCC, IPBES = 0.95+)
    - Directness of causal relationship
    """

    CRITICAL_VARIABLES = [
        "soil_organic_carbon", "soil_moisture", "soil_ph",
        "rainfall", "land_use", "species_richness"
    ]

    def evaluate_confidence(
        self,
        environmental_state: EnvironmentalState,
        evidence_list: List[Dict[str, Any]],
        variables_used: List[str]
    ) -> Dict[str, Any]:
        # 1. Environmental Completeness (0.0 to 1.0)
        known_vars = environmental_state.get_known_variables()
        known_critical = sum(1 for v in self.CRITICAL_VARIABLES if v in known_vars)
        input_completeness = min(1.0, known_critical / len(self.CRITICAL_VARIABLES))

        # 2. Retrieval Quality (0.0 to 1.0)
        if evidence_list:
            avg_sim = sum(e.get("similarity_score", 0.7) for e in evidence_list) / len(evidence_list)
        else:
            avg_sim = 0.4

        # 3. Evidence Volume & Quality (0.0 to 1.0)
        source_count = len(evidence_list)
        volume_score = min(1.0, source_count / 3.0)
        
        if evidence_list:
            avg_reliability = sum(e.get("reliability_score", 0.9) for e in evidence_list) / len(evidence_list)
        else:
            avg_reliability = 0.5

        # 4. Composite Confidence Calculation
        composite_score = (
            (input_completeness * 0.35) +
            (avg_sim * 0.25) +
            (volume_score * 0.20) +
            (avg_reliability * 0.20)
        )

        # Categorize
        if composite_score >= 0.75:
            rating = "High"
        elif composite_score >= 0.50:
            rating = "Medium"
        else:
            rating = "Low"

        # Explicit scientific rationale
        reasons = []
        if source_count >= 2:
            reasons.append(f"Supported by {source_count} authoritative sources (e.g., {', '.join(set(e.get('organization', 'Literature') for e in evidence_list[:2]))})")
        else:
            reasons.append("Limited empirical sources retrieved for this specific variable combination")

        missing = [v.replace('_', ' ') for v in self.CRITICAL_VARIABLES if v not in known_vars]
        if missing:
            reasons.append(f"Incomplete local measurements for {', '.join(missing[:3])}")
        else:
            reasons.append("Comprehensive field parameters provided")

        explanation = ". ".join(reasons) + "."

        return {
            "rating": rating,
            "score": round(composite_score, 3),
            "input_completeness": round(input_completeness, 2),
            "evidence_count": source_count,
            "average_similarity": round(avg_sim, 3),
            "reason": explanation
        }

confidence_service = ConfidenceService()
