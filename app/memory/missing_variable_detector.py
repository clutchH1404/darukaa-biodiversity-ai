import re
from typing import Dict, Any, List, Optional
from ..models.environmental_state import EnvironmentalState
from ..models.response_models import MissingVariableQuestion

class MissingVariableDetector:
    """
    Dynamically identifies missing critical environmental variables.
    Prevents generic answers by asking targeted questions when information is incomplete,
    and ensures previously collected variables are never re-queried.
    """

    KEY_MEASUREMENTS = [
        {
            "variable": "soil_organic_carbon",
            "question": "What is your approximate Soil Organic Carbon (SOC %)? If unknown, is the soil visibly pale/eroded or dark/humus-rich?",
            "importance": "Critical: Determines soil aggregate stability, microbial habitat, and available water holding capacity.",
            "options": ["< 0.5% (Very low)", "0.5% - 1.2% (Low/Degraded)", "1.2% - 2.5% (Moderate)", "> 2.5% (Healthy)"]
        },
        {
            "variable": "rainfall",
            "question": "What is your typical annual precipitation or irrigation access?",
            "importance": "Critical: Dictates hydrological stress and species survival thresholds.",
            "options": ["Low (<400mm / Semi-arid)", "Moderate (400-800mm)", "High (>800mm)", "Irrigated"]
        },
        {
            "variable": "land_use",
            "question": "What is the primary current land-use or cropping system?",
            "importance": "Critical: Defines physical vegetation structure and landscape heterogeneity.",
            "options": ["Continuous cereal monoculture (wheat/corn)", "Crop rotation", "Pasture/Grazing", "Orchard/Agroforestry"]
        },
        {
            "variable": "soil_ph",
            "question": "Do you have a recent soil pH measurement?",
            "importance": "High: Dictates nutrient availability and rhizosphere microbial activity.",
            "options": ["Acidic (< 5.8)", "Optimal neutral (6.0 - 7.3)", "Alkaline / Calcareous (> 7.5)", "Unknown"]
        },
        {
            "variable": "region",
            "question": "What is your approximate geographic region or climate zone?",
            "importance": "High: Calibrates evapotranspiration rates and regional native biodiversity baselines.",
            "options": ["Semi-arid / Dryland", "Temperate continental", "Mediterranean", "Tropical / Subtropical"]
        }
    ]

    def extract_variables_from_text(self, text: str) -> Dict[str, Any]:
        """
        Extracts mentioned environmental parameters from natural language user query.
        """
        extracted = {}
        lower_text = text.lower()

        # SOC detection (e.g., "0.3% SOC", "soil carbon is 0.3", "organic carbon 1.2")
        soc_match = re.search(r"(\d+(?:\.\d+)?)\s*%\s*(?:soc|soil organic carbon|carbon)", lower_text)
        if not soc_match:
            soc_match = re.search(r"(?:soc|organic carbon|soil carbon)\s*(?:is|of|=|:)?\s*(\d+(?:\.\d+)?)\s*%?", lower_text)
        if soc_match:
            try:
                extracted["soil_organic_carbon"] = float(soc_match.group(1))
            except ValueError:
                pass

        # pH detection (e.g. "ph 6.8", "soil ph: 7.2")
        ph_match = re.search(r"(?:soil\s*)?ph\s*(?:is|of|=|:)?\s*(\d+(?:\.\d+)?)", lower_text)
        if ph_match:
            try:
                extracted["soil_ph"] = float(ph_match.group(1))
            except ValueError:
                pass

        # Moisture detection
        moist_match = re.search(r"(\d+(?:\.\d+)?)\s*%\s*(?:soil\s*)?moisture", lower_text)
        if moist_match:
            try:
                extracted["soil_moisture"] = float(moist_match.group(1))
            except ValueError:
                pass

        # Rainfall detection
        if "low rainfall" in lower_text or "arid" in lower_text or "dryland" in lower_text:
            extracted["rainfall"] = "low"
        elif "high rainfall" in lower_text or "heavy rain" in lower_text:
            extracted["rainfall"] = "high"
        elif "moderate rainfall" in lower_text:
            extracted["rainfall"] = "moderate"

        # Land use detection
        if "monoculture wheat" in lower_text or "wheat monoculture" in lower_text:
            extracted["land_use"] = "monoculture wheat"
            extracted["monoculture_or_polyculture"] = "monoculture"
        elif "monoculture" in lower_text:
            extracted["land_use"] = "monoculture"
            extracted["monoculture_or_polyculture"] = "monoculture"
        elif "polyculture" in lower_text or "mixed crop" in lower_text or "intercrop" in lower_text:
            extracted["monoculture_or_polyculture"] = "polyculture"

        # Region
        if "semi-arid" in lower_text or "semi arid" in lower_text:
            extracted["region"] = "semi-arid"
        elif "mediterranean" in lower_text:
            extracted["region"] = "Mediterranean"
        elif "tropical" in lower_text:
            extracted["region"] = "tropical"

        # Pesticide
        if "high pesticide" in lower_text or "heavy pesticide" in lower_text:
            extracted["pesticide_intensity"] = "high"
        elif "low pesticide" in lower_text or "organic" in lower_text:
            extracted["pesticide_intensity"] = "low"

        # Pollinators
        if "low pollinator" in lower_text or "no bees" in lower_text or "few pollinators" in lower_text:
            extracted["pollinator_presence"] = "low"

        # Richness / biodiversity
        if "low biodiversity" in lower_text or "low species richness" in lower_text:
            extracted["species_richness"] = "low"

        return extracted

    def detect_missing(
        self,
        current_state: EnvironmentalState,
        max_questions: int = 4
    ) -> List[MissingVariableQuestion]:
        """
        Returns targeted questions for missing high-priority variables.
        Never asks for variables that already have non-null values.
        """
        known_vars = current_state.get_known_variables()
        missing_questions: List[MissingVariableQuestion] = []

        for item in self.KEY_MEASUREMENTS:
            var_name = item["variable"]
            if var_name not in known_vars or known_vars[var_name] is None:
                missing_questions.append(
                    MissingVariableQuestion(
                        variable_name=var_name,
                        question_text=item["question"],
                        importance=item["importance"],
                        suggested_options=item["options"]
                    )
                )
                if len(missing_questions) >= max_questions:
                    break

        return missing_questions

missing_variable_detector = MissingVariableDetector()
