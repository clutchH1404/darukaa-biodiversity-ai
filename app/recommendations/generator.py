from typing import List, Dict, Any, Optional
from ..models.environmental_state import EnvironmentalState
from ..models.knowledge_schema import RetrievedEvidence, CitationItem
from ..models.response_models import RecommendationItem, ReasoningTrace
from ..services.confidence_service import confidence_service
from .intervention_library import INTERVENTION_CATALOG, AgroecologicalIntervention

class RecommendationGenerator:
    """
    Generates actionable, non-obvious, scientifically defensible biodiversity
    recommendations adhering strictly to the 10-point schema.
    """

    def generate_recommendations(
        self,
        state: EnvironmentalState,
        reasoning_trace: ReasoningTrace,
        retrieved_evidence: List[RetrievedEvidence]
    ) -> List[RecommendationItem]:
        soc = state.soil_organic_carbon
        rainfall_str = str(state.rainfall or "").lower()
        land_use_str = str(state.land_use or "").lower()
        is_monoculture = (
            "monoculture" in str(state.monoculture_or_polyculture or "").lower() or
            "monoculture" in land_use_str
        )
        pollinator_str = str(state.pollinator_presence or "").lower()
        is_low_pollinator = any(w in pollinator_str for w in ["low", "absent", "rare"])
        pesticide_str = str(state.pesticide_intensity or "").lower()

        # Prioritize interventions
        selected_interventions: List[AgroecologicalIntervention] = []

        # 1. Carbon & Water Stress -> Cover crops
        if (soc is not None and soc < 1.5) or "low" in rainfall_str or is_monoculture:
            selected_interventions.append(INTERVENTION_CATALOG[0])  # INT-COV-01: Cover Cropping

        # 2. Monoculture / Wind / Microclimate / Semi-Arid -> Agroforestry Belts
        if is_monoculture or "semi-arid" in str(state.region or "").lower() or (state.temperature and state.temperature > 28):
            selected_interventions.append(INTERVENTION_CATALOG[1])  # INT-AGR-02: Contour Agroforestry

        # 3. Pollinator Deficit / Pesticides / Field Margins -> Native Flowering Strips
        if is_low_pollinator or any(w in pesticide_str for w in ["high", "moderate"]) or is_monoculture:
            selected_interventions.append(INTERVENTION_CATALOG[2])  # INT-POL-03: Flowering Field Margins

        # 4. Monoculture Crop Diversification -> Strip Intercropping
        if is_monoculture and len(selected_interventions) < 3:
            selected_interventions.append(INTERVENTION_CATALOG[3])  # INT-INT-04: Strip Intercropping

        # 5. Water Stress / Sporadic Rainfall -> Swales
        if ("variab" in str(state.rainfall_variability or "").lower() or "drought" in str(state.drought_condition or "").lower()) and len(selected_interventions) < 3:
            selected_interventions.append(INTERVENTION_CATALOG[4])  # INT-WAT-05: Micro-Catchment Swales

        # Fallback to first two if none matched
        if not selected_interventions:
            selected_interventions = INTERVENTION_CATALOG[:2]

        # Build recommendation items with real scientific citations
        recommendation_items: List[RecommendationItem] = []

        for idx, intervention in enumerate(selected_interventions[:3]):
            # Assign relevant citations from retrieved evidence or specific domain matches
            matching_citations: List[CitationItem] = []

            for ev in retrieved_evidence:
                # Check domain or variable overlap
                has_var_overlap = any(
                    any(v.lower() in ev_var.lower() for ev_var in ev.variables)
                    for v in intervention.variables_addressed
                )
                if has_var_overlap or ev.environmental_domain.lower() in intervention.domain.lower():
                    matching_citations.append(
                        CitationItem(
                            source_organization=ev.organization,
                            title=ev.title,
                            year=ev.publication_year,
                            citation=ev.citation,
                            url=ev.url,
                            relevant_evidence=ev.excerpt[:220] + "..."
                        )
                    )

            # If no direct match in top-k, use the highest-ranked retrieved source
            if not matching_citations and retrieved_evidence:
                top_ev = retrieved_evidence[0]
                matching_citations.append(
                    CitationItem(
                        source_organization=top_ev.organization,
                        title=top_ev.title,
                        year=top_ev.publication_year,
                        citation=top_ev.citation,
                        url=top_ev.url,
                        relevant_evidence=top_ev.excerpt[:220] + "..."
                    )
                )

            # Compute transparent confidence
            conf_data = confidence_service.evaluate_confidence(
                environmental_state=state,
                evidence_list=[ev.model_dump() for ev in retrieved_evidence],
                variables_used=intervention.variables_addressed
            )

            rec_item = RecommendationItem(
                id=f"REC-{idx+1}-{intervention.id}",
                title=intervention.title,
                what_to_do=intervention.what_to_do,
                why_it_works=intervention.why_it_works,
                variables_involved=intervention.variables_addressed,
                impacted_metrics=intervention.impacted_metrics,
                time_horizon=intervention.time_horizon,
                expected_direction=intervention.expected_direction,
                confidence=conf_data["rating"],
                confidence_reason=conf_data["reason"],
                scientific_evidence=matching_citations,
                important_assumptions=intervention.assumptions,
                possible_trade_offs=intervention.trade_offs
            )
            recommendation_items.append(rec_item)

        return recommendation_items

recommendation_generator = RecommendationGenerator()
