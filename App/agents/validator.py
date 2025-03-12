"""
Agent for validating information completeness and requesting missing data.
"""
from typing import Dict, List, Tuple
from ..models.azure import AzureModel
from ..utils.prompts import VALIDATION_PROMPT, format_prompt

class InfoValidator:
    def __init__(self):
        """Initialize the validator with Azure LLM model."""
        self.llm = AzureModel()

    def check_completeness(self, current_info: Dict) -> Dict:
        """
        Check if all necessary information is present.
        
        Args:
            current_info (Dict): Current medical information
            
        Returns:
            Dict: Validation results with raw text response
        """
        prompt = format_prompt(VALIDATION_PROMPT, current_info=current_info)
        response = self.llm.invoke(prompt)
        
        # Create a dictionary to hold both empty structured data and raw text
        result = {
            'ready': True,  # Default to True for now
            'missing': [],  # Empty list for future structured data
            'questions': [],  # Empty list for future structured data
            'raw_text': response  # Store raw text for display
        }
        
        # Future enhancement: Parse response into structured format
        # if enable_structured_data:
        #     ready, missing, questions = self._parse_validation_response(response)
        #     result.update({
        #         'ready': ready,
        #         'missing': missing,
        #         'questions': questions
        #     })
        
        return result

    def _parse_validation_response(self, response: str) -> Tuple[bool, List[str], List[str]]:
        """
        Parse LLM response into structured validation results.
        This is a placeholder for future implementation of structured data parsing.
        
        Args:
            response (str): Raw LLM response
            
        Returns:
            Tuple[bool, List[str], List[str]]: Structured validation results
        """
        # TODO: Implement structured parsing logic
        # Example implementation:
        # ready = "Ready to proceed" in response
        # missing = []
        # questions = []
        # for line in response.split('\n'):
        #     if line.startswith('Missing:'):
        #         missing.append(line.replace('Missing:', '').strip())
        #     elif line.startswith('Question:'):
        #         questions.append(line.replace('Question:', '').strip())
        return True, [], []

def check_missing_info(current_info: Dict) -> List[str]:
    """
    Convenience function for checking missing information.
    
    Args:
        current_info (Dict): Current medical information
        
    Returns:
        List[str]: List of missing information items
    """
    validator = InfoValidator()
    ready, missing, _ = validator.check_completeness(current_info)
    return missing

def generate_followup_questions(missing_info: List[str]) -> List[str]:
    """
    Convenience function for generating follow-up questions.
    
    Args:
        missing_info (List[str]): List of missing information items
        
    Returns:
        List[str]: List of follow-up questions
    """
    # Basic implementation - would need proper question generation logic
    return [f"Can you provide more information about {item}?" for item in missing_info]
