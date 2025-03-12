"""
Agent for generating and validating treatment plans based on analysis.
"""
from typing import Dict, List
from ..models.azure import AzureModel
from ..utils.prompts import TREATMENT_PROMPT, format_prompt
from ..utils.schemas import Treatment, TreatmentPlan

class TreatmentPlanner:
    def __init__(self):
        """Initialize the planner with Azure LLM model."""
        self.llm = AzureModel()

    def generate_plan(self, diagnosis_info: Dict) -> Dict:
        """
        Generate treatment plan based on diagnosis information.
        
        Args:
            diagnosis_info (Dict): Complete diagnosis information
            
        Returns:
            Dict: Treatment plan with raw text response
        """
        prompt = format_prompt(TREATMENT_PROMPT, diagnosis_info=diagnosis_info)
        response = self.llm.invoke(prompt)
        
        # Create a dictionary to hold both empty structured data and raw text
        result = {
            'plan': TreatmentPlan(
                primary_treatments=[],
                secondary_treatments=[],
                monitoring_plan=[],
                expected_outcomes={},
                alternative_plans=[]
            ).dict(),  # Empty plan for future structured data
            'raw_text': response  # Store raw text for display
        }
        
        # Future enhancement: Parse response into structured format
        # if enable_structured_data:
        #     result['plan'] = self._parse_treatment_response(response).dict()
        
        return result

    def _parse_treatment_response(self, response: str) -> TreatmentPlan:
        """
        Parse LLM response into structured treatment plan.
        This is a placeholder for future implementation of structured data parsing.
        
        Args:
            response (str): Raw LLM response
            
        Returns:
            TreatmentPlan: Structured treatment plan
        """
        # TODO: Implement structured parsing logic
        # Example implementation:
        # primary = []
        # secondary = []
        # monitoring = []
        # outcomes = {}
        # alternatives = []
        # 
        # sections = response.split("\n\n")
        # for section in sections:
        #     if "Primary Treatments" in section:
        #         for line in section.split("\n"):
        #             if line.startswith("-"):
        #                 primary.append(Treatment(
        #                     name=line.strip("- "),
        #                     category="primary"
        #                 ))
        # ...
        
        return TreatmentPlan(
            primary_treatments=[],
            secondary_treatments=[],
            monitoring_plan=[],
            expected_outcomes={},
            alternative_plans=[]
        )

def generate_treatment_options(diagnosis: Dict) -> Dict:
    """
    Convenience function for generating treatment options.
    
    Args:
        diagnosis (Dict): Diagnosis information
        
    Returns:
        Dict: Treatment plan
    """
    planner = TreatmentPlanner()
    plan = planner.generate_plan(diagnosis)
    return plan.dict()

def create_final_plan(treatment_options: List[Dict]) -> Dict:
    """
    Convenience function for creating final treatment plan.
    
    Args:
        treatment_options (List[Dict]): List of possible treatments
        
    Returns:
        Dict: Final treatment plan
    """
    # Basic implementation - would need proper plan finalization logic
    return TreatmentPlan(
        primary_treatments=[],
        secondary_treatments=[],
        monitoring_plan=[],
        expected_outcomes={},
        alternative_plans=[]
    ).dict()
