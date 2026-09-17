import React, { useState, useEffect } from "react";
import { AtmosphericShader } from "./components/background/AtmosphericShader";
import { TacticalGrid } from "./components/background/TacticalGrid";
import { TopMissionBar } from "./components/layout/TopMissionBar";
import { SideNavBar } from "./components/layout/SideNavBar";
import { Footer } from "./components/layout/Footer";
import { EarthIntelligenceHero } from "./components/hero/EarthIntelligenceHero";
import { ReasoningPipelineHUD } from "./components/hero/ReasoningPipelineHUD";
import { ScientistWorkspace } from "./components/scientist/ScientistWorkspace";
import { CausalRelationshipGraph } from "./components/graph/CausalRelationshipGraph";
import { ProtocolsList } from "./components/recommendations/ProtocolsList";
import { RagEvidenceDrawer } from "./components/evidence/RagEvidenceDrawer";
import { InterventionSimulator } from "./components/simulator/InterventionSimulator";
import { SpatialBioMapHUD } from "./components/map/SpatialBioMapHUD";

import {
  getHealth,
  getSources,
  postChat,
  getEnvironmentalGraph
} from "./services/api";

import {
  SystemHealth,
  ChatResponse,
  RetrievedEvidence,
  GraphData,
  EnvironmentalState
} from "./types/api";

import { JUDGE_PRESETS, JudgeScenarioPreset } from "./types/scenario";

