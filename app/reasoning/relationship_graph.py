from typing import Dict, List, Any, Tuple

class EnvironmentalRelationshipGraph:
    """
    Configurable directed causal graph mapping environmental variables
    through biophysical mechanisms to ecological outcomes.
    """

    def __init__(self):
        self.nodes = [
            "soil_organic_carbon", "soil_structure", "water_retention", "soil_moisture",
            "plant_resilience", "habitat_quality", "biodiversity", "species_richness",
            "rainfall", "water_availability", "water_stress", "plant_survival", "species_survival",
            "land_use_intensity", "monoculture", "habitat_fragmentation", "spatial_heterogeneity",
            "species_movement", "pesticide_intensity", "non_target_toxicity", "pollinator_abundance",
            "soil_ph", "nutrient_availability", "microbial_diversity", "decomposition_cycling",
            "deforestation", "erosion_risk", "microclimate_stability", "temperature"
        ]

        # Directed causal edges: (source, target, polarity, mechanism)
        # polarity: +1 (positive correlation), -1 (negative correlation)
        self.edges = [
            # Carbon-Moisture-Habitat cascade
            ("soil_organic_carbon", "soil_structure", 1, "Humic substances aggregate mineral particles into stable peds"),
            ("soil_structure", "water_retention", 1, "Pore network tortuosity increases plant-available water holding capacity (AWHC)"),
            ("water_retention", "soil_moisture", 1, "Sustains capillary water against gravitational drainage and evaporation"),
            ("soil_moisture", "plant_resilience", 1, "Buffers crops and native flora during dry spells"),
            ("plant_resilience", "habitat_quality", 1, "Provides continuous vegetation cover, root exudates, and structural niche complexity"),
            ("habitat_quality", "biodiversity", 1, "Supports diverse trophic levels, invertebrate communities, and vertebrate guilds"),

            # Rainfall-Hydrology cascade
            ("rainfall", "water_availability", 1, "Replenishes root zone moisture and local groundwater tables"),
            ("rainfall", "water_stress", -1, "Adequate rainfall diminishes plant hydraulic tension"),
            ("water_stress", "plant_survival", -1, "High xylem cavitation risk under acute matric water potential stress"),
            ("plant_survival", "species_survival", 1, "Underpins primary productivity and consumer food webs"),

            # Land-use / Monoculture cascade
            ("land_use_intensity", "habitat_fragmentation", 1, "Continuous arable expansion segments remnant natural biotopes"),
            ("monoculture", "spatial_heterogeneity", -1, "Eliminates botanical variety and multi-tiered canopy structure"),
            ("habitat_fragmentation", "species_movement", -1, "Disrupts ecological corridors and dispersal pathways"),
            ("spatial_heterogeneity", "species_richness", 1, "Higher niche dimensionality permits coexistence of more species"),
            ("species_movement", "species_richness", 1, "Facilitates gene flow and metapopulation recolonization"),

            # Chemical & Pesticide cascade
            ("pesticide_intensity", "non_target_toxicity", 1, "Insecticides and fungicides spill into floral resources and soil horizons"),
            ("non_target_toxicity", "pollinator_abundance", -1, "Impaired orientation, physiological mortality, and brood loss in wild apoidea"),
            ("non_target_toxicity", "microbial_diversity", -1, "Suppression of mycorrhizal fungi and beneficial bacterial taxa"),
            ("pollinator_abundance", "biodiversity", 1, "Drives angiosperm sexual reproduction and seed production"),

            # Soil Chemical cascade
            ("soil_ph", "nutrient_availability", 1, "Optimal pH 6.0-7.2 maximizes cationic bioavailability (P, N, K, Ca, Mg)"),
            ("nutrient_availability", "microbial_diversity", 1, "Balanced chemical environment stimulates rhizosphere microflora"),
            ("microbial_diversity", "decomposition_cycling", 1, "Enzymatic breakdown converts recalcitrant residues into bioavailable nutrients"),
            ("decomposition_cycling", "soil_structure", 1, "Microbial glues (glomalin) solidify soil aggregates"),

            # Deforestation & Microclimate cascade
            ("deforestation", "erosion_risk", 1, "Loss of root binding and canopy interception exposes topsoil to kinetic rain impact"),
            ("deforestation", "microclimate_stability", -1, "Amplifies diurnal temperature swings and reduces boundary layer humidity"),
            ("temperature", "water_stress", 1, "Elevated vapor pressure deficit (VPD) accelerates transpiration"),
        ]

    def trace_pathways(self, starting_variable: str, target_variable: str = "biodiversity") -> List[List[Tuple[str, str, int, str]]]:
        """Finds causal pathways from a measured variable to an ecological endpoint."""
        paths = []

        def dfs(current: str, current_path: List[Tuple[str, str, int, str]], visited: set):
            if current == target_variable:
                paths.append(list(current_path))
                return
            for src, dst, pol, mech in self.edges:
                if src == current and dst not in visited:
                    visited.add(dst)
                    current_path.append((src, dst, pol, mech))
                    dfs(dst, current_path, visited)
                    current_path.pop()
                    visited.remove(dst)

        dfs(starting_variable, [], {starting_variable})
        return paths

    def get_related_variables(self, variable_name: str) -> List[str]:
        """Returns direct incoming and outgoing variables."""
        related = set()
        for src, dst, _, _ in self.edges:
            if src == variable_name:
                related.add(dst)
            elif dst == variable_name:
                related.add(src)
        return list(related)

    def explain_chain(self, pathway: List[Tuple[str, str, int, str]]) -> str:
        """Converts a causal pathway into an explanatory scientific sentence."""
        steps = []
        for src, dst, pol, mech in pathway:
            direction = "enhances" if pol == 1 else "attenuates / suppresses"
            src_clean = src.replace("_", " ")
            dst_clean = dst.replace("_", " ")
            steps.append(f"{src_clean} {direction} {dst_clean} ({mech})")
        return " → ".join(steps)

relationship_graph = EnvironmentalRelationshipGraph()
