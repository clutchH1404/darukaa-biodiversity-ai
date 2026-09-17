import React from "react";
import { JudgeScenarioPreset } from "../../types/scenario";

interface EarthIntelligenceHeroProps {
  activePreset: JudgeScenarioPreset | null;
  onExplorePreset: (presetId: string) => void;
}

export const EarthIntelligenceHero: React.FC<EarthIntelligenceHeroProps> = ({
  activePreset
}) => {
  return (
    <section className="relative overflow-hidden rounded-xl border border-surface-border bg-gradient-to-br from-surface-container-lowest via-surface-container-low to-surface-container/40 p-6 sm:p-8 backdrop-blur-md">
      {/* Decorative Glow */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-primary/10 rounded-full blur-3xl pointer-events-none -mr-20 -mt-20" />
      <div className="absolute bottom-0 left-1/3 w-80 h-80 bg-secondary/10 rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10 max-w-4xl space-y-4">
        {/* Subtitle Badge */}
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/30 text-primary font-mono text-xs">
          <span className="w-1.5 h-1.5 rounded-full bg-primary animate-ping" />
          <span>DARUKAA.EARTH BIOSYSTEM ARCHITECTURE</span>
        </div>

        {/* Main Title */}
        <h1 className="text-3xl sm:text-4xl lg:text-5xl font-sans font-bold text-slate-100 tracking-tight leading-tight">
          AI Planetary Biosphere <br className="hidden sm:inline" />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary via-emerald-400 to-secondary">
            Intelligence & Command Console
          </span>
        </h1>

        {/* Hackathon Core Objective Paragraph */}
        <p className="text-sm sm:text-base text-slate-300 font-sans leading-relaxed max-w-3xl">
          <strong>Understand ecological risk. Connect environmental variables. Take evidence-backed action.</strong>{" "}
          Operating as an AI Environmental Scientist, Darukaa.Earth fuses multi-metric biophysical reasoning,
          peer-reviewed ecological literature, and dynamic missing context inquiries to protect terrestrial ecosystems.
        </p>

        {/* Current Active Monitoring Area */}
        {activePreset && (
          <div className="pt-2 flex flex-wrap items-center gap-4 text-xs font-mono text-slate-400">
            <div className="flex items-center gap-1.5 bg-surface-container px-3 py-1.5 rounded border border-surface-border">
              <span className="text-slate-500">TARGET:</span>
              <span className="text-slate-200 font-semibold">{activePreset.label}</span>
            </div>
            <div className="flex items-center gap-1.5 bg-surface-container px-3 py-1.5 rounded border border-surface-border">
              <span className="text-slate-500">BIOME:</span>
              <span className="text-secondary font-semibold">{activePreset.biome}</span>
            </div>
            <div className="flex items-center gap-1.5 bg-surface-container px-3 py-1.5 rounded border border-surface-border">
              <span className="text-slate-500">STRESS VECTORS:</span>
              <span className="text-tertiary font-semibold">{activePreset.variables.join(" • ")}</span>
            </div>
          </div>
        )}
      </div>
    </section>
  );
};
