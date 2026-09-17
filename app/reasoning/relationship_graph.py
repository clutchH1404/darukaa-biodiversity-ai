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

    def export_graph(self, state: Any = None) -> Dict[str, Any]:
        """
        Exports full structured environmental relationship graph as specified in Hackathon Section 11.
        Each node includes metric name, state, trend, source, related variables, and explanation.
        Each edge includes relationship type, direction, evidence, and explanation.
        """
        known_vars = {}
        if state is not None and hasattr(state, "get_known_variables"):
            known_vars = state.get_known_variables()
        elif isinstance(state, dict):
            known_vars = state

        NODE_METADATA = {
            "soil_organic_carbon": {"domain": "soil", "source": "FAO Recarbonizing Global Soils (2020)", "explanation": "Core determinant of soil aggregate stability and biological micro-habitats."},
            "soil_structure": {"domain": "soil", "source": "FAO / USDA Soil Quality (2020)", "explanation": "Macro-aggregate porosity governing gas exchange and hydrological infiltration."},
            "water_retention": {"domain": "hydrology", "source": "IPCC Climate Change & Land (2019)", "explanation": "Available water holding capacity buffering vegetation against acute dry spells."},
            "soil_moisture": {"domain": "hydrology", "source": "FAO Soils Technical Report (2020)", "explanation": "Root-zone volumetric matric potential sustaining transpiration."},
            "plant_resilience": {"domain": "vegetation", "source": "Science (Tamburini et al., 2020)", "explanation": "Vegetative physiological tolerance to meteorological anomalies."},
            "habitat_quality": {"domain": "biodiversity", "source": "IPBES Global Assessment (2019)", "explanation": "Structural complexity, nesting substrates, and floral resource continuity."},
            "biodiversity": {"domain": "biodiversity", "source": "Nature (Hooper et al., 2012)", "explanation": "Equilibrium of multi-trophic taxa underpinning biospheric resilience."},
            "species_richness": {"domain": "biodiversity", "source": "IPBES (2019)", "explanation": "Taxonomic count of coexisting floral and faunal species."},
            "rainfall": {"domain": "climate", "source": "IPCC SRCCL (2019)", "explanation": "Meteorological precipitation input dictating regional hydrological thresholds."},
            "water_availability": {"domain": "hydrology", "source": "UNEP GEO-6 (2019)", "explanation": "Net accessible water volume for plant root systems and riparian biotopes."},
            "water_stress": {"domain": "hydrology", "source": "IPCC SRCCL (2019)", "explanation": "Hydraulic xylem tension resulting from high vapor pressure deficit or soil drought."},
            "plant_survival": {"domain": "vegetation", "source": "Nature Plants (2017)", "explanation": "Viability and vegetative persistence under abiotic pressures."},
            "species_survival": {"domain": "biodiversity", "source": "IPBES (2019)", "explanation": "Metapopulation demographic stability across trophic levels."},
            "land_use_intensity": {"domain": "human_impact", "source": "IPBES Global Assessment (2019)", "explanation": "Anthropogenic cultivation pressure and chemical amendment frequency."},
            "monoculture": {"domain": "vegetation", "source": "Science (Tamburini et al., 2020)", "explanation": "Botanical uniformity eliminating micro-niches and floral succession."},
            "habitat_fragmentation": {"domain": "human_impact", "source": "IPBES (2019)", "explanation": "Patch division increasing edge effects and isolating genetic demes."},
            "spatial_heterogeneity": {"domain": "vegetation", "source": "IPBES (2019)", "explanation": "Landscape mosaic diversity of cover types, canopy heights, and phenologies."},
            "species_movement": {"domain": "biodiversity", "source": "Nature (Hooper et al., 2012)", "explanation": "Ecological dispersal corridors facilitating recolonization and gene flow."},
            "pesticide_intensity": {"domain": "human_impact", "source": "IPBES Pollinators Assessment (2016)", "explanation": "Chemical application load causing non-target ecotoxicological stress."},
            "non_target_toxicity": {"domain": "human_impact", "source": "IPBES (2016)", "explanation": "Sublethal physiological impairment of beneficial invertebrates."},
            "pollinator_abundance": {"domain": "biodiversity", "source": "IPBES (2016)", "explanation": "Population densities of wild bees, hoverflies, and lepidopterans."},
            "soil_ph": {"domain": "soil", "source": "FAO Technical Manual (2020)", "explanation": "Chemical acidity/alkalinity controlling cation exchange and nutrient mobility."},
            "nutrient_availability": {"domain": "soil", "source": "FAO (2020)", "explanation": "Bioavailable nitrogen, phosphorus, and potassium in soil solution."},
            "microbial_diversity": {"domain": "soil", "source": "Nature (2012)", "explanation": "Taxonomic richness of mycorrhizal fungi and rhizosphere bacterial communities."},
            "decomposition_cycling": {"domain": "soil", "source": "FAO (2020)", "explanation": "Microbial enzymatic mineralization of organic residues into humus."},
            "deforestation": {"domain": "human_impact", "source": "UNEP GEO-6 (2019)", "explanation": "Removal of perennial canopy exposing soil to solar radiation and kinetic rain."},
            "erosion_risk": {"domain": "soil", "source": "FAO (2020)", "explanation": "Vulnerability of superficial topsoil horizons to wind and rill detachment."},
            "microclimate_stability": {"domain": "climate", "source": "IPCC SRCCL (2019)", "explanation": "Boundary-layer thermal and humidity buffering provided by vegetation cover."},
            "temperature": {"domain": "climate", "source": "IPCC (2019)", "explanation": "Ambient thermal kinetic energy driving vapor pressure deficit and evapotranspiration."}
        }

        nodes_out = []
        for n in self.nodes:
            meta = NODE_METADATA.get(n, {
                "domain": "general_ecosystem",
                "source": "Darukaa.Earth Domain Ontology",
                "explanation": f"Biophysical parameter: {n.replace('_', ' ')}."
            })
            curr_val = known_vars.get(n, None)
            state_str = str(curr_val) if curr_val is not None else "unmeasured"
            trend = "depleted / stressed" if curr_val in ["low", "acidic", "alkaline"] or (isinstance(curr_val, (int, float)) and curr_val < 1.0) else "stable / baseline"

            nodes_out.append({
                "id": n,
                "metric": n.replace("_", " ").title(),
                "domain": meta["domain"],
                "current_state": state_str,
                "trend": trend if curr_val is not None else "unknown",
                "source": meta["source"],
                "related_variables": self.get_related_variables(n),
                "explanation": meta["explanation"]
            })

        edges_out = []
        for src, dst, pol, mech in self.edges:
            edges_out.append({
                "source": src,
                "target": dst,
                "relationship_type": "causal_reinforcing" if pol == 1 else "causal_attenuating",
                "direction": "positive (+1)" if pol == 1 else "negative (-1)",
                "evidence": mech,
                "explanation": f"{src.replace('_', ' ').title()} {'promotes' if pol == 1 else 'suppresses'} {dst.replace('_', ' ').title()} via: {mech}."
            })

        return {
            "metadata": {
                "total_nodes": len(nodes_out),
                "total_edges": len(edges_out),
                "causal_target": "biodiversity",
                "description": "Evidence-grounded biophysical causal directed graph mapping ecological cascades."
            },
            "nodes": nodes_out,
            "edges": edges_out
        }

relationship_graph = EnvironmentalRelationshipGraph()
