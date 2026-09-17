from typing import Dict, Any, List
from ..models.environmental_state import EnvironmentalState

class BottleneckDetector:
    """
    Detects critical limiting factors and compounding ecological bottlenecks
    by cross-referencing soil, climate, land, biodiversity, and human disturbance variables.
    """

    def analyze_bottlenecks(self, state: EnvironmentalState) -> List[Dict[str, Any]]:
        bottlenecks = []
        known = state.get_known_variables()

        # Variable extractions & standardizations
        soc = state.soil_organic_carbon
        ph = state.soil_ph
        moisture = state.soil_moisture
        temp = state.temperature
        
        rainfall_val = str(state.rainfall or "").lower()
        land_use_val = str(state.land_use or "").lower()
        is_monoculture = (
            "monoculture" in str(state.monoculture_or_polyculture or "").lower() or
            "monoculture" in land_use_val or
            "single crop" in land_use_val
        )
        pesticide_val = str(state.pesticide_intensity or "").lower()
        pollinator_val = str(state.pollinator_presence or "").lower()
        fragmentation_val = str(state.habitat_fragmentation or "").lower()
        richness_val = str(state.species_richness or "").lower()
        water_stress_val = str(state.water_stress or "").lower()
        pollution_val = str(state.pollution_level or "").lower()

        # Bottleneck 1: Desiccation & Soil Structural Collapse (Carbon-Water-Land nexus)
        is_low_soc = soc is not None and soc < 1.0
        is_low_rain = "low" in rainfall_val or (isinstance(state.rainfall, (int, float)) and state.rainfall < 400)
        
        if is_low_soc and (is_low_rain or "drought" in str(state.drought_condition or "").lower()):
            bottlenecks.append({
                "name": "Soil Structural Degradation & Moisture Retention Deficit",
                "severity": "CRITICAL" if is_monoculture else "HIGH",
                "variables_involved": ["soil_organic_carbon", "rainfall", "soil_moisture", "land_use"],
                "description": (
                    f"Critically depleted soil organic carbon ({soc}% SOC) restricts aggregate formation and pore volume. "
                    f"Coupled with low precipitation ({state.rainfall}), this severely limits Available Water Capacity (AWC), "
                    f"driving acute matric water stress and biological desiccation."
                ),
                "synergy_factors": ["monoculture" if is_monoculture else "annual cropping", "low infiltration"]
            })

        # Bottleneck 2: Monoculture Landscape Homogenization & Trophic Niche Scarcity
        if is_monoculture and ("low" in richness_val or "fragmented" in fragmentation_val or not state.species_richness):
            bottlenecks.append({
                "name": "Spatial Homogenization & Habitat Niche Depletion",
                "severity": "HIGH",
                "variables_involved": ["land_use", "habitat_diversity", "species_richness", "habitat_fragmentation"],
                "description": (
                    f"Continuous monoculture farming ({state.land_use or 'single crop'}) eliminates botanical diversity and vertical vegetation strata. "
                    f"This removes vital floral resources, nesting substrates, and overwintering habitats for invertebrates and beneficial predators."
                ),
                "synergy_factors": ["landscape simplification", "intermittent bare soil"]
            })

        # Bottleneck 3: Agro-chemical Pollinator & Microbial Toxicity
        is_high_pesticide = any(w in pesticide_val for w in ["high", "intensive", "severe", "frequent"])
        is_low_pollinator = any(w in pollinator_val for w in ["low", "absent", "rare", "declining"])
        if is_high_pesticide or (is_low_pollinator and is_monoculture):
            bottlenecks.append({
                "name": "Ecotoxicological Pressure on Beneficial Entomofauna & Microbiome",
                "severity": "HIGH" if is_high_pesticide else "MODERATE",
                "variables_involved": ["pesticide_intensity", "pollinator_presence", "microbial_diversity"],
                "description": (
                    "Chemical application pressures and lack of non-crop floral forage create acute ecotoxicity for wild pollinators "
                    "and inhibit symbiotic arbuscular mycorrhizal fungi in the rhizosphere."
                ),
                "synergy_factors": ["synthetic inputs", "lack of pollen succession"]
            })

        # Bottleneck 4: Edaphic Chemical Lockup (pH Extremes)
        if ph is not None and (ph < 5.5 or ph > 8.0):
            status = "Acidic aluminum/manganese toxicity" if ph < 5.5 else "Alkaline phosphorus/micronutrient fixation"
            bottlenecks.append({
                "name": f"Edaphic Chemical Constraint ({status})",
                "severity": "HIGH",
                "variables_involved": ["soil_ph", "soil_organic_carbon", "microbial_diversity"],
                "description": (
                    f"Soil pH of {ph} disrupts cationic exchange capacity and enzymatic functionality of nitrifying and decomposer bacteria."
                ),
                "synergy_factors": ["nutrient immobilization", "inhibited mineralization"]
            })

        # Bottleneck 5: Urban-Fringe Fragmentation & Contaminant Runoff
        is_high_pollution = any(w in pollution_val for w in ["moderate", "high", "severe"])
        is_fragmented = any(w in fragmentation_val for w in ["high", "severe", "fragmented"])
        if is_fragmented or is_high_pollution:
            bottlenecks.append({
                "name": "Landscape Fragmentation & Anthropogenic Disturbance",
                "severity": "MODERATE",
                "variables_involved": ["habitat_fragmentation", "pollution_level", "species_richness"],
                "description": (
                    "Physical barriers to biological movement combined with chemical contaminants truncate meta-population connectivity "
                    "and impede gene flow across remnant habitat patches."
                ),
                "synergy_factors": ["edge effects", "corridor severance"]
            })

        # If no explicit bottleneck matched, provide systemic baseline
        if not bottlenecks:
            bottlenecks.append({
                "name": "General Agroecosystem Imbalance",
                "severity": "MODERATE",
                "variables_involved": ["soil_organic_carbon", "habitat_diversity", "species_richness"],
                "description": "Baseline vulnerability detected across soil carbon balance and biological diversity indicators.",
                "synergy_factors": ["suboptimal organic matter replenishment"]
            })

        return bottlenecks

bottleneck_detector = BottleneckDetector()
