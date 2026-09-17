import React, { useState, useEffect } from "react";
import { SystemHealth } from "../../types/api";

interface TopMissionBarProps {
  health: SystemHealth | null;
  activeCoordinates?: string;
  onOpenEvidence: () => void;
  onOpenSimulator: () => void;
  onSearchSubmit: (query: string) => void;
}

export const TopMissionBar: React.FC<TopMissionBarProps> = ({
  health,
  activeCoordinates = "03°08'40\"S 60°01'30\"W — MANAUS GRD",
  onOpenEvidence,
  onOpenSimulator,
  onSearchSubmit
}) => {
  const [timeUtc, setTimeUtc] = useState<string>("");
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      const zulu = now.toISOString().replace("T", " ").substring(0, 19) + "Z";
      setTimeUtc(zulu);
    };
    updateTime();
    const timer = setInterval(updateTime, 1000);
    return () => clearInterval(timer);
  }, []);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && searchQuery.trim()) {
      onSearchSubmit(searchQuery.trim());
    }
  };

  return (
    <header className="relative z-20 h-16 border-b border-surface-border bg-surface-container-lowest/80 backdrop-blur-md px-4 sm:px-6 flex items-center justify-between gap-4">
      {/* Left: Tactical Mission Status & Coordinates */}
      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full bg-primary animate-pulse" />
          <span className="font-mono text-xs text-primary font-medium tracking-wider uppercase">
            ORBITAL MISSION CONSOLE
          </span>
        </div>

        <div className="hidden lg:flex items-center gap-2 font-mono text-xs text-slate-400 bg-surface-container px-2.5 py-1 rounded border border-surface-border/50">
          <span className="material-symbols-outlined text-xs text-secondary">explore</span>
          <span>{activeCoordinates}</span>
        </div>

        <div className="hidden md:flex items-center gap-1.5 font-mono text-xs text-slate-400">
          <span className="material-symbols-outlined text-xs text-tertiary">schedule</span>
          <span>{timeUtc || "SYNCHRONIZING..."}</span>
        </div>
      </div>

      {/* Center: Command Search / Query Intake */}
      <div className="flex-1 max-w-xl">
        <div className="relative flex items-center">
          <span className="material-symbols-outlined absolute left-3 text-slate-400 text-sm">
            search
          </span>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask AI Environmental Scientist or input observation (e.g., 'Declining pollinators in semi-arid wheat')..."
            className="w-full bg-surface-container/90 border border-surface-border/70 rounded-md py-1.5 pl-9 pr-24 text-xs font-mono text-slate-200 placeholder-slate-500 focus:outline-none focus:border-primary/60 focus:ring-1 focus:ring-primary/40 transition-all"
          />
          <button
            onClick={() => searchQuery.trim() && onSearchSubmit(searchQuery.trim())}
            className="absolute right-1.5 px-2 py-0.5 bg-primary/20 hover:bg-primary/30 border border-primary/40 rounded text-[10px] font-mono text-primary transition-all flex items-center gap-1"
          >
            <span>SUBMIT</span>
            <span className="text-[9px] opacity-70">↵</span>
          </button>
        </div>
      </div>

      {/* Right: Telemetry Health & Action Drawers */}
      <div className="flex items-center gap-3">
        {/* API Health Pill */}
        <div className="hidden sm:flex items-center gap-2 px-2.5 py-1 rounded bg-surface-container border border-surface-border text-xs font-mono">
          <span className={`w-2 h-2 rounded-full ${health?.status === "healthy" ? "bg-primary" : "bg-tertiary"} animate-ping`} />
          <span className="text-slate-300">
            {health?.status === "healthy" ? `CHROMA: ${health.vector_store_documents} DOCS` : "CONNECTING..."}
          </span>
        </div>

        {/* Action CTAs */}
        <button
          onClick={onOpenEvidence}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-surface-container hover:bg-surface-container-high border border-surface-border text-xs font-mono text-secondary hover:text-cyan-300 transition-colors"
          title="Inspect RAG retrieved peer-reviewed papers"
        >
          <span className="material-symbols-outlined text-sm">library_books</span>
          <span className="hidden md:inline">EVIDENCE</span>
        </button>

        <button
          onClick={onOpenSimulator}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-primary/10 hover:bg-primary/20 border border-primary/40 text-xs font-mono text-primary transition-all"
          title="Simulate agroecological interventions"
        >
          <span className="material-symbols-outlined text-sm">tune</span>
          <span className="hidden md:inline">SIMULATOR</span>
        </button>
      </div>
    </header>
  );
};
