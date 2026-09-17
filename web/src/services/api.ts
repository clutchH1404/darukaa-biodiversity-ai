import {
  EnvironmentalState,
  RetrievedEvidence,
  RecommendationItem,
  ChatResponse,
  SystemHealth,
  QueryUnderstandingResult,
  GraphData,
  SimulationScenarioRequest,
  SimulationResult,
  StructuredSessionContext
} from "../types/api";

const API_BASE = ""; // Handled by Vite dev proxy to http://127.0.0.1:8000

export async function getHealth(): Promise<SystemHealth> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error(`Health check failed: ${res.statusText}`);
  return res.json();
}

export async function getSources(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/sources`);
  if (!res.ok) throw new Error(`Fetch sources failed: ${res.statusText}`);
  return res.json();
}

export async function retrieveEvidence(
  query: string,
  environmental_variables?: string[],
  geographic_context?: Record<string, any>,
  top_k: number = 5
): Promise<RetrievedEvidence[]> {
  const res = await fetch(`${API_BASE}/retrieve`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      environmental_variables,
      geographic_context,
      top_k
    })
  });
  if (!res.ok) throw new Error(`RAG retrieval failed: ${res.statusText}`);
  return res.json();
}

export async function understandQuery(query: string): Promise<QueryUnderstandingResult> {
  const res = await fetch(`${API_BASE}/understand`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query })
  });
  if (!res.ok) throw new Error(`Query understanding failed: ${res.statusText}`);
  return res.json();
}

export async function getEnvironmentalGraph(state?: EnvironmentalState): Promise<GraphData> {
  if (state && Object.keys(state).length > 0) {
    const res = await fetch(`${API_BASE}/graph`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ environmental_state: state })
    });
    if (!res.ok) throw new Error(`Graph generation failed: ${res.statusText}`);
    return res.json();
  } else {
    const res = await fetch(`${API_BASE}/graph`);
    if (!res.ok) throw new Error(`Graph fetch failed: ${res.statusText}`);
    return res.json();
  }
}

export async function simulateIntervention(
  req: SimulationScenarioRequest
): Promise<SimulationResult> {
  const res = await fetch(`${API_BASE}/simulate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req)
  });
  if (!res.ok) throw new Error(`Simulation failed: ${res.statusText}`);
  return res.json();
}

export async function postChat(
  message: string,
  state?: EnvironmentalState,
  conversation_id?: string,
  geographic_context?: Record<string, any>
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      environmental_state: state,
      conversation_id,
      geographic_context
    })
  });
  if (!res.ok) throw new Error(`Chat API error: ${res.statusText}`);
  return res.json();
}

export async function getSessionContext(conversation_id: string): Promise<StructuredSessionContext> {
  const res = await fetch(`${API_BASE}/session/${conversation_id}/context`);
  if (!res.ok) throw new Error(`Session context fetch failed: ${res.statusText}`);
  return res.json();
}
