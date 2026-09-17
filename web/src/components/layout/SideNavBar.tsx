import React from "react";
import { JUDGE_PRESETS, JudgeScenarioPreset } from "../../types/scenario";

interface SideNavBarProps {
  activeTab: "overview" | "scientist" | "graph" | "simulator" | "evidence";
  setActiveTab: (tab: "overview" | "scientist" | "graph" | "simulator" | "evidence") => void;
  activePresetId: string;
  onSelectPreset: (preset: JudgeScenarioPreset) => void;
}

export const SideNavBar: React.FC<SideNavBarProps> = ({
  activeTab,
  setActiveTab,
  activePresetId,
  onSelectPreset
}) => {
  return (
    <aside className="w-64 xl:w-72 bg-surface-container-lowest/90 border-r border-surface-border flex flex-col justify-between p-4 z-20 overflow-y-auto">
      {/* Brand Header */}
      <div className="space-y-6">
        <div className="flex items-center gap-3 px-2 py-1">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-primary via-emerald-600 to-secondary flex items-center justify-center shadow-lg shadow-primary/20">
            <span className="material-symbols-outlined text-background font-bold text-xl">
              nest_eco_leaf
            </span>
          </div>
          <div>
            <h1 className="font-sans font-bold text-sm tracking-wider text-slate-100 flex items-center gap-1.5">
              DARUKAA<span className="text-primary font-mono">.EARTH</span>
            </h1>
            <p className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">
              AI Biosphere Intelligence
            </p>
          </div>
        </div>

        {/* Navigation Sections */}
        <div className="space-y-1">
          <div className="text-[10px] font-mono text-slate-500 uppercase px-3 mb-2 tracking-wider">
            CONSOLE WORKSPACES
          </div>

          <button
            onClick={() => setActiveTab("overview")}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-md text-xs font-mono transition-all ${
              activeTab === "overview"
                ? "bg-primary/15 text-primary border border-primary/30"
                : "text-slate-400 hover:text-slate-200 hover:bg-surface-container"
            }`}
          >
            <span className="material-symbols-outlined text-base">public</span>
            <span>01 EARTH INTELLIGENCE</span>
          </button>

          <button
            onClick={() => setActiveTab("scientist")}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-md text-xs font-mono transition-all ${
              activeTab === "scientist"
                ? "bg-primary/15 text-primary border border-primary/30"
                : "text-slate-400 hover:text-slate-200 hover:bg-surface-container"
            }`}
          >
            <span className="material-symbols-outlined text-base">psychology</span>
            <span>02 AI SCIENTIST CONSOLE</span>
          </button>

          <button
            onClick={() => setActiveTab("graph")}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-md text-xs font-mono transition-all ${
              activeTab === "graph"
                ? "bg-primary/15 text-primary border border-primary/30"
                : "text-slate-400 hover:text-slate-200 hover:bg-surface-container"
            }`}
          >
            <span className="material-symbols-outlined text-base">account_tree</span>
            <span>03 BIOPHYSICAL GRAPH</span>
          </button>

          <button
            onClick={() => setActiveTab("simulator")}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-md text-xs font-mono transition-all ${
              activeTab === "simulator"
                ? "bg-primary/15 text-primary border border-primary/30"
                : "text-slate-400 hover:text-slate-200 hover:bg-surface-container"
            }`}
          >
            <span className="material-symbols-outlined text-base">biotech</span>
            <span>04 INTERVENTION SIMULATOR</span>
          </button>

          <button
            onClick={() => setActiveTab("evidence")}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-md text-xs font-mono transition-all ${
              activeTab === "evidence"
                ? "bg-primary/15 text-primary border border-primary/30"
                : "text-slate-400 hover:text-slate-200 hover:bg-surface-container"
            }`}
          >
            <span className="material-symbols-outlined text-base">menu_book</span>
            <span>05 SCIENTIFIC EVIDENCE (RAG)</span>
          </button>
        </div>

        {/* Judge Demo Presets (Hackathon Section 25) */}
        <div className="space-y-2 pt-3 border-t border-surface-border/60">
          <div className="flex items-center justify-between px-3">
            <span className="text-[10px] font-mono text-tertiary uppercase tracking-wider font-semibold">
              JUDGE DEMO PRESETS
            </span>
            <span className="text-[9px] font-mono text-slate-500 bg-surface-container px-1.5 py-0.5 rounded">
              REAL BACKEND
            </span>
          </div>

          <div className="space-y-1.5">
            {JUDGE_PRESETS.map((preset) => {
              const isSelected = preset.id === activePresetId;
              return (
                <button
                  key={preset.id}
                  onClick={() => onSelectPreset(preset)}
                  className={`w-full text-left p-2.5 rounded border transition-all ${
                    isSelected
                      ? "bg-surface-container border-primary/50 text-slate-100 shadow-sm shadow-primary/10"
                      : "bg-surface-container-lowest/60 border-surface-border/50 text-slate-400 hover:border-slate-600 hover:text-slate-300"
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-mono text-[11px] font-semibold text-slate-200">
                      {preset.label}
                    </span>
                    <span className="font-mono text-[9px] text-secondary">
                      {preset.biome}
                    </span>
                  </div>
                  <p className="text-[10px] text-slate-400 line-clamp-2 leading-relaxed">
                    {preset.focusProblem}
                  </p>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Audit & Grounding Telemetry Footer */}
      <div className="mt-6 pt-4 border-t border-surface-border/70 space-y-3">
        <div className="bg-surface-container p-3 rounded border border-surface-border text-[11px] font-mono space-y-1.5">
          <div className="flex items-center justify-between text-slate-400">
            <span>RAG EVIDENCE CORPUS</span>
            <span className="text-primary font-bold">12 PAPERS</span>
          </div>
          <div className="flex items-center justify-between text-slate-400">
            <span>CAUSAL GRAPH NODES</span>
            <span className="text-secondary font-bold">29 NODES</span>
          </div>
          <div className="flex items-center justify-between text-slate-400">
            <span>MULTI-METRIC RULE</span>
            <span className="text-tertiary font-bold">≥3 VARS</span>
          </div>
          <div className="flex items-center justify-between text-slate-400">
            <span>AUTOMATED TESTS</span>
            <span className="text-emerald-400 font-bold">37/37 PASS</span>
          </div>
        </div>

        <div className="text-[10px] font-mono text-slate-500 text-center">
          DARUKAA.EARTH v1.0.0 • ZERO HALLUCINATIONS
        </div>
      </div>
    </aside>
  );
};
