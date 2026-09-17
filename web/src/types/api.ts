export interface EnvironmentalState {
  id?: string;
  location_name?: string;
  latitude?: number;
  longitude?: number;
  region?: string;
  country?: string;
  climate_zone?: string;
  soil_ph?: number;
  soil_organic_carbon?: number;
  soil_moisture?: number;
  land_use?: string;
  land_cover?: string;
  monoculture_or_polyculture?: string;
  habitat_diversity?: string | number;
  habitat_fragmentation?: string | number;
  species_richness?: string | number;
  species_diversity?: string | number;
  pollinator_presence?: string | number;
  microbial_diversity?: string | number;
  temperature?: number;
  rainfall?: string | number;
  rainfall_variability?: string;
  drought_condition?: string | boolean;
  pollution_level?: string | number;
  pesticide_intensity?: string | number;
  deforestation_level?: string | number;
  urbanization?: string | number;
  land_disturbance?: string | number;
  water_availability?: string | number;
  irrigation?: string | boolean;
  water_stress?: string | number;
  timestamp?: string;
}

export interface CitationItem {
  source_organization: string;
  title: string;
  year: number;
  citation: string;
  url: string;
  relevant_evidence: string;
}

export interface RecommendationItem {
  id: string;
  title: string;
  what_to_do: string;
  why_it_works: string;
  variables_involved: string[];
  impacted_metrics: string[];
  time_horizon: string;
  expected_direction: string;
  confidence: string;
  confidence_reason: string;
  scientific_evidence: CitationItem[];
  important_assumptions: string[];
  possible_trade_offs: string[];
}

export interface RetrievedEvidence {
  document_id: string;
  title: string;
  organization: string;
  publication_year: number;
  environmental_domain: string;
  variables: string[];
  excerpt: string;
  similarity_score: number;
  citation: string;
  url: string;
  reliability_score: number;
}

export interface MissingVariableQuestion {
  variable_name: string;
  question_text: string;
  importance: string;
  suggested_options?: string[];
}

export interface ChatResponse {
  conversation_id: string;
  formatted_response: string;
  environmental_assessment: string;
  key_drivers: string[];
  multi_metric_reasoning: string;
  recommendations: RecommendationItem[];
  trade_offs_and_risks: string[];
  evidence_retrieved: RetrievedEvidence[];
  missing_variables_detected: MissingVariableQuestion[];
  updated_environmental_state: Record<string, any>;
  confidence_summary: {
    rating: string;
    score: number;
    input_completeness: number;
    evidence_count: number;
    average_similarity: number;
    reason: string;
  };
  debug_trace?: {
    user_query: string;
    extracted_environmental_variables: Record<string, any>;
    missing_variables: string[];
    retrieved_documents: string[];
    similarity_scores: number[];
    reasoning_factors: string[];
    recommendation_candidates: string[];
    citations_count: number;
  };
}

export interface SystemHealth {
  status: string;
  service: string;
  version: string;
  vector_store_documents: number;
  database_connected: boolean;
  llm_online: boolean;
}

export interface QueryUnderstandingResult {
  query: string;
  detected_variables: string[];
  extracted_state: Record<string, any>;
  missing_variables: string[];
  missing_context_questions: MissingVariableQuestion[];
  location: Record<string, any>;
  ecosystem_context: Record<string, any>;
  time_context: Record<string, any>;
  confidence: number;
  intent: string;
  reasoning_prerequisites: string[];
}

export interface GraphNode {
  id: string;
  metric: string;
  domain: string;
  current_state: string;
  trend: string;
  source: string;
  related_variables: string[];
  explanation: string;
}

export interface GraphEdge {
  source: string;
  target: string;
  relationship_type: string;
  direction: string;
  evidence: string;
  explanation: string;
}

export interface GraphData {
  metadata: {
    total_nodes: number;
    total_edges: number;
    causal_target: string;
    description: string;
  };
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface MetricDelta {
  metric_name: string;
  baseline_value?: any;
  projected_value?: any;
  delta_percentage: number;
  unit: string;
  direction: string;
  scientific_mechanism: string;
}

export interface SimulationResult {
  intervention_type: string;
  status: "modeled" | "unavailable";
  time_horizon_years: number;
  projected_deltas: MetricDelta[];
  ecological_summary: string;
  confidence_level: string;
  scientific_basis: string[];
  limitations: string;
}

export interface SimulationScenarioRequest {
  intervention_type: string;
  intensity: number;
  time_horizon_years: number;
  baseline_state?: EnvironmentalState;
}

export interface StructuredSessionContext {
  conversation_id: string;
  location: Record<string, any>;
  soil: Record<string, any>;
  water: Record<string, any>;
  vegetation: Record<string, any>;
  land_use: Record<string, any>;
  biodiversity: Record<string, any>;
  climate: Record<string, any>;
  conversation_history: Array<{ role: string; content: string }>;
}
