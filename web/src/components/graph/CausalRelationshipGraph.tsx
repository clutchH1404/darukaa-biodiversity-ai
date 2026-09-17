import React, { useState } from "react";
import { GraphData, GraphNode } from "../../types/api";

interface CausalRelationshipGraphProps {
  graphData: GraphData | null;
  ecologicalNarrative?: string;
  onRefreshGraph: () => void;
}

// Preset visual coordinate layout for 9 major key biophysical domains
const KEY_NODE_POSITIONS: Record<string, { x: number; y: number; label: string }> = {
  soil_organic_carbon: { x: 140, y: 150, label: "Soil Organic Carbon" },
  soil_structure: { x: 260, y: 190, label: "Soil Aggregate Structure" },
  water_retention: { x: 380, y: 160, label: "Water Holding Capacity" },
  soil_moisture: { x: 420, y: 250, label: "Root Zone Moisture" },
  rainfall: { x: 200, y: 60, label: "Rainfall Input" },
  water_availability: { x: 340, y: 80, label: "Hydrological Balance" },
  water_stress: { x: 500, y: 110, label: "Plant Hydraulic Stress" },
  monoculture: { x: 680, y: 80, label: "Monoculture Uniformity" },
  habitat_fragmentation: { x: 780, y: 170, label: "Habitat Fragmentation" },
  species_movement: { x: 720, y: 280, label: "Dispersal Corridors" },
  plant_resilience: { x: 520, y: 240, label: "Vegetative Resilience" },
  habitat_quality: { x: 580, y: 350, label: "Habitat Niche Quality" },
  pollinator_abundance: { x: 300, y: 380, label: "Pollinator Abundance" },
  pesticide_intensity: { x: 160, y: 340, label: "Pesticide Application" },
  biodiversity: { x: 480, y: 450, label: "BIOSPHERE EQUILIBRIUM" }
};

