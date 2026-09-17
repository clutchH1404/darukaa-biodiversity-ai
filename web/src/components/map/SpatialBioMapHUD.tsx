import React, { useState } from "react";
import { JudgeScenarioPreset } from "../../types/scenario";

interface SpatialBioMapHUDProps {
  activePreset: JudgeScenarioPreset | null;
}

export const SpatialBioMapHUD: React.FC<SpatialBioMapHUDProps> = ({
  activePreset
}) => {
  const [activeLayer, setActiveLayer] = useState<string>("vegetation");

  const LAYERS = [
    { id: "vegetation", label: "NDVI CANOPY", available: true },
    { id: "soil", label: "SOIL SOC 0-30CM", available: true },
    { id: "hydrology", label: "HYDROLOGICAL STRESS", available: true },
    { id: "corridors", label: "CONNECTIVITY CORRIDORS", available: true },
    { id: "hyper_sar", label: "HYPERSPECTRAL SAR", available: false }
  ];

  return (
    <div className="bg-surface-container-lowest/80 border border-surface-border rounded-xl backdrop-blur-md p-4 sm:p-6 space-y-4">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-surface-border/60 pb-3">
        <div>
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-secondary text-base">
              satellite_alt
            </span>
            <h2 className="font-mono text-sm font-bold text-slate-100 uppercase tracking-wider">
              Multispectral Sentinel-2 Earth Observation HUD
            </h2>
          </div>
          <p className="text-xs text-slate-400 font-sans mt-0.5">
            Spatial context grounding biophysical observations with regional landscape telemetry.
          </p>
        </div>

        <div className="flex items-center gap-2 font-mono text-[10px]">
          <span className="px-2 py-0.5 rounded bg-tertiary/20 text-tertiary border border-tertiary/40 font-bold">
            DEMO MODE (CALIBRATED OBSERVATION)
          </span>
          <span className="text-slate-500">•</span>
          <span className="text-slate-400">
            {activePreset ? activePreset.coordinates : "03°08'40\"S 60°01'30\"W"}
          </span>
        </div>
      </div>

      {/* Layer Selector Chips */}
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-[10px] font-mono text-slate-500 uppercase mr-1">
          SPECTRAL LAYERS:
        </span>
        {LAYERS.map((layer) => (
          <button
            key={layer.id}
            onClick={() => layer.available && setActiveLayer(layer.id)}
            disabled={!layer.available}
            className={`px-2.5 py-1 rounded text-[10px] font-mono transition-all flex items-center gap-1.5 ${
              !layer.available
                ? "bg-surface-container-low/40 text-slate-600 border border-surface-border/30 cursor-not-allowed"
                : activeLayer === layer.id
                ? "bg-secondary/20 text-secondary border border-secondary/40 font-bold"
                : "bg-surface-container text-slate-400 hover:text-slate-200 border border-surface-border"
            }`}
          >
            <span>{layer.label}</span>
            {!layer.available && (
              <span className="text-[8px] text-tertiary font-bold">[UNAVAILABLE]</span>
            )}
          </button>
        ))}
      </div>

      {/* Synthetic Satellite Viewport with HUD Crosshairs */}
      <div className="relative h-64 sm:h-80 rounded-lg overflow-hidden border border-surface-border bg-gradient-to-br from-slate-950 via-slate-900 to-emerald-950/40 flex items-center justify-center">
        {/* Synthetic Multispectral Texture */}
        <div
          className="absolute inset-0 opacity-25"
          style={{
            backgroundImage: `radial-gradient(ellipse at 40% 60%, rgba(78, 222, 163, 0.4) 0%, transparent 60%),
                              radial-gradient(ellipse at 70% 30%, rgba(76, 215, 246, 0.3) 0%, transparent 50%),
                              radial-gradient(ellipse at 20% 20%, rgba(255, 185, 95, 0.2) 0%, transparent 40%)`
          }}
        />

        {/* Tactical Crosshair Overlay */}
        <div className="absolute inset-0 pointer-events-none flex items-center justify-center">
          <div className="w-48 h-48 border border-secondary/30 rounded-full flex items-center justify-center">
            <div className="w-24 h-24 border border-secondary/50 rounded-full flex items-center justify-center">
              <div className="w-2 h-2 bg-primary rounded-full animate-ping" />
            </div>
          </div>
          {/* Cross lines */}
          <div className="absolute w-full h-[1px] bg-secondary/15" />
          <div className="absolute h-full w-[1px] bg-secondary/15" />
        </div>

        {/* HUD Data Overlay Boxes */}
        <div className="absolute top-3 left-3 bg-surface-container-lowest/80 border border-surface-border p-2 rounded text-[10px] font-mono space-y-0.5 text-slate-300">
          <div>
            <span className="text-slate-500">TARGET:</span>{" "}
            <span className="text-slate-100 font-bold">
              {activePreset ? activePreset.label : "Amazon Sector 04B"}
            </span>
          </div>
          <div>
            <span className="text-slate-500">BIOME:</span>{" "}
            <span className="text-secondary">{activePreset ? activePreset.biome : "Rainforest"}</span>
          </div>
          <div>
            <span className="text-slate-500">RES:</span> 10M SENTINEL-2 L2A
          </div>
        </div>

        <div className="absolute bottom-3 right-3 bg-surface-container-lowest/80 border border-surface-border p-2 rounded text-[10px] font-mono space-y-0.5 text-slate-300 text-right">
          <div>
            <span className="text-slate-500">ACTIVE BAND:</span>{" "}
            <span className="text-primary font-bold">{activeLayer.toUpperCase()}</span>
          </div>
          <div className="text-tertiary">
            CORRIDOR DEFICIT DETECTED
          </div>
        </div>
      </div>
    </div>
  );
};
