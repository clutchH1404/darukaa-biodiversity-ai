from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from .environmental_state import EnvironmentalState
from .knowledge_schema import RetrievedEvidence, CitationItem

class MissingVariableQuestion(BaseModel):
    variable_name: str
    question_text: str
    importance: str
    suggested_options: Optional[List[str]] = None

class RecommendationItem(BaseModel):
    id: str
    title: str
    what_to_do: str = Field(..., description="A. Specific, context-sensitive intervention")
    why_it_works: str = Field(..., description="B. Bio-physical and ecological mechanisms")
    variables_involved: List[str] = Field(..., min_length=3, description="C. Must involve at least 3 environmental variables")
    impacted_metrics: List[str] = Field(..., description="D. Impacted metrics with defensible direction")
    time_horizon: str = Field(..., description="E. Short (1 season) / Medium (2-3 yrs) / Long (3+ yrs)")
    expected_direction: str = Field(..., description="F. e.g. SOC ↑, Water Retention ↑, Pests ↓")
    confidence: str = Field(..., description="G. High, Medium, or Low")
    confidence_reason: str = Field(..., description="Explicit rationale for confidence score")
    scientific_evidence: List[CitationItem] = Field(..., description="H. Authentic scientific evidence")
    important_assumptions: List[str] = Field(..., description="I. Environmental and physical constraints")
    possible_trade_offs: List[str] = Field(..., description="J. Risks, labour, cost, water competition")

class ReasoningFactor(BaseModel):
    source_variable: str
    target_variable: str
    relationship_type: str  # positive, negative, threshold
    mechanism: str

class ReasoningTrace(BaseModel):
    primary_bottlenecks: List[str]
    causal_chains: List[str]
    interacting_variables: List[str]
    ecological_narrative: str

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    environmental_state: Optional[EnvironmentalState] = None
    geographic_context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    conversation_id: str
    formatted_response: str
    environmental_assessment: str
    key_drivers: List[str]
    multi_metric_reasoning: str
    recommendations: List[RecommendationItem]
    trade_offs_and_risks: List[str]
    evidence_retrieved: List[RetrievedEvidence]
    missing_variables_detected: List[MissingVariableQuestion]
    updated_environmental_state: Dict[str, Any]
    confidence_summary: Dict[str, Any]
    debug_trace: Optional[Dict[str, Any]] = None

class AnalyzeRequest(BaseModel):
    environmental_state: EnvironmentalState
    user_notes: Optional[str] = None

class AnalyzeResponse(BaseModel):
    assessment: str
    bottlenecks: List[str]
    risk_level: str
    reasoning_trace: ReasoningTrace
    variables_evaluated: Dict[str, Any]
    missing_critical_variables: List[MissingVariableQuestion]
