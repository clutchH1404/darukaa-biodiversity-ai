import re
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from .missing_variable_detector import missing_variable_detector
from ..models.environmental_state import EnvironmentalState
from ..models.response_models import MissingVariableQuestion

class QueryUnderstandingResult(BaseModel):
    query: str
    detected_variables: List[str]
    extracted_state: Dict[str, Any]
    missing_variables: List[str]
    missing_context_questions: List[MissingVariableQuestion]
    location: Dict[str, Any]
    ecosystem_context: Dict[str, Any]
    time_context: Dict[str, Any]
    confidence: float
    intent: str
    reasoning_prerequisites: List[str]

class EnvironmentalQueryUnderstander:
    """
    Robust environmental query understanding layer detecting 20+ variables,
    identifying missing context, and parsing spatial, temporal, and ecosystem indicators.
    """

    VARIABLE_LEXICON = {
        "soil_health": ["soil health", "poor soil", "healthy soil", "soil condition", "soil biology", "soil structure"],
        "soil_organic_matter": ["soil organic carbon", "soil organic matter", "soc", "humus", "carbon content", "organic content"],
        "soil_degradation": ["soil degradation", "eroded", "erosion", "compaction", "hardpan", "salinization", "nutrient depletion"],
        "water_availability": ["water availability", "water deficit", "water shortage", "irrigation", "water table", "drought stress"],
        "water_quality": ["water quality", "salinity", "runoff contamination", "turbidity", "eutrophication"],
        "rainfall": ["rainfall", "precipitation", "monsoon", "dry spell", "rainfed", "arid", "semi-arid", "annual rain"],
        "temperature": ["temperature", "heat stress", "thermal", "frost", "warm", "degrees", "celsius"],
        "climate": ["climate change", "climate zone", "arid climate", "tropical", "mediterranean", "temperate"],
        "vegetation": ["vegetation", "canopy", "ground cover", "understory", "biomass", "flora"],
        "native_vegetation": ["native vegetation", "native species", "endemic flora", "indigenous plants", "native trees"],
        "habitat_quality": ["habitat quality", "niche", "degraded habitat", "shelter", "foraging", "nesting"],
        "habitat_fragmentation": ["fragmentation", "fragmented", "patch", "isolation", "edge effect", "barrier"],
        "land_use": ["land use", "farming", "cropland", "pasture", "grazing", "orchard", "plantation"],
        "land_cover": ["land cover", "bare ground", "woodland", "scrubland", "tillage"],
        "biodiversity": ["biodiversity", "biodiversity decline", "loss of species", "biotic", "ecosystem diversity"],
        "species_richness": ["species richness", "species count", "few species", "diverse species", "monoculture"],
        "pollinators": ["pollinators", "bees", "wild bees", "butterflies", "hoverflies", "pollination", "honeybees"],
        "wildlife": ["wildlife", "fauna", "mammals", "birds", "avian", "invertebrates", "reptiles"],
        "ecosystem_resilience": ["ecosystem resilience", "resilience", "buffering capacity", "vulnerability", "recovery"],
        "connectivity": ["connectivity", "wildlife corridor", "habitat corridor", "stepping stones", "dispersal pathway"],
        "agriculture": ["agriculture", "agricultural", "farm", "farming", "crop", "harvest", "fertilizer", "pesticide"],
        "deforestation": ["deforestation", "clearing", "tree removal", "land clearing", "logging"],
        "restoration": ["restoration", "rewilding", "reforestation", "agroecology", "regenerative", "rehabilitate"]
    }

    ECOSYSTEM_MARKERS = {
        "tropical_rainforest": ["rainforest", "amazon", "equatorial", "jungle"],
        "savanna_cerrado": ["cerrado", "savanna", "grassland", "scrubland"],
        "semi_arid_dryland": ["semi-arid", "dryland", "steppe", "deccan", "sahel", "arid"],
        "mediterranean": ["mediterranean", "chaparral", "olive grove"],
        "temperate_cropland": ["temperate", "corn belt", "plains", "cereal belt"],
        "riparian_wetland": ["riparian", "river basin", "wetland", "floodplain", "catchment", "swale"]
    }

    LOCATION_PATTERNS = [
        r"\b(?:in|near|around|at)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)",
        r"(amazon\s+basin|cerrado|rift\s+valley|atlantic\s+forest|maharashtra|punjab|california|midwest)"
    ]

    def understand_query(self, query: str) -> QueryUnderstandingResult:
        lower_q = query.lower()
        detected_vars: List[str] = []

        # 1. Lexicon match for 20+ variables
        for var_name, terms in self.VARIABLE_LEXICON.items():
            if any(term in lower_q for term in terms):
                detected_vars.append(var_name)

        # 2. Extract quantitative state parameters using regex engine
        extracted_state = missing_variable_detector.extract_variables_from_text(query)
        for k in extracted_state.keys():
            if k not in detected_vars:
                detected_vars.append(k)

        # 3. Location extraction
        location_info: Dict[str, Any] = {}
        for pattern in self.LOCATION_PATTERNS:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                loc_text = match.group(1).strip()
                if loc_text.lower() not in ["what", "my", "our", "the"]:
                    location_info["name"] = loc_text
                    break

        if "maharashtra" in lower_q:
            location_info.update({"name": "Maharashtra, India", "region": "semi-arid", "country": "India"})
        elif "amazon" in lower_q:
            location_info.update({"name": "Amazon Basin", "region": "tropical", "country": "Brazil"})
        elif "cerrado" in lower_q:
            location_info.update({"name": "Cerrado Biome", "region": "savanna", "country": "Brazil"})
        elif "rift valley" in lower_q:
            location_info.update({"name": "East African Rift Valley", "region": "arid/semi-arid", "country": "Kenya/Ethiopia"})

        # 4. Ecosystem Context
        ecosystem_info: Dict[str, Any] = {}
        for eco_name, markers in self.ECOSYSTEM_MARKERS.items():
            if any(m in lower_q for m in markers):
                ecosystem_info["biome"] = eco_name
                break

        # 5. Time Context
        time_info: Dict[str, Any] = {"scale": "inter-annual"}
        if any(w in lower_q for w in ["rapid", "sudden", "this season", "current year", "recent"]):
            time_info["temporal_scope"] = "acute / seasonal"
        elif any(w in lower_q for w in ["decade", "years", "chronic", "declining over time", "historical"]):
            time_info["temporal_scope"] = "chronic / long-term"
        else:
            time_info["temporal_scope"] = "unspecified"

        # 6. Missing context detection
        temp_state = EnvironmentalState(**extracted_state)
        missing_questions = missing_variable_detector.detect_missing(temp_state)
        missing_vars = [q.variable_name for q in missing_questions]

        # 7. Confidence & Intent calculation
        confidence = round(min(0.95, 0.40 + (len(detected_vars) * 0.1) + (0.15 if location_info else 0.0)), 2)
        intent = "diagnostic_and_intervention_request" if ("what should" in lower_q or "how to" in lower_q or "recommend" in lower_q) else "environmental_observation"

        reasoning_prereqs = []
        if "biodiversity" in detected_vars and "water_availability" not in detected_vars:
            reasoning_prereqs.append("Requires hydrological context to distinguish between resource limitation and biophysical habitat loss.")
        if "soil_health" in detected_vars and "soil_organic_matter" not in detected_vars:
            reasoning_prereqs.append("Requires quantitative SOC % or organic amendment history to establish baseline fertility trajectory.")

        return QueryUnderstandingResult(
            query=query,
            detected_variables=detected_vars,
            extracted_state=extracted_state,
            missing_variables=missing_vars,
            missing_context_questions=missing_questions,
            location=location_info,
            ecosystem_context=ecosystem_info,
            time_context=time_info,
            confidence=confidence,
            intent=intent,
            reasoning_prerequisites=reasoning_prereqs
        )

query_understander = EnvironmentalQueryUnderstander()
