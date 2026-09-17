import React from "react";

export const TacticalGrid: React.FC = () => {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
      {/* Tactical Dot Grid */}
      <div
        className="absolute inset-0 opacity-[0.08]"
        style={{
          backgroundImage: `radial-gradient(circle at 1px 1px, #4edea3 1px, transparent 0)`,
          backgroundSize: "28px 28px"
        }}
      />

      {/* Sweep Scan Beam */}
      <div className="absolute inset-0 scan-beam pointer-events-none" />

      {/* Perimeter Vignette */}
      <div className="absolute inset-0 bg-gradient-to-b from-background/70 via-transparent to-background/90" />
    </div>
  );
};
