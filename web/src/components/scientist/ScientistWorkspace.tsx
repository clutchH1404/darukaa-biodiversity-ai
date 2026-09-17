import React, { useState, useRef, useEffect } from "react";
import {
  ChatResponse,
  MissingVariableQuestion,
  RecommendationItem,
  RetrievedEvidence
} from "../../types/api";

interface MessageEntry {
  role: "user" | "assistant";
  content: string;
  responseObj?: ChatResponse;
}

interface ScientistWorkspaceProps {
  chatHistory: MessageEntry[];
  latestResponse: ChatResponse | null;
  isLoading: boolean;
  onSendMessage: (msg: string) => void;
  onAnswerMissingVar: (varName: string, answerValue: string) => void;
  onInspectEvidence: (evidenceList: RetrievedEvidence[]) => void;
}

export const ScientistWorkspace: React.FC<ScientistWorkspaceProps> = ({
  chatHistory,
  latestResponse,
  isLoading,
  onSendMessage,
  onAnswerMissingVar,
  onInspectEvidence
}) => {
  const [inputText, setInputText] = useState("");
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory, isLoading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim() || isLoading) return;
    onSendMessage(inputText.trim());
    setInputText("");
  };

  return (
    <div className="flex flex-col h-[760px] bg-surface-container-lowest/80 border border-surface-border rounded-xl backdrop-blur-md overflow-hidden">
      {/* Console Subheader */}
      <div className="h-12 border-b border-surface-border bg-surface-container-low/60 px-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-primary text-base">
            psychology
          </span>
          <span className="font-mono text-xs font-semibold text-slate-200 uppercase tracking-wider">
            Conversational Environmental Scientist
          </span>
        </div>
        <div className="flex items-center gap-3 text-[10px] font-mono text-slate-400">
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-primary" />
            <span>GROUNDED REASONING ACTIVE</span>
          </span>
          <span className="hidden sm:inline text-slate-600">•</span>
          <span className="hidden sm:inline text-slate-400">SESSION PERSISTED</span>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
        {chatHistory.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-6 space-y-3">
            <div className="w-14 h-14 rounded-full bg-surface-container border border-surface-border flex items-center justify-center text-primary">
              <span className="material-symbols-outlined text-3xl">ecg_heart</span>
            </div>
            <h3 className="font-sans font-semibold text-slate-200 text-sm">
              AI Environmental Scientist Standing By
            </h3>
            <p className="text-xs text-slate-400 max-w-md font-sans">
              Enter an ecological observation, submit a farm query, or choose a Judge Demo Preset from the sidebar.
              The AI will parse variables, detect missing context, and synthesize multi-metric recommendations.
            </p>
          </div>
        ) : (
          chatHistory.map((msg, idx) => (
            <div key={idx} className="space-y-3">
              {msg.role === "user" ? (
                /* User Observation Card */
                <div className="flex items-start gap-3 justify-end">
                  <div className="max-w-2xl bg-surface-container border border-surface-border rounded-lg p-3.5 text-xs text-slate-200 font-sans shadow-md">
                    <div className="flex items-center gap-2 mb-1 text-[10px] font-mono text-secondary uppercase font-semibold">
                      <span className="material-symbols-outlined text-xs">person</span>
                      <span>FIELD OBSERVATION INTAKE</span>
                    </div>
                    <div className="leading-relaxed whitespace-pre-wrap">{msg.content}</div>
                  </div>
                </div>
              ) : (
                /* AI Environmental Scientist Structured Diagnosis */
                <div className="flex items-start gap-3 justify-start">
                  <div className="w-full max-w-4xl bg-surface-container-low/90 border border-surface-border rounded-lg p-4 sm:p-5 text-xs text-slate-200 font-sans shadow-xl space-y-4">
                    {/* Header */}
                    <div className="flex items-center justify-between border-b border-surface-border/60 pb-2">
                      <div className="flex items-center gap-2 text-primary font-mono text-[11px] font-bold uppercase">
                        <span className="material-symbols-outlined text-sm">science</span>
                        <span>BIOPHYSICAL DIAGNOSIS & REASONING TRACE</span>
                      </div>
                      {msg.responseObj && (
                        <div className="font-mono text-[10px] text-slate-400 bg-surface-container px-2 py-0.5 rounded border border-surface-border">
                          CONFIDENCE:{" "}
                          <span className="text-primary font-semibold">
                            {msg.responseObj.confidence_summary.rating}
                          </span>
                        </div>
                      )}
                    </div>

                    {/* Environmental Assessment */}
                    {msg.responseObj?.environmental_assessment && (
                      <div className="space-y-1">
                        <div className="font-mono text-[10px] text-slate-400 uppercase tracking-wider font-semibold">
                          EVALUATION SUMMARY
                        </div>
                        <p className="text-slate-300 leading-relaxed font-sans">
                          {msg.responseObj.environmental_assessment}
                        </p>
                      </div>
                    )}

                    {/* Detected Variables Chips (Hackathon Section 5) */}
                    {msg.responseObj?.updated_environmental_state &&
                      Object.keys(msg.responseObj.updated_environmental_state).length > 0 && (
                        <div className="space-y-1.5">
                          <div className="font-mono text-[10px] text-slate-400 uppercase tracking-wider font-semibold flex items-center gap-1.5">
                            <span className="material-symbols-outlined text-xs text-secondary">
                              fact_check
                            </span>
                            <span>DETECTED & CALIBRATED ENVIRONMENTAL PARAMETERS</span>
                          </div>
                          <div className="flex flex-wrap gap-1.5">
                            {Object.entries(msg.responseObj.updated_environmental_state).map(
                              ([key, val]) => (
                                <span
                                  key={key}
                                  className="inline-flex items-center gap-1 px-2 py-1 rounded bg-surface-container border border-surface-border text-[11px] font-mono text-slate-300"
                                >
                                  <span className="text-slate-500">
                                    {key.replace(/_/g, " ")}:
                                  </span>
                                  <span className="text-primary font-bold">
                                    {String(val)}
                                  </span>
                                </span>
                              )
                            )}
                          </div>
                        </div>
                      )}

                    {/* Multi-Metric Causal Reasoning Narrative (Hackathon Section 10 & 13) */}
                    {msg.responseObj?.multi_metric_reasoning && (
                      <div className="p-3 rounded bg-surface-container/60 border border-surface-border space-y-1.5">
                        <div className="font-mono text-[10px] text-secondary uppercase tracking-wider font-semibold flex items-center gap-1.5">
                          <span className="material-symbols-outlined text-xs">
                            alt_route
                          </span>
                          <span>CAUSAL BIOPHYSICAL CHAIN (≥3 VARIABLES SUPERIMPOSED)</span>
                        </div>
                        <p className="text-slate-300 leading-relaxed font-sans">
                          {msg.responseObj.multi_metric_reasoning}
                        </p>
                      </div>
                    )}

                    {/* Missing Context Clarifying Questions Deck (Hackathon Section 6) */}
                    {msg.responseObj?.missing_variables_detected &&
                      msg.responseObj.missing_variables_detected.length > 0 && (
                        <div className="p-3.5 rounded bg-tertiary/10 border border-tertiary/30 space-y-2.5">
                          <div className="flex items-center gap-1.5 text-tertiary font-mono text-[11px] font-bold uppercase">
                            <span className="material-symbols-outlined text-sm">
                              help_outline
                            </span>
                            <span>MISSING ENVIRONMENTAL CONTEXT INQUIRIES</span>
                          </div>
                          <p className="text-[11px] text-slate-300">
                            To refine biophysical impact models and prevent generic recommendations, please provide:
                          </p>
                          <div className="space-y-2">
                            {msg.responseObj.missing_variables_detected.map((q) => (
                              <div
                                key={q.variable_name}
                                className="bg-surface-container-lowest/80 p-2.5 rounded border border-surface-border text-[11px] space-y-1.5"
                              >
                                <div className="flex items-center justify-between">
                                  <span className="font-mono font-bold text-slate-200">
                                    {q.variable_name.replace(/_/g, " ").toUpperCase()}
                                  </span>
                                  <span className="text-[9px] font-mono text-tertiary">
                                    HIGH VALUE
                                  </span>
                                </div>
                                <div className="text-slate-300">{q.question_text}</div>
                                {q.suggested_options && (
                                  <div className="flex flex-wrap gap-1.5 pt-1">
                                    {q.suggested_options.map((opt) => (
                                      <button
                                        key={opt}
                                        onClick={() => onAnswerMissingVar(q.variable_name, opt)}
                                        className="px-2 py-0.5 rounded bg-surface-container hover:bg-surface-container-high border border-surface-border hover:border-primary/40 text-[10px] font-mono text-primary transition-colors"
                                      >
                                        + {opt}
                                      </button>
                                    ))}
                                  </div>
                                )}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                    {/* Recommendations (Hackathon Section 12) */}
                    {msg.responseObj?.recommendations &&
                      msg.responseObj.recommendations.length > 0 && (
                        <div className="space-y-3 pt-1">
                          <div className="font-mono text-[10px] text-slate-400 uppercase tracking-wider font-semibold flex items-center justify-between">
                            <span>RECOMMENDED INTERVENTIONS (10-POINT EVIDENCE SCHEMA)</span>
                            <span className="text-primary font-mono">
                              {msg.responseObj.recommendations.length} PROTOCOLS
                            </span>
                          </div>

                          <div className="space-y-2.5">
                            {msg.responseObj.recommendations.map((rec, rIdx) => (
                              <div
                                key={rec.id || rIdx}
                                className="bg-surface-container p-3 rounded border border-surface-border space-y-2"
                              >
                                <div className="flex items-center justify-between">
                                  <div className="font-mono font-bold text-xs text-slate-100 flex items-center gap-1.5">
                                    <span className="text-primary">{rIdx + 1}.</span>
                                    <span>{rec.title}</span>
                                  </div>
                                  <span className="font-mono text-[10px] px-2 py-0.5 rounded bg-primary/20 text-primary border border-primary/40 font-semibold">
                                    {rec.time_horizon}
                                  </span>
                                </div>

                                <div className="text-[11px] text-slate-300">
                                  <strong className="text-slate-200">What to do:</strong>{" "}
                                  {rec.what_to_do}
                                </div>

                                <div className="text-[11px] text-slate-300">
                                  <strong className="text-slate-200">Why it works:</strong>{" "}
                                  {rec.why_it_works}
                                </div>

                                {/* Impacted Metrics */}
                                <div className="flex flex-wrap gap-1">
                                  {rec.impacted_metrics.map((m) => (
                                    <span
                                      key={m}
                                      className="px-1.5 py-0.5 bg-surface-container-high rounded text-[10px] font-mono text-secondary"
                                    >
                                      {m}
                                    </span>
                                  ))}
                                </div>

                                {/* Citations */}
                                {rec.scientific_evidence && rec.scientific_evidence.length > 0 && (
                                  <div className="pt-1 border-t border-surface-border/50 flex flex-wrap items-center gap-2 text-[10px] font-mono text-slate-400">
                                    <span className="text-slate-500">EVIDENCE:</span>
                                    {rec.scientific_evidence.map((cit, cIdx) => (
                                      <a
                                        key={cIdx}
                                        href={cit.url}
                                        target="_blank"
                                        rel="noreferrer"
                                        className="text-primary hover:underline"
                                      >
                                        [{cit.source_organization} {cit.year}]
                                      </a>
                                    ))}
                                  </div>
                                )}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                    {/* Retrieved Evidence CTA */}
                    {msg.responseObj?.evidence_retrieved &&
                      msg.responseObj.evidence_retrieved.length > 0 && (
                        <div className="pt-2 flex items-center justify-between border-t border-surface-border/60">
                          <span className="font-mono text-[10px] text-slate-400">
                            {msg.responseObj.evidence_retrieved.length} PEER-REVIEWED SOURCES RETRIEVED VIA CHROMADB
                          </span>
                          <button
                            onClick={() =>
                              msg.responseObj &&
                              onInspectEvidence(msg.responseObj.evidence_retrieved)
                            }
                            className="px-2.5 py-1 rounded bg-secondary/15 hover:bg-secondary/25 border border-secondary/40 text-[10px] font-mono text-secondary transition-all"
                          >
                            INSPECT RAG EVIDENCE DRAWER →
                          </button>
                        </div>
                      )}
                  </div>
                </div>
              )}
            </div>
          ))
        )}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex items-start gap-3">
            <div className="bg-surface-container-low border border-surface-border rounded-lg p-4 font-mono text-xs text-secondary flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-secondary animate-ping" />
              <span>AI Environmental Scientist synthesizing biophysical causal pathways...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Message Input Footer */}
      <form
        onSubmit={handleSubmit}
        className="p-3 sm:p-4 border-t border-surface-border bg-surface-container-lowest/90 flex gap-2"
      >
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Type your environmental question or provide missing variable values..."
          disabled={isLoading}
          className="flex-1 bg-surface-container border border-surface-border rounded-md px-3.5 py-2 text-xs font-mono text-slate-100 placeholder-slate-500 focus:outline-none focus:border-primary/60 focus:ring-1 focus:ring-primary/40 disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={isLoading || !inputText.trim()}
          className="px-4 py-2 rounded-md bg-primary hover:bg-emerald-400 text-background font-mono text-xs font-bold transition-all disabled:opacity-50 flex items-center gap-1.5"
        >
          <span>TRANSMIT</span>
          <span className="material-symbols-outlined text-sm">send</span>
        </button>
      </form>
    </div>
  );
};
