import pandas as pd
import altair as alt
from typing import Dict, Any

def render_soil_health_chart(state_dict: Dict[str, Any]):
    """
    Renders an interactive comparative bar chart of soil health metrics against target thresholds.
    """
    soc = state_dict.get("soil_organic_carbon")
    soc_val = float(soc) if soc is not None else 0.5

    moisture = state_dict.get("soil_moisture")
    moist_val = float(moisture) if moisture is not None else 20.0

    ph = state_dict.get("soil_ph")
    ph_norm = (float(ph) / 14.0 * 100.0) if ph is not None else 50.0

    # Normalized comparison (Current vs Resilient Target)
    data = pd.DataFrame([
        {"Metric": "Soil Organic Carbon (% × 25)", "Category": "Observed", "Score": min(100.0, soc_val * 25.0)},
        {"Metric": "Soil Organic Carbon (% × 25)", "Category": "Resilient Target", "Score": 75.0},
        
        {"Metric": "Soil Moisture (% Vol)", "Category": "Observed", "Score": min(100.0, moist_val * 2.0)},
        {"Metric": "Soil Moisture (% Vol)", "Category": "Resilient Target", "Score": 70.0},
        
        {"Metric": "Soil pH Balance (% Optimal)", "Category": "Observed", "Score": ph_norm},
        {"Metric": "Soil pH Balance (% Optimal)", "Category": "Resilient Target", "Score": 50.0},
    ])

    chart = alt.Chart(data).mark_bar(cornerRadius=6).encode(
        x=alt.X("Score:Q", title="Relative Agroecological Health Score (0-100)", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Metric:N", title="", sort=None),
        color=alt.Color("Category:N", scale=alt.Scale(domain=["Observed", "Resilient Target"], range=["#06B6D4", "#10B981"])),
        yOffset="Category:N",
        tooltip=["Metric", "Category", "Score"]
    ).properties(
        height=220,
        title="Soil Health Metrics vs Resilient Agroecological Targets"
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        labelColor="#94A3B8",
        titleColor="#E2E8F0",
        gridColor="#1E293B"
    ).configure_title(
        color="#F8FAFC",
        fontSize=14
    )

    return chart

def render_biodiversity_indicators(state_dict: Dict[str, Any]):
    """
    Renders visual indicators for biodiversity, pollinator presence, and habitat diversity.
    """
    richness = str(state_dict.get("species_richness", "low")).lower()
    pollinator = str(state_dict.get("pollinator_presence", "low")).lower()
    habitat = str(state_dict.get("habitat_diversity", "low")).lower()
    frag = str(state_dict.get("habitat_fragmentation", "moderate")).lower()

    def map_level(val: str, invert: bool = False) -> int:
        if "high" in val or "severe" in val:
            lvl = 85
        elif "mod" in val:
            lvl = 50
        else:
            lvl = 20
        return 100 - lvl if invert else lvl

    data = pd.DataFrame([
        {"Indicator": "Species Richness", "Score": map_level(richness), "Status": richness.title()},
        {"Indicator": "Pollinator Abundance", "Score": map_level(pollinator), "Status": pollinator.title()},
        {"Indicator": "Habitat Heterogeneity", "Score": map_level(habitat), "Status": habitat.title()},
        {"Indicator": "Landscape Connectivity", "Score": map_level(frag, invert=True), "Status": f"Frag: {frag.title()}"},
    ])

    chart = alt.Chart(data).mark_bar(cornerRadius=4).encode(
        x=alt.X("Score:Q", scale=alt.Scale(domain=[0, 100]), title="Ecological Integrity Index"),
        y=alt.Y("Indicator:N", sort=None, title=""),
        color=alt.Color("Score:Q", scale=alt.Scale(scheme="redyellowgreen", domain=[0, 100]), legend=None),
        tooltip=["Indicator", "Score", "Status"]
    ).properties(
        height=200,
        title="Biodiversity & Landscape Indicators"
    ).configure_axis(
        labelColor="#94A3B8",
        titleColor="#E2E8F0",
        gridColor="#1E293B"
    ).configure_title(
        color="#F8FAFC",
        fontSize=14
    )

    return chart

def render_relationship_graph():
    """
    Generates Graphviz DOT syntax for the interactive relationship graph.
    """
    dot = """
    digraph G {
        bgcolor="transparent";
        rankdir=LR;
        node [shape=box, style="filled,rounded", fontname="Inter", fontsize=10, fontcolor="#F8FAFC", fillcolor="#1E293B", color="#334155", penwidth=1.5];
        edge [fontname="Inter", fontsize=8, color="#06B6D4", fontcolor="#94A3B8", penwidth=1.2];

        SOC [label="Soil Organic Carbon\\n(% SOC)", fillcolor="#064E3B", color="#10B981"];
        Structure [label="Soil Structure\\n& Aggregation"];
        AWHC [label="Water Retention\\n(AWHC)"];
        Rainfall [label="Rainfall\\n& Moisture", fillcolor="#0C4A6E", color="#0284C7"];
        WaterStress [label="Plant Water\\nStress", fillcolor="#7F1D1D", color="#EF4444"];
        Monoculture [label="Monoculture\\nCropping", fillcolor="#78350F", color="#F59E0B"];
        Heterogeneity [label="Spatial\\nHeterogeneity"];
        Pollinators [label="Wild Pollinators\\n& Invertebrates"];
        Biodiversity [label="Biodiversity &\\nCrop Resilience", fillcolor="#047857", color="#34D399"];

        SOC -> Structure [label="+ glomalin"];
        Structure -> AWHC [label="+ porosity"];
        AWHC -> WaterStress [label="- matric tension", color="#10B981"];
        Rainfall -> AWHC [label="+ recharge"];
        WaterStress -> Biodiversity [label="- drought mortality", color="#EF4444"];
        Monoculture -> Heterogeneity [label="- niche space", color="#EF4444"];
        Heterogeneity -> Pollinators [label="+ continuous forage"];
        Pollinators -> Biodiversity [label="+ pollination"];
        Structure -> Biodiversity [label="+ soil fauna"];
    }
    """
    return dot
