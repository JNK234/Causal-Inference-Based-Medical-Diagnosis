"""
LangGraph workflow definition for the diagnosis process.
Manages state transitions and agent coordination.
"""
from typing import Dict, List
from agents.extractor import extract_nodes
from agents.analyzer import analyze_causal_links, analyze_counterfactuals
from agents.validator import check_missing_info, generate_followup_questions
from agents.planner import generate_treatment_options, create_final_plan

class DiagnosisWorkflow:
    def __init__(self):
        """Initialize the diagnosis workflow."""
        self._setup_workflow()

    def _setup_workflow(self):
        """Setup the workflow states."""
        pass

    def _validate_info(self, state: Dict) -> Dict:
        """
        Validate extracted information.
        
        Args:
            state (Dict): Current workflow state
            
        Returns:
            Dict: Updated state with validation results
        """
        missing_info = check_missing_info(state["nodes"])
        if missing_info:
            questions = generate_followup_questions(missing_info)
            state["missing_info"] = missing_info
            state["questions"] = questions
            state["complete"] = False
        else:
            state["complete"] = True
        return state

    def _check_validation(self, state: Dict) -> str:
        """
        Check validation result and determine next step.
        
        Args:
            state (Dict): Current workflow state
            
        Returns:
            str: Next step to take
        """
        return "complete" if state.get("complete", False) else "incomplete"

    def _analyze_causal(self, state: Dict) -> Dict:
        """
        Perform causal analysis.
        
        Args:
            state (Dict): Current workflow state
            
        Returns:
            Dict: Updated state with causal analysis
        """
        causal_links = analyze_causal_links(state["nodes"])
        counterfactuals = analyze_counterfactuals(state["nodes"])
        state["analysis"] = {
            "causal_links": causal_links,
            "counterfactuals": counterfactuals
        }
        return state

    def _plan_treatment(self, state: Dict) -> Dict:
        """
        Generate treatment plan.
        
        Args:
            state (Dict): Current workflow state
            
        Returns:
            Dict: Updated state with treatment plan
        """
        treatment_options = generate_treatment_options(state["analysis"])
        final_plan = create_final_plan(treatment_options)
        state["treatment_plan"] = final_plan
        return state

    def run(self, case_text: str) -> Dict:
        """
        Run the diagnosis workflow.
        
        Args:
            case_text (str): Patient case text
            
        Returns:
            Dict: Final workflow state
        """
        # Initialize state
        state = {"case_text": case_text}
        
        # Step 1: Extract nodes
        state["nodes"] = extract_nodes(case_text)
        
        # Step 2: Validate information
        state = self._validate_info(state)
        if not state.get("complete", False):
            return state
        
        # Step 3: Analyze causal relationships
        state = self._analyze_causal(state)
        
        # Step 4: Generate treatment plan
        state = self._plan_treatment(state)
        
        return state

def run_diagnosis(case_text: str) -> Dict:
    """
    Convenience function to run diagnosis workflow.
    
    Args:
        case_text (str): Patient case text
        
    Returns:
        Dict: Diagnosis results
    """
    workflow = DiagnosisWorkflow()
    return workflow.run(case_text)
