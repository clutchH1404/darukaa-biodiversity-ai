import React from "react";

interface ReasoningPipelineHUDProps {
  currentStage: number; // 1 to 7
  isLoading: boolean;
  detectedCount: number;
  missingCount: number;
  retrievedCount: number;
  varsCombinedCount: number;
  recsCount: number;
  citationsCount: number;
}

export const ReasoningPipelineHUD: React.FC<ReasoningPipelineHUDProps> = ({
  currentStage,
  isLoading,
  detectedCount,
  missingCount,
  retrievedCount,
  varsCombinedCount,
  recsCount,
  citationsCount
}) => {
  const STAGES = [
    { num: "01", label: "INTAKE", desc: "User Observation Intake", statusInfo: "Active Input" },
    { num: "02", label: "PARSE", desc: "Variable Detection (20+)", statusInfo: `${detectedCount} Extracted` },
    { num: "03", label: "CONTEXT", desc: "Missing Critical Context", statusInfo: `${missingCount} Missing` },
    { num: "04", label: "RAG", desc: "ChromaDB Vector Retrieval", statusInfo: `${retrievedCount} Sources` },
    { num: "05", label: "GRAPH", desc: "Multi-Metric Causal Synthesis", statusInfo: `${varsCombinedCount} Coupled Vars` },
    { num: "06", label: "ACTIONS", desc: "10-Point Recommendations", statusInfo: `${recsCount} Generated` },
    { num: "07", label: "AUDIT", desc: "Evidence & DOI Verification", statusInfo: `${citationsCount} Citations` }
  ];

  return (
    <div className="w-full bg-surface-container-lowest/80 border border-surface-border rounded-lg p-3 sm:p-4 backdrop-blur-sm">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-primary text-sm">
            timeline
          </span>
          <span className="font-mono text-xs font-semibold text-slate-200 tracking-wider uppercase">
            AI Environmental Reasoning Pipeline
          </span>
          <span className="text-[10px] font-mono text-slate-400 bg-surface-container px-2 py-0.5 rounded border border-surface-border/60">
            AUDITABLE SCIENTIFIC TRACE
          </span>
        </div>

        {isLoading && (
          <div className="flex items-center gap-2 font-mono text-[11px] text-secondary">
            <span className="w-2 h-2 rounded-full bg-secondary animate-ping" />
            <span>EXECUTING STAGE 0{currentStage}...</span>
          </div>
        )}
      </div>

      {/* Grid of 7 Stages */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2">
        {STAGES.map((s, idx) => {
          const stageIndex = idx + 1;
          const isDone = stageIndex < currentStage;
          const isCurrent = stageIndex === currentStage;
          const isPending = stageIndex > currentStage;

          let borderClass = "border-surface-border/60 bg-surface-container-low/40";
          let textClass = "text-slate-500";
          let badgeColor = "bg-surface-container text-slate-500";

          if (isDone) {
            borderClass = "border-primary/40 bg-primary/5";
            textClass = "text-slate-300";
            badgeColor = "bg-primary/20 text-primary border border-primary/30";
          } else if (isCurrent) {
            borderClass = "border-secondary bg-secondary/10 shadow-sm shadow-secondary/20";
            textClass = "text-slate-100";
            badgeColor = "bg-secondary text-background font-bold";
          }

          return (
            <div
              key={s.num}
              className={`p-2.5 rounded border transition-all ${borderClass}`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <span className="font-mono text-[10px] font-bold text-slate-400">
                  {s.num}
                </span>
                <span className={`font-mono text-[9px] px-1.5 py-0.5 rounded ${badgeColor}`}>
                  {isDone ? "✓ DONE" : isCurrent ? (isLoading ? "RUNNING" : "ACTIVE") : "PENDING"}
                </span>
              </div>

              <div className={`font-mono text-[11px] font-bold uppercase mb-0.5 ${textClass}`}>
                {s.label}
              </div>

              <div className="text-[10px] text-slate-400 line-clamp-1 mb-1">
                {s.desc}
              </div>

              <div className="font-mono text-[9px] text-secondary font-medium">
                {s.statusInfo}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
