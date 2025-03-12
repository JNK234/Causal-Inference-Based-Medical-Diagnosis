"""
Pydantic models for structured data handling.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel

class MedicalNode(BaseModel):
    """Base class for medical information nodes."""
    description: str
    category: str
    confidence: Optional[float] = None

class MedicalNodes(BaseModel):
    """Container for all extracted medical nodes."""
    symptoms: List[MedicalNode] = []
    conditions: List[MedicalNode] = []
    history: List[MedicalNode] = []
    exam_findings: List[MedicalNode] = []
    diagnostics: List[MedicalNode] = []
    interventions: List[MedicalNode] = []

class CausalLink(BaseModel):
    """Represents a causal relationship between nodes."""
    cause: str
    effect: str
    strength: Optional[float] = None
    evidence: Optional[str] = None

class CausalAnalysis(BaseModel):
    """Complete causal analysis results."""
    direct_links: List[CausalLink] = []
    confounders: List[Dict[str, str]] = []
    mediators: List[Dict[str, str]] = []
    instrumental_variables: List[Dict[str, str]] = []

class Counterfactual(BaseModel):
    """Represents a counterfactual scenario."""
    scenario: str
    impact: str
    probability: Optional[float] = None

class Treatment(BaseModel):
    """Represents a treatment option."""
    name: str
    category: str  # causal, preventative, or symptomatic
    effectiveness: Optional[float] = None
    risks: List[str] = []
    contraindications: List[str] = []

class TreatmentPlan(BaseModel):
    """Complete treatment plan."""
    primary_treatments: List[Treatment] = []
    secondary_treatments: List[Treatment] = []
    monitoring_plan: List[str] = []
    expected_outcomes: Dict[str, str] = {}
    alternative_plans: List[Dict[str, List[Treatment]]] = []
