from typing import List, Dict, Any
from pydantic import BaseModel

class AgroecologicalIntervention(BaseModel):
    id: str
    title: str
    domain: str
    suitable_conditions: Dict[str, Any]
    variables_addressed: List[str]
    what_to_do: str
    why_it_works: str
    impacted_metrics: List[str]
    time_horizon: str
    expected_direction: str
    assumptions: List[str]
    trade_offs: List[str]

INTERVENTION_CATALOG: List[AgroecologicalIntervention] = [
    AgroecologicalIntervention(
        id="INT-COV-01",
        title="Legume-Grass Mixed Cover Cropping Between Cereal Cycles",
        domain="Soil Health & Water Conservation",
        suitable_conditions={"soil_organic_carbon_max": 1.5, "rainfall_zones": ["semi-arid", "sub-humid", "low", "moderate"]},
        variables_addressed=["soil_organic_carbon", "soil_moisture", "land_use", "biodiversity"],
        what_to_do="Introduce a bi-culture cover crop mixture (e.g., Vicia villosa / Hairy Vetch paired with Secale cereale / Cereal Rye) immediately post-harvest. Terminate via roller-crimper prior to main crop sowing to establish an in-situ organic mulch mat without soil inversion.",
        why_it_works="Living roots deposit rhizodeposits and mycorrhizal glomalin, binding silt and clay into water-stable macro-aggregates. The surface mulch layer attenuates solar radiation, lowering soil surface temperature by 4-8°C, suppressing vapor evaporation, and providing carbon substrate for subterranean detritivores and earthworms.",
        impacted_metrics=[
            "soil_organic_carbon ↑ (empirically supported +0.2 to +0.5 t C/ha/yr in temperate/semi-arid drylands)",
            "soil_moisture retention ↑ (+15% to +25% available water holding capacity)",
            "habitat_diversity ↑ (continuous ground cover for epigeic arthropods)",
            "weed_suppression ↑ (physical biomass barrier suppresses weed emergence by 60-80%)"
        ],
        time_horizon="Short (1 season for cover & moisture retention); Medium (2-3 years for measurable SOC increase)",
        expected_direction="SOC ↑, Soil Moisture Retention ↑, Infiltration ↑, Erosion ↓, Weed Emergence ↓",
        assumptions=[
            "Adequate residual autumn soil moisture or minimal precipitation (>250mm) to support cover germination",
            "Availability of roller-crimper or non-inversion termination equipment"
        ],
        trade_offs=[
            "Potential competition for early spring soil moisture if termination is delayed in drought-stressed regions",
            "Initial expenditure on certified legume-grass seed mixtures"
        ]
    ),
    AgroecologicalIntervention(
        id="INT-AGR-02",
        title="Contour Alley Cropping & Multi-Strata Agroforestry Belts",
        domain="Agroforestry & Microclimate Regulation",
        suitable_conditions={"land_use_types": ["cropland", "monoculture wheat", "monoculture"], "slope_or_wind": True},
        variables_addressed=["habitat_diversity", "soil_moisture", "temperature", "species_richness", "biodiversity"],
        what_to_do="Establish multi-species woody perennial hedgerows along contour lines at 24-30m intervals using drought-hardy nitrogen-fixing trees and shrubs (e.g., Faidherbia albida, Caragana arborescens, or native Prunus spinosa / Crataegus).",
        why_it_works="Woody canopy reduces boundary-layer wind velocity by 30-50%, drastically decreasing crop vapor pressure deficit (VPD) and crop transpiration stress. Deep perennial root systems create hydraulic lift, bringing moisture from lower vadose zones into the upper rooting profile while providing perennial structural niches and nesting sites for avian insectivores and wild apoidea.",
        impacted_metrics=[
            "microclimate_stability ↑ (lowers wind speed and summer crop canopy temperature peaks by 2-4°C)",
            "species_richness ↑ (+30% to +50% richness in bird, bat, and predatory carabid beetle populations)",
            "soil_organic_carbon ↑ (sub-canopy leaf litter and deep root turnover +0.3 t C/ha/yr)",
            "wind_erosion ↓ (up to 80% reduction in soil detachment)"
        ],
        time_horizon="Medium (2-3 years for windbreak establishment); Long (5+ years for full microclimatic buffer)",
        expected_direction="Microclimatic buffering ↑, Floral and Faunal Richness ↑, Deep Carbon Storage ↑, Evaporative Losses ↓",
        assumptions=[
            "Tree rows do not obstruct mechanized harvest swath widths",
            "Initial sapling protection from herbivory and rodent girdling during establishment"
        ],
        trade_offs=[
            "Loss of 3-5% effective arable field surface area dedicated to perennial tree rows",
            "Shading along immediate edge rows (within 2m of hedgerow)"
        ]
    ),
    AgroecologicalIntervention(
        id="INT-POL-03",
        title="Perennial Native Flowering Field Margins & Pollinator Corridors",
        domain="Pollinator Support & Pest Regulation",
        suitable_conditions={"pollinator_presence_low": True, "monoculture": True},
        variables_addressed=["pollinator_presence", "species_richness", "pesticide_intensity", "habitat_fragmentation"],
        what_to_do="Sow 3 to 6-meter-wide perennial flowering buffer strips along field boundaries and headlands using a high-diversity seed blend of native perennial forbs (Asteraceae, Fabaceae, Lamiaceae) with staggered flowering phenology from April through October.",
        why_it_works="Monoculture fields induce seasonal 'floral deserts' outside brief crop bloom windows. Continuous nectar and pollen succession sustains wild solitary bees, bumblebees, and parasitoid wasps. Undisturbed tussock grasses provide overwintering shelter for predatory spiders and beetles, enabling biological pest control into the crop interior up to 60m from field margins.",
        impacted_metrics=[
            "pollinator_presence ↑ (+40% to +100% wild bee abundance in adjacent field margins)",
            "biological_pest_control ↑ (+20% to +35% parasitism and predation of cereal aphids)",
            "species_richness ↑ (doubling of non-crop botanical and invertebrate taxa along margins)"
        ],
        time_horizon="Short (1 season for flowering visitor recruitment); Medium (2-3 years for stabilized perennial community)",
        expected_direction="Pollinator Abundance ↑, Parasitoid Wasps ↑, Crop Pest Pressure ↓, Boundary Botanical Diversity ↑",
        assumptions=[
            "Elimination or strict drift shielding of insecticides and synthetic herbicides within 10m of flowering strips",
            "Proper seedbed preparation to prevent aggressive invasive rhizomatous grass dominance"
        ],
        trade_offs=[
            "Periodic mowing or selective weeding required to prevent noxious weed encroachment",
            "Initial establishment costs for high-diversity regional ecotype native seeds"
        ]
    ),
    AgroecologicalIntervention(
        id="INT-INT-04",
        title="Cereal-Legume Strip Intercropping & Crop Rotation Diversification",
        domain="Cropping System Diversification",
        suitable_conditions={"monoculture": True, "land_use": "cropland"},
        variables_addressed=["land_use", "soil_organic_carbon", "habitat_diversity", "microbial_diversity"],
        what_to_do="Transition from continuous cereal monoculture to an alternating strip intercrop or 4-year rotational sequence (e.g., Wheat - Chickpea/Lentil - Barley - Mustard/Camelina).",
        why_it_works="Root exudates of varied botanical families stimulate differentiated rhizosphere bacterial and fungal communities, interrupting host-specific soil-borne pathogen cycles (such as Gaeumannomyces graminis / take-all). Legumes fix atmospheric nitrogen biologically ($N_2$), reducing dependence on synthetic ammonium fertilizers while producing easily decomposable low C:N residues that accelerate microbial biomass turnover.",
        impacted_metrics=[
            "microbial_diversity ↑ (+25% to +45% functional rhizosphere microbial diversity and enzymatic activity)",
            "synthetic_nitrogen_requirement ↓ (20-40 kg N/ha credit from biological fixation)",
            "habitat_diversity ↑ (multi-crop landscape mosaic breaks monoculture homogenization)"
        ],
        time_horizon="Short (1 growing season for disease break); Medium (2-4 years for full rotation benefits)",
        expected_direction="Soil Microbial Activity ↑, Soil-Borne Pathogens ↓, Synthetic Fertilizer Inputs ↓, Yield Stability ↑",
        assumptions=[
            "Viable local supply chain and market demand for grain legumes or oilseeds",
            "Equipment adjustable for variable row spacing and seed sizing"
        ],
        trade_offs=[
            "Requires more sophisticated farm management and harvest logistics for multiple grain types",
            "Legume yield sensitivity to pre-emergence herbicide carryover"
        ]
    ),
    AgroecologicalIntervention(
        id="INT-WAT-05",
        title="Contour Micro-Catchment Swales & Vegetated Buffer Filters",
        domain="Hydrological Restoration & Runoff Mitigation",
        suitable_conditions={"rainfall_variability": "high", "water_stress": True},
        variables_addressed=["water_availability", "soil_moisture", "rainfall", "soil_organic_carbon"],
        what_to_do="Excavate shallow contour retention swales and vegetated micro-catchments stabilized with deep-rooted native bunchgrasses (e.g., Vetiver, Chrysopogon or Stipa) along gentle slopes to intercept and infiltrate sheetwash runoff.",
        why_it_works="Rapid surface runoff in degraded low-carbon soils causes laminar soil erosion and escapes the root zone. Contour swales passively harvest sporadic high-intensity rainfall, converting destructive runoff into subterranean groundwater recharge and extending subsoil moisture availability by several weeks into dry seasons.",
        impacted_metrics=[
            "water_availability ↑ (+30% to +50% retention of storm event precipitation in root zone)",
            "topsoil_loss ↓ (up to 85% reduction in particulate sediment runoff)",
            "soil_moisture ↑ (sustained capillary water in down-slope crop bands)"
        ],
        time_horizon="Short (immediate storm runoff capture); Medium (1-2 years for vegetative stabilization)",
        expected_direction="Rainwater Infiltration ↑, Vadose Zone Moisture ↑, Gully Formation ↓, Nutrient Leaching ↓",
        assumptions=[
            "Swale grade must follow precise contour levels to prevent concentrated water blowout during extreme events",
            "Topography has gentle to moderate slope (1-8%)"
        ],
        trade_offs=[
            "Initial earthmoving labor and precision surveying required",
            "Temporary obstacle for heavy machinery unless incorporated into field border alleys"
        ]
    )
]
