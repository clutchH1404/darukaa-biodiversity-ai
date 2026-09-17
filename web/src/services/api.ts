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

const getApiBase = (): string => {
  const envUrl = import.meta.env.VITE_API_URL || import.meta.env.VITE_API_BASE_URL;
  if (envUrl && typeof envUrl === "string" && envUrl.trim() !== "") {
    return envUrl.trim().replace(/\/+$/, "");
  }
  return "";
};

const API_BASE = getApiBase();

async function handleFetch(url: string, options?: RequestInit): Promise<Response> {
  try {
    const res = await fetch(url, options);
    return res;
  } catch (err: any) {
    console.error(`[Darukaa.Earth API Network Error] ${url}:`, err);
    throw new Error(
      `Network connection to Darukaa.Earth backend (${API_BASE || "local server"}) failed. If hosted on a cloud tier such as Render, the instance may be spinning up from sleep mode (~30s cold start).`
    );
  }
}

export async function getHealth(): Promise<SystemHealth> {
  const res = await handleFetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error(`Health check failed: ${res.statusText}`);
  return res.json();
}

export async function getSources(): Promise<any[]> {
  const res = await handleFetch(`${API_BASE}/sources`);
  if (!res.ok) throw new Error(`Fetch sources failed: ${res.statusText}`);
  return res.json();
}

export async function retrieveEvidence(
  query: string,
  environmental_variables?: string[],
  geographic_context?: Record<string, any>,
  top_k: number = 5
): Promise<RetrievedEvidence[]> {
  const res = await handleFetch(`${API_BASE}/retrieve`, {
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
  const res = await handleFetch(`${API_BASE}/understand`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query })
  });
  if (!res.ok) throw new Error(`Query understanding failed: ${res.statusText}`);
  return res.json();
}

export async function getEnvironmentalGraph(state?: EnvironmentalState): Promise<GraphData> {
  if (state && Object.keys(state).length > 0) {
    const res = await handleFetch(`${API_BASE}/graph`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ environmental_state: state })
    });
    if (!res.ok) throw new Error(`Graph generation failed: ${res.statusText}`);
    return res.json();
  } else {
    const res = await handleFetch(`${API_BASE}/graph`);
    if (!res.ok) throw new Error(`Graph fetch failed: ${res.statusText}`);
    return res.json();
  }
}

export async function simulateIntervention(
  req: SimulationScenarioRequest
): Promise<SimulationResult> {
  const res = await handleFetch(`${API_BASE}/simulate`, {
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
  const res = await handleFetch(`${API_BASE}/chat`, {
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
  const res = await handleFetch(`${API_BASE}/session/${conversation_id}/context`);
  if (!res.ok) throw new Error(`Session context fetch failed: ${res.statusText}`);
  return res.json();
}