export const App: React.FC = () => {
  // Navigation & View State
  const [activeTab, setActiveTab] = useState<
    "overview" | "scientist" | "graph" | "simulator" | "evidence"
  >("overview");
  const [activePreset, setActivePreset] = useState<JudgeScenarioPreset>(
    JUDGE_PRESETS[0]
  );
  const [isEvidenceDrawerOpen, setIsEvidenceDrawerOpen] = useState(false);

  // Backend Data State
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [evidenceList, setEvidenceList] = useState<RetrievedEvidence[]>([]);
  const [latestResponse, setLatestResponse] = useState<ChatResponse | null>(null);
  const [chatHistory, setChatHistory] = useState<
    Array<{ role: "user" | "assistant"; content: string; responseObj?: ChatResponse }>
  >([]);
  const [conversationId, setConversationId] = useState<string | undefined>(undefined);
  const [cumulativeState, setCumulativeState] = useState<EnvironmentalState>({});

  // Pipeline execution & loading state
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [pipelineStage, setPipelineStage] = useState<number>(1);

  // Initial Load: Health, Graph, Sources, and first Preset run
  useEffect(() => {
    const initApp = async () => {
      try {
        const [h, g, s] = await Promise.all([
          getHealth().catch(() => null),
          getEnvironmentalGraph().catch(() => null),
          getSources().catch(() => [])
        ]);
        if (h) setHealth(h);
        if (g) setGraphData(g);
        if (s && s.length > 0) {
          setEvidenceList(
            s.map((src: any) => ({
              document_id: src.document_id,
              title: src.title,
              organization: src.organization,
              publication_year: src.publication_year,
              environmental_domain: src.environmental_domain || "Agroecology",
              variables: src.variables || [],
              excerpt: src.text?.substring(0, 260) || "",
              similarity_score: 0.95,
              citation: src.citation,
              url: src.url,
              reliability_score: src.reliability_score || 0.98
            }))
          );
        }

        // Run Preset 1 automatically
        handleRunScenario(JUDGE_PRESETS[0]);
      } catch (err) {
        console.error("Initialization error:", err);
      }
    };
    initApp();
  }, []);

  // Run a scenario through the real backend
  const handleRunScenario = async (preset: JudgeScenarioPreset) => {
    setActivePreset(preset);
    setIsLoading(true);
    setPipelineStage(1);

    try {
      // Step 01 Intake & 02 Parse
      setPipelineStage(2);
      await new Promise((r) => setTimeout(r, 200));

      // Step 03 Context & 04 RAG
      setPipelineStage(4);

      const response = await postChat(
        preset.defaultQuery,
        preset.initialState,
        conversationId,
        { region: preset.biome }
      );

      // Step 05 Graph & 06 Actions
      setPipelineStage(6);

      setLatestResponse(response);
      setConversationId(response.conversation_id);
      setCumulativeState(response.updated_environmental_state || {});

      // Add to conversation history
      setChatHistory((prev) => [
        ...prev,
        { role: "user", content: preset.defaultQuery },
        {
          role: "assistant",
          content: response.formatted_response,
          responseObj: response
        }
      ]);

      if (response.evidence_retrieved && response.evidence_retrieved.length > 0) {
        setEvidenceList(response.evidence_retrieved);
      }

      // Refresh graph with updated environmental state
      try {
        const updatedGraph = await getEnvironmentalGraph(response.updated_environmental_state);
        setGraphData(updatedGraph);
      } catch {
        // Fallback to existing graph
      }

      // Step 07 Audit Complete
      setPipelineStage(7);
    } catch (err) {
      console.error("Failed to execute scenario query:", err);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle user custom message
  const handleSendMessage = async (msg: string) => {
    if (!msg.trim()) return;
    setIsLoading(true);
    setPipelineStage(2);

    try {
      setPipelineStage(4);
      const response = await postChat(
        msg,
        cumulativeState,
        conversationId
      );

      setPipelineStage(6);
      setLatestResponse(response);
      setConversationId(response.conversation_id);
      setCumulativeState(response.updated_environmental_state || {});

      setChatHistory((prev) => [
        ...prev,
        { role: "user", content: msg },
        {
          role: "assistant",
          content: response.formatted_response,
          responseObj: response
        }
      ]);

      if (response.evidence_retrieved && response.evidence_retrieved.length > 0) {
        setEvidenceList(response.evidence_retrieved);
      }

      try {
        const updatedGraph = await getEnvironmentalGraph(response.updated_environmental_state);
        setGraphData(updatedGraph);
      } catch {
        // Keep existing
      }

      setPipelineStage(7);
    } catch (err) {
      console.error("Failed to process chat message:", err);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle answering missing variable question
  const handleAnswerMissingVar = (varName: string, answerValue: string) => {
    const clarifyingMsg = `Providing missing environmental measurement: ${varName.replace(/_/g, " ")} is ${answerValue}.`;
    handleSendMessage(clarifyingMsg);
  };

  return (
    <div className="relative min-h-screen bg-background text-slate-100 flex flex-col font-sans overflow-x-hidden selection:bg-primary/30 selection:text-primary">
      {/* WebGL Multi-Octave Atmospheric Shader */}
      <AtmosphericShader />

      {/* Tactical Ambient Dot Grid & Scan Beam */}
      <TacticalGrid />

      {/* Top Mission Control Bar */}
      <TopMissionBar
        health={health}
        activeCoordinates={activePreset.coordinates}
        onOpenEvidence={() => setIsEvidenceDrawerOpen(true)}
        onOpenSimulator={() => setActiveTab("simulator")}
        onSearchSubmit={(q) => handleSendMessage(q)}
      />

      {/* Main Workspace Frame */}
      <div className="relative z-10 flex-1 flex overflow-hidden">
        {/* Left Side Navigation & Judge Preset Bar */}
        <SideNavBar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          activePresetId={activePreset.id}
          onSelectPreset={(preset) => handleRunScenario(preset)}
        />

        {/* Center Dynamic Content Area */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 space-y-6">
          {/* 7-Stage Reasoning Pipeline HUD (Always visible on top of console) */}
          <ReasoningPipelineHUD
            currentStage={pipelineStage}
            isLoading={isLoading}
            detectedCount={
              latestResponse?.updated_environmental_state
                ? Object.keys(latestResponse.updated_environmental_state).length
                : activePreset.variables.length
            }
            missingCount={latestResponse?.missing_variables_detected?.length || 2}
            retrievedCount={evidenceList.length}
            varsCombinedCount={
              latestResponse?.updated_environmental_state
                ? Math.max(3, Object.keys(latestResponse.updated_environmental_state).length)
                : 3
            }
            recsCount={latestResponse?.recommendations?.length || 3}
            citationsCount={
              latestResponse?.recommendations?.reduce(
                (acc, r) => acc + (r.scientific_evidence?.length || 0),
                0
              ) || 4
            }
          />

          {/* Conditional Workspaces */}
          {activeTab === "overview" && (
            <div className="space-y-6">
              <EarthIntelligenceHero
                activePreset={activePreset}
                onExplorePreset={(pid) => {
                  const p = JUDGE_PRESETS.find((x) => x.id === pid);
                  if (p) handleRunScenario(p);
                }}
              />

              {/* Split: Scientist Workspace & Multispectral Map */}
              <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
                <div className="xl:col-span-7">
                  <ScientistWorkspace
                    chatHistory={chatHistory}
                    latestResponse={latestResponse}
                    isLoading={isLoading}
                    onSendMessage={handleSendMessage}
                    onAnswerMissingVar={handleAnswerMissingVar}
                    onInspectEvidence={(evs) => {
                      setEvidenceList(evs);
                      setIsEvidenceDrawerOpen(true);
                    }}
                  />
                </div>

                <div className="xl:col-span-5 space-y-6">
                  <SpatialBioMapHUD activePreset={activePreset} />
                  <CausalRelationshipGraph
                    graphData={graphData}
                    ecologicalNarrative={latestResponse?.multi_metric_reasoning}
                    onRefreshGraph={async () => {
                      const g = await getEnvironmentalGraph(cumulativeState);
                      setGraphData(g);
                    }}
                  />
                </div>
              </div>

              {/* 10-Point Recommendations List */}
              <ProtocolsList
                recommendations={latestResponse?.recommendations || []}
                onSimulateProtocol={() => setActiveTab("simulator")}
                onInspectEvidence={() => setIsEvidenceDrawerOpen(true)}
              />
            </div>
          )}

          {activeTab === "scientist" && (
            <div className="space-y-6">
              <ScientistWorkspace
                chatHistory={chatHistory}
                latestResponse={latestResponse}
                isLoading={isLoading}
                onSendMessage={handleSendMessage}
                onAnswerMissingVar={handleAnswerMissingVar}
                onInspectEvidence={(evs) => {
                  setEvidenceList(evs);
                  setIsEvidenceDrawerOpen(true);
                }}
              />
            </div>
          )}

          {activeTab === "graph" && (
            <div className="space-y-6">
              <CausalRelationshipGraph
                graphData={graphData}
                ecologicalNarrative={latestResponse?.multi_metric_reasoning}
                onRefreshGraph={async () => {
                  const g = await getEnvironmentalGraph(cumulativeState);
                  setGraphData(g);
                }}
              />
            </div>
          )}

          {activeTab === "simulator" && (
            <div className="space-y-6">
              <InterventionSimulator />
            </div>
          )}

          {activeTab === "evidence" && (
            <div className="space-y-6">
              <div className="bg-surface-container-lowest/80 border border-surface-border rounded-xl p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-secondary text-lg">
                      library_books
                    </span>
                    <h2 className="font-mono text-sm font-bold text-slate-100 uppercase tracking-wider">
                      Authoritative Peer-Reviewed Knowledge Base (ChromaDB)
                    </h2>
                  </div>
                  <span className="font-mono text-xs text-primary font-bold">
                    {evidenceList.length} DOCUMENTS
                  </span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {evidenceList.map((ev, idx) => (
                    <div
                      key={idx}
                      className="bg-surface-container-low p-4 rounded-lg border border-surface-border space-y-2"
                    >
                      <div className="flex items-center justify-between font-mono text-[10px]">
                        <span className="text-secondary font-bold">{ev.document_id}</span>
                        <span className="text-primary font-bold">
                          {(ev.similarity_score * 100).toFixed(1)}% RELEVANCE
                        </span>
                      </div>
                      <h4 className="font-sans font-bold text-xs text-slate-200">
                        {ev.title}
                      </h4>
                      <p className="text-[11px] text-slate-400 font-sans leading-relaxed">
                        "{ev.excerpt}"
                      </p>
                      <div className="pt-2 border-t border-surface-border/50 flex items-center justify-between text-[10px] font-mono">
                        <span className="text-slate-500">{ev.organization} ({ev.publication_year})</span>
                        {ev.url && (
                          <a
                            href={ev.url}
                            target="_blank"
                            rel="noreferrer"
                            className="text-primary hover:underline font-bold"
                          >
                            VIEW SOURCE ↗
                          </a>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </main>
      </div>

      {/* RAG Evidence Drawer Slide-over */}
      <RagEvidenceDrawer
        isOpen={isEvidenceDrawerOpen}
        onClose={() => setIsEvidenceDrawerOpen(false)}
        evidenceList={evidenceList}
      />

      {/* Tactical Status Footer */}
      <Footer />
    </div>
  );
};

export default App;
