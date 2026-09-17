# Darukaa.Earth AI Biodiversity Intelligence: System Architecture

## 1. Executive Summary
**Darukaa.Earth** is an AI-powered conversational environmental intelligence system engineered to behave like an expert AI Environmental Scientist rather than a generic conversational model. 

Traditional LLMs suffer from severe limitations when applied to ecological domains:
- Hallucination of species names, recovery rates, and yield impacts.
- Generic recommendations ("plant trees", "use compost", "reduce pesticides").
- Disregard of biophysical limiting factors (e.g., suggesting water-intensive cover crops in semi-arid zones with <300 mm rainfall).
- Disconnected single-metric responses (failing to see how soil carbon dictates water retention and pollinator forage).

Darukaa.Earth eliminates these issues by coupling:
1. **Multi-Metric Causal Reasoning Engine** ($G = (V, E)$ directed graph) that mandates combining at least 3 environmental variables before recommending interventions.
2. **Authoritative RAG Retrieval Pipeline** grounded exclusively in genuine publications from FAO, IPCC, UNEP, IPBES, CGIAR, US EPA, and high-impact peer-reviewed journals.
3. **Transparent Confidence Calculation** factoring input completeness, retrieval quality, evidence density, and source reliability.
4. **Dynamic Missing Variable Detector** that inquires about critical unmeasured metrics before rushing to conclusions.

---

## 2. End-to-End Information Flow
```
               User Query / Structured JSON
                            │
                            ▼
               [Security Guard & Input Sanitizer]
               (Neutralizes Prompt Injections)
                            │
                            ▼
          [Dynamic Missing Information Detector]
        (Checks Soil, Land, Climate, Water, Bio)
                            │
               ┌────────────┴────────────┐
               ▼                         ▼
      [Clarifying Questions]   [Cumulative Session Memory]
      (If critical vars missing) (SQLite & In-Memory Store)
                            │
                            ▼
           [Multi-Metric Reasoning Engine]
         - Metric Bottleneck Assessment
         - Directed Causal Graph Traversal
         - Tri-Variable Causal Synthesis
                            │
                            ▼
           [Authoritative RAG Vector Pipeline]
         - ChromaDB Persistent HNSW Index
         - Semantic + Domain + Geo Hybrid Ranking
         - Passive Data Delimitation (<evidence_item>)
                            │
                            ▼
           [Agroecological Intervention Engine]
         - Context-Sensitive Intervention Mapping
         - 10-Point Recommendation Synthesis (A-J)
         - Factorized Scientific Confidence
                            │
                            ▼
     [Structured Response & Scientific Citations]
    (Markdown Schema + Interactive Altair & Graphviz UI)
```

---

## 3. The 6 Environmental Domains & Measured Variables

| Domain | Variables Analyzed | Typical Bottlenecks Identified |
|---|---|---|
| **SOIL** | `soil_ph`, `soil_organic_carbon` (SOC %), `soil_moisture` | Structural aggregate breakdown, crusting, acidification, available water capacity deficit |
| **LAND** | `land_use`, `land_cover`, `monoculture_or_polyculture`, `habitat_diversity`, `habitat_fragmentation` | Landscape homogenization, loss of structural micro-refugia, dispersal barriers |
| **BIODIVERSITY** | `species_richness`, `species_diversity`, `pollinator_presence`, `microbial_diversity` | Trophic collapse, pollinator deficit, rhizosphere mycorrhizal suppression |
| **CLIMATE** | `temperature`, `rainfall`, `rainfall_variability`, `drought_condition` | High vapor pressure deficit (VPD), terminal drought stress, thermal shock |
| **HUMAN IMPACT** | `pollution_level`, `pesticide_intensity`, `deforestation_level`, `urbanization`, `land_disturbance` | Non-target entomofauna mortality, intensive tillage oxidation of carbon |
| **WATER** | `water_availability`, `irrigation`, `water_stress` | Hydrological desiccation, vadose zone depletion, excessive runoff |

---

## 4. Multi-Metric Causal Relationship Graph
The biophysical reasoning engine models cascades of interactions:

$$\text{SOC} \uparrow \xrightarrow{+ \text{glomalin}} \text{Soil Aggregate Stability} \uparrow \xrightarrow{+ \text{porosity}} \text{Available Water Capacity} \uparrow \xrightarrow{- \text{tension}} \text{Crop Water Stress} \downarrow$$

$$\text{Continuous Monoculture} \xrightarrow{- \text{niche space}} \text{Spatial Heterogeneity} \downarrow \xrightarrow{- \text{floral succession}} \text{Pollinator Abundance} \downarrow \xrightarrow{- \text{pollination}} \text{Biodiversity} \downarrow$$

$$\text{Pesticide Intensity} \uparrow \xrightarrow{+ \text{toxicity}} \text{Beneficial Invertebrates} \downarrow \xrightarrow{- \text{predation}} \text{Secondary Pest Outbreaks} \uparrow$$

---

## 5. Anti-Hallucination & Grounding Safeguards
1. **Source Registry Lockdown**: Every cited report in an AI recommendation must exist in the SQLite `sources_registry` and ChromaDB vector database.
2. **Quantitative Protection**: The system never hallucinates percentage increases; quantitative ranges (e.g. `+0.2 to +0.5 t C/ha/yr`) are drawn strictly from empirical literature.
3. **Passive Context Delimitation**: Retrieved documents are wrapped inside `<evidence_item>` tags and treated strictly as data, preventing indirect prompt injection attacks.