export const CausalRelationshipGraph: React.FC<CausalRelationshipGraphProps> = ({
  graphData,
  ecologicalNarrative,
  onRefreshGraph
}) => {
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);

  const nodes = graphData?.nodes || [];
  const edges = graphData?.edges || [];

  // Filter edges to those between positioned nodes for clean rendering
  const visibleEdges = edges.filter(
    (e) => KEY_NODE_POSITIONS[e.source] && KEY_NODE_POSITIONS[e.target]
  );

  return (
    <div className="bg-surface-container-lowest/80 border border-surface-border rounded-xl backdrop-blur-md p-4 sm:p-6 space-y-4">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-surface-border/60 pb-3">
        <div>
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-primary text-base">
              hub
            </span>
            <h2 className="font-mono text-sm font-bold text-slate-100 uppercase tracking-wider">
              Biophysical Causal Relationship Network
            </h2>
          </div>
          <p className="text-xs text-slate-400 font-sans mt-0.5">
            Directed biophysical pathways mapping stressors, feedback loops, and ecological equilibrium.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-[10px] font-mono text-slate-400 bg-surface-container px-2.5 py-1 rounded border border-surface-border">
            {nodes.length} NODES • {edges.length} DIRECTED CAUSAL EDGES
          </span>
          <button
            onClick={onRefreshGraph}
            className="p-1.5 rounded bg-surface-container hover:bg-surface-container-high border border-surface-border text-slate-300 hover:text-primary transition-colors"
            title="Refresh network"
          >
            <span className="material-symbols-outlined text-sm">refresh</span>
          </button>
        </div>
      </div>

      {/* Synthesis Narrative Banner */}
      {ecologicalNarrative && (
        <div className="p-3.5 rounded bg-surface-container/60 border border-surface-border text-xs text-slate-300 leading-relaxed font-sans flex items-start gap-2.5">
          <span className="material-symbols-outlined text-secondary text-base shrink-0 mt-0.5">
            insights
          </span>
          <div>
            <strong className="text-secondary font-mono text-[10px] uppercase block mb-0.5">
              SYNTHESIZED MULTI-METRIC CASSETTE
            </strong>
            {ecologicalNarrative}
          </div>
        </div>
      )}

      {/* Main Interactive Graph & Inspector Split */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* SVG Graph Viewport (2 Cols on lg) */}
        <div className="lg:col-span-2 relative bg-surface-container-low/40 rounded-lg border border-surface-border/80 overflow-hidden flex items-center justify-center p-2 min-h-[480px]">
          <svg
            viewBox="0 0 960 520"
            className="w-full h-full max-h-[520px] select-none"
          >
            <defs>
              <marker
                id="arrow-pos"
                viewBox="0 0 10 10"
                refX="22"
                refY="5"
                markerWidth="6"
                markerHeight="6"
                orient="auto-start-reverse"
              >
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#4edea3" />
              </marker>
              <marker
                id="arrow-neg"
                viewBox="0 0 10 10"
                refX="22"
                refY="5"
                markerWidth="6"
                markerHeight="6"
                orient="auto-start-reverse"
              >
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#ffb95f" />
              </marker>
            </defs>

            {/* Edges */}
            {visibleEdges.map((e, idx) => {
              const srcPos = KEY_NODE_POSITIONS[e.source];
              const tgtPos = KEY_NODE_POSITIONS[e.target];
              const isPositive = e.direction.includes("+1");

              return (
                <path
                  key={idx}
                  d={`M ${srcPos.x} ${srcPos.y} Q ${(srcPos.x + tgtPos.x) / 2} ${(srcPos.y + tgtPos.y) / 2 - 20} ${tgtPos.x} ${tgtPos.y}`}
                  fill="none"
                  stroke={isPositive ? "#4edea3" : "#ffb95f"}
                  strokeWidth="1.5"
                  strokeOpacity="0.45"
                  strokeDasharray={isPositive ? "none" : "3,3"}
                  markerEnd={isPositive ? "url(#arrow-pos)" : "url(#arrow-neg)"}
                  className="transition-all hover:stroke-opacity-100 hover:stroke-width-2 cursor-pointer"
                />
              );
            })}

            {/* Positioned Nodes */}
            {Object.entries(KEY_NODE_POSITIONS).map(([nodeId, pos]) => {
              const nodeData = nodes.find((n) => n.id === nodeId);
              const isSelected = selectedNode?.id === nodeId;
              const isCentral = nodeId === "biodiversity";
              const isStressed = nodeData?.trend?.includes("depleted") || nodeData?.trend?.includes("stressed");

              let nodeColor = "#4cd7f6"; // default cyan
              if (isCentral) nodeColor = "#4edea3"; // emerald
              else if (isStressed) nodeColor = "#ffb95f"; // amber stress

              return (
                <g
                  key={nodeId}
                  transform={`translate(${pos.x}, ${pos.y})`}
                  onClick={() =>
                    setSelectedNode(
                      nodeData || {
                        id: nodeId,
                        metric: pos.label,
                        domain: "biophysical",
                        current_state: "unmeasured",
                        trend: "stable",
                        source: "Darukaa.Earth Domain Ontology",
                        related_variables: [],
                        explanation: "Biophysical parameter governing ecosystem equilibrium."
                      }
                    )
                  }
                  className="cursor-pointer group"
                >
                  {/* Glow circle */}
                  <circle
                    r={isCentral ? 22 : 14}
                    fill={nodeColor}
                    fillOpacity={isSelected ? "0.35" : "0.15"}
                    stroke={nodeColor}
                    strokeWidth={isSelected ? "2.5" : "1.5"}
                    className="transition-all group-hover:scale-125"
                  />
                  {/* Inner dot */}
                  <circle
                    r={isCentral ? 6 : 4}
                    fill={nodeColor}
                  />
                  {/* Label */}
                  <text
                    y={isCentral ? 34 : 24}
                    textAnchor="middle"
                    fill={isSelected ? "#ffffff" : "#cbd5e1"}
                    fontSize={isCentral ? "11" : "9"}
                    fontFamily="monospace"
                    className="pointer-events-none select-none font-semibold"
                  >
                    {pos.label}
                  </text>
                </g>
              );
            })}
          </svg>

          <div className="absolute bottom-2 left-2 text-[9px] font-mono text-slate-500 bg-surface-container-lowest/80 px-2 py-1 rounded border border-surface-border">
            CLICK ANY NODE TO INSPECT BIOPHYSICAL PROVENANCE
          </div>
        </div>

        {/* Node Inspector Panel (1 Col on lg) */}
        <div className="bg-surface-container-low/80 rounded-lg border border-surface-border p-4 space-y-3">
          <div className="flex items-center justify-between border-b border-surface-border/60 pb-2">
            <span className="font-mono text-[11px] font-bold text-slate-200 uppercase">
              NODE INSPECTOR
            </span>
            {selectedNode && (
              <span className="font-mono text-[9px] px-2 py-0.5 rounded bg-primary/20 text-primary border border-primary/30">
                ACTIVE
              </span>
            )}
          </div>

          {selectedNode ? (
            <div className="space-y-3 text-xs font-sans">
              <div>
                <span className="text-[10px] font-mono text-slate-500 uppercase block">
                  METRIC IDENTIFIER
                </span>
                <div className="font-mono font-bold text-sm text-slate-100">
                  {selectedNode.metric}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2 text-[11px]">
                <div className="bg-surface-container p-2 rounded border border-surface-border">
                  <span className="text-[9px] font-mono text-slate-500 uppercase block">
                    CURRENT STATE
                  </span>
                  <span className="font-mono text-primary font-bold">
                    {selectedNode.current_state}
                  </span>
                </div>
                <div className="bg-surface-container p-2 rounded border border-surface-border">
                  <span className="text-[9px] font-mono text-slate-500 uppercase block">
                    TREND VECTOR
                  </span>
                  <span
                    className={`font-mono font-bold ${
                      selectedNode.trend?.includes("stressed") ||
                      selectedNode.trend?.includes("depleted")
                        ? "text-tertiary"
                        : "text-slate-300"
                    }`}
                  >
                    {selectedNode.trend}
                  </span>
                </div>
              </div>

              <div>
                <span className="text-[10px] font-mono text-slate-500 uppercase block mb-1">
                  BIOPHYSICAL ROLE
                </span>
                <p className="text-slate-300 leading-relaxed text-[11px]">
                  {selectedNode.explanation}
                </p>
              </div>

              <div>
                <span className="text-[10px] font-mono text-slate-500 uppercase block mb-1">
                  SCIENTIFIC LITERATURE PROVENANCE
                </span>
                <div className="bg-surface-container p-2 rounded border border-surface-border text-[10px] font-mono text-secondary">
                  {selectedNode.source}
                </div>
              </div>

              {selectedNode.related_variables && selectedNode.related_variables.length > 0 && (
                <div>
                  <span className="text-[10px] font-mono text-slate-500 uppercase block mb-1">
                    CONNECTED ENVIRONMENTAL METRICS
                  </span>
                  <div className="flex flex-wrap gap-1">
                    {selectedNode.related_variables.map((rv) => (
                      <span
                        key={rv}
                        className="px-1.5 py-0.5 rounded bg-surface-container border border-surface-border text-[10px] font-mono text-slate-300"
                      >
                        {rv.replace(/_/g, " ")}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="h-48 flex flex-col items-center justify-center text-center text-slate-500 text-xs">
              <span className="material-symbols-outlined text-2xl mb-1 text-slate-600">
                touch_app
              </span>
              <span>Click any node in the causal diagram to inspect biophysical properties and source literature.</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
