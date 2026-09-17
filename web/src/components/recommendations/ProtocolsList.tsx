import React from "react";
import { RecommendationItem } from "../../types/api";

interface ProtocolsListProps {
  recommendations: RecommendationItem[];
  onSimulateProtocol?: (recTitle: string) => void;
  onInspectEvidence?: () => void;
}

export const ProtocolsList: React.FC<ProtocolsListProps> = ({
  recommendations,
  onSimulateProtocol,
  onInspectEvidence
}) => {
  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="bg-surface-container-lowest/80 border border-surface-border rounded-xl p-8 text-center space-y-3">
        <span className="material-symbols-outlined text-3xl text-slate-600">
          playlist_add_check
        </span>
        <h3 className="font-mono text-sm font-semibold text-slate-300">
          No Recommendation Protocols Active
        </h3>
        <p className="text-xs text-slate-500 max-w-md mx-auto">
          Submit an environmental observation or choose a Judge Preset to trigger the multi-metric reasoning engine.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-primary text-base">
            task_alt
          </span>
          <h2 className="font-mono text-sm font-bold text-slate-100 uppercase tracking-wider">
            Evidence-Backed Agroecological Protocols (10-Point Schema)
          </h2>
        </div>
        <span className="text-[10px] font-mono text-slate-400 bg-surface-container px-2.5 py-1 rounded border border-surface-border">
          {recommendations.length} SCIENTIFIC INTERVENTIONS
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {recommendations.map((rec, idx) => (
          <div
            key={rec.id || idx}
            className="flex flex-col justify-between bg-surface-container-lowest/90 border border-surface-border hover:border-primary/40 rounded-xl p-5 backdrop-blur-sm transition-all shadow-md group"
          >
            <div className="space-y-3">
              {/* Card Header */}
              <div className="flex items-start justify-between gap-2 border-b border-surface-border/60 pb-2.5">
                <div className="space-y-0.5">
                  <span className="text-[10px] font-mono text-primary font-bold">
                    PROTOCOL 0{idx + 1}
                  </span>
                  <h3 className="font-sans font-bold text-sm text-slate-100 group-hover:text-primary transition-colors">
                    {rec.title}
                  </h3>
                </div>
                <span className="text-[9px] font-mono px-2 py-0.5 rounded bg-primary/10 text-primary border border-primary/30 shrink-0 font-semibold">
                  {rec.time_horizon}
                </span>
              </div>

              {/* What to do */}
              <div className="space-y-1">
                <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider block font-semibold">
                  ACTION
                </span>
                <p className="text-xs text-slate-300 font-sans leading-relaxed">
                  {rec.what_to_do}
                </p>
              </div>

              {/* Why it works */}
              <div className="space-y-1">
                <span className="text-[10px] font-mono text-secondary uppercase tracking-wider block font-semibold">
                  BIOPHYSICAL MECHANISM
                </span>
                <p className="text-xs text-slate-400 font-sans leading-relaxed">
                  {rec.why_it_works}
                </p>
              </div>

              {/* Impacted Metrics */}
              <div className="space-y-1.5 pt-1">
                <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider block font-semibold">
                  IMPACTED METRICS
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {rec.impacted_metrics.map((m) => (
                    <span
                      key={m}
                      className="px-2 py-0.5 bg-surface-container rounded text-[10px] font-mono text-emerald-300 border border-emerald-500/20"
                    >
                      {m}
                    </span>
                  ))}
                </div>
              </div>

              {/* Confidence & Rationale */}
              <div className="p-2.5 rounded bg-surface-container/60 border border-surface-border text-[11px] font-mono space-y-1">
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">CALCULATED CONFIDENCE:</span>
                  <span className="text-primary font-bold">{rec.confidence}</span>
                </div>
                <div className="text-[10px] text-slate-400 font-sans">
                  {rec.confidence_reason}
                </div>
              </div>

              {/* Citations */}
              {rec.scientific_evidence && rec.scientific_evidence.length > 0 && (
                <div className="space-y-1 pt-1">
                  <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider block">
                    PEER-REVIEWED CITATIONS
                  </span>
                  <div className="space-y-1">
                    {rec.scientific_evidence.slice(0, 2).map((cit, cIdx) => (
                      <a
                        key={cIdx}
                        href={cit.url}
                        target="_blank"
                        rel="noreferrer"
                        className="block text-[11px] font-sans text-slate-400 hover:text-primary transition-colors line-clamp-1"
                      >
                        • <strong className="text-slate-300 font-mono text-[10px]">{cit.source_organization} ({cit.year}):</strong> {cit.title}
                      </a>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* CTA Buttons */}
            <div className="pt-4 mt-3 border-t border-surface-border/60 flex items-center justify-between gap-2">
              {onSimulateProtocol && (
                <button
                  onClick={() => onSimulateProtocol(rec.title)}
                  className="flex-1 py-1.5 px-2.5 rounded bg-primary/10 hover:bg-primary/20 border border-primary/40 text-[11px] font-mono text-primary transition-all flex items-center justify-center gap-1.5"
                >
                  <span className="material-symbols-outlined text-xs">tune</span>
                  <span>SIMULATE DELTA</span>
                </button>
              )}
              {onInspectEvidence && (
                <button
                  onClick={onInspectEvidence}
                  className="py-1.5 px-2.5 rounded bg-surface-container hover:bg-surface-container-high border border-surface-border text-[11px] font-mono text-slate-300 hover:text-secondary transition-all"
                  title="Inspect peer-reviewed chunks in drawer"
                >
                  PROOF
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
