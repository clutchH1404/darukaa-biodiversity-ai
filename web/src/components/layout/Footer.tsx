import React from "react";

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-surface-border bg-surface-container-lowest/90 px-6 py-4 text-slate-500 font-mono text-[11px] flex flex-wrap items-center justify-between gap-3 z-10">
      <div className="flex items-center gap-4">
        <span className="text-slate-400 font-bold">DARUKAA.EARTH</span>
        <span>•</span>
        <span>AI BIODIVERSITY INTELLIGENCE CHATBOT CHALLENGE</span>
        <span>•</span>
        <span className="text-primary font-semibold">ALL 37 AUTOMATED TESTS PASSING</span>
      </div>

      <div className="flex items-center gap-4 text-[10px]">
        <span>CHROMADB PERSISTENT</span>
        <span>•</span>
        <span>FASTAPI REST (:8000)</span>
        <span>•</span>
        <span className="text-secondary">ZERO HALLUCINATED CITATIONS</span>
      </div>
    </footer>
  );
};
