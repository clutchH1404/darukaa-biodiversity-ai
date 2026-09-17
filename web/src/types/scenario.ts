import { EnvironmentalState } from "./api";

export interface JudgeScenarioPreset {
  id: string;
  label: string;
  biome: string;
  coordinates: string;
  focusProblem: string;
  variables: string[];
  defaultQuery: string;
  initialState: EnvironmentalState;
}

export const JUDGE_PRESETS: JudgeScenarioPreset[] = [
  {
    id: "amazon-04b",
    label: "Amazon Basin Sector 04B",
    biome: "Tropical Rainforest Frontier",
    coordinates: "03°08'40\"S 60°01'30\"W — MANAUS GRD",
    focusProblem: "Avian and pollinator biodiversity collapse, acute topsoil desiccation (0.3% SOC), and severe buffer fragmentation.",
    variables: ["Soil Organic Carbon", "Pollinator Presence", "Habitat Fragmentation", "Rainfall"],
    defaultQuery: "My agricultural buffer in Sector 04B shows declining avian & pollinator biodiversity, depleted soil organic carbon at 0.3%, and accelerating topsoil desiccation under low rainfall.",
    initialState: {
      location_name: "Amazon Basin Sector 04B",
      latitude: -3.1333,
      longitude: -60.0167,
      region: "semi-arid tropical frontier",
      soil_organic_carbon: 0.3,
      soil_ph: 6.8,
      soil_moisture: 18.0,
      rainfall: "low",
      rainfall_variability: "high",
      land_use: "monoculture wheat",
      monoculture_or_polyculture: "monoculture",
      temperature: 31.0,
      species_richness: "low",
      pollinator_presence: "low",
      pollution_level: "moderate",
      drought_condition: "active",
      habitat_fragmentation: "0.82 (high)"
    }
  },
  {
    id: "cerrado-c12",
    label: "Cerrado Agricultural Fringe",
    biome: "Sub-Humid Savanna Scrub",
    coordinates: "12°14'20\"S 45°59'10\"W — MATO GROSSO",
    focusProblem: "Severe topsoil compaction and organic carbon oxidation following deep soybean monocropping cycles.",
    variables: ["Soil Structure", "SOC Oxidation", "Pesticide Intensity", "Native Bees"],
    defaultQuery: "Severe topsoil compaction and organic carbon oxidation following continuous monoculture cropping and high pesticide application across boundary sector C-12.",
    initialState: {
      location_name: "Cerrado Agricultural Fringe C-12",
      latitude: -12.2333,
      longitude: -45.9833,
      region: "sub-humid savannah fringe",
      soil_organic_carbon: 0.8,
      soil_ph: 5.4,
      soil_moisture: 22.0,
      rainfall: "moderate",
      land_use: "monoculture soybean",
      monoculture_or_polyculture: "monoculture",
      temperature: 29.0,
      species_richness: "low",
      pollinator_presence: "low",
      pesticide_intensity: "high"
    }
  },
  {
    id: "rift-valley-water",
    label: "Rift Valley Water Deficit",
    biome: "Semi-Arid Rift Basin",
    coordinates: "00°22'10\"N 36°05'20\"E — NAKURU BASIN",
    focusProblem: "Catastrophic water catchment drawdown impacting endemic amphibian colonies and migratory herbivore transit.",
    variables: ["Hydrological Stress", "Aquifer Drawdown", "Riparian Desiccation"],
    defaultQuery: "Catastrophic water catchment drawdown impacting endemic amphibian colonies and migratory herbivore watering transit points under acute drought conditions.",
    initialState: {
      location_name: "Rift Valley Catchment Zone",
      latitude: 0.3667,
      longitude: 36.0833,
      region: "semi-arid rift basin",
      soil_organic_carbon: 1.1,
      soil_ph: 7.8,
      soil_moisture: 14.0,
      rainfall: "low",
      water_availability: "scarce",
      water_stress: "severe",
      temperature: 33.0,
      species_richness: "low",
      drought_condition: "severe"
    }
  },
  {
    id: "atlantic-fragment-8",
    label: "Atlantic Forest Fragment #8",
    biome: "Coastal Montane Fragment",
    coordinates: "23°32'40\"S 46°38'10\"W — SERRA DO MAR",
    focusProblem: "Extreme matrix isolation of endangered arboreal mammal populations in isolated patches smaller than 25 hectares.",
    variables: ["Patch Isolation", "Edge Effect", "Matrix Resistance", "Corridors"],
    defaultQuery: "Extreme matrix isolation of endangered arboreal mammal populations in isolated forest fragments smaller than 25 hectares surrounded by intensive pasture.",
    initialState: {
      location_name: "Atlantic Forest Fragment #8",
      latitude: -23.5333,
      longitude: -46.6333,
      region: "coastal fragmented biome",
      soil_organic_carbon: 1.9,
      soil_ph: 6.2,
      habitat_fragmentation: "high",
      species_richness: "moderate",
      urbanization: "high",
      pollution_level: "moderate"
    }
  }
];
