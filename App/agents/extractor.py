"""
Agent responsible for extracting key medical factors from patient case.
Uses LLM to extract and categorize information based on the provided prompt.
"""
from typing import Dict
from ..models.azure import AzureModel
from ..utils.prompts import NODE_EXTRACTION_PROMPT, format_prompt
from ..utils.schemas import MedicalNodes, MedicalNode
from typing import List

class NodeExtractor:
    def __init__(self):
        """Initialize the extractor with Azure LLM model."""
        self.llm = AzureModel()

    def extract_nodes(self, case_text: str, chat_history: List[Dict[str, str]] = None) -> MedicalNodes:
        """
        Extract medical nodes from the case text and chat history using LLM.
        
        Args:
            case_text (str): Raw patient case text
            chat_history (List[Dict[str, str]], optional): Chat history
            
        Returns:
            MedicalNodes: Medical information with raw text response
        """
        # Format the extraction prompt
        prompt = format_prompt(NODE_EXTRACTION_PROMPT, case_text=case_text)
        
        # Prepare messages for LLM
        messages = chat_history or []
        messages.append({'role': 'user', 'content': prompt})
        
        # Get LLM response
        response = self.llm.generate(messages)
                
        # Create empty MedicalNodes object for future schema implementation
        nodes = MedicalNodes(
            symptoms=[],
            conditions=[],
            history=[],
            exam_findings=[],
            diagnostics=[],
            interventions=[],
            # raw_text=response.content
        )
        
        # Store raw text for chat display
        # Note: This is a custom attribute not defined in the schema
        # It won't affect JSON serialization but will be available for display
        # setattr(nodes, 'raw_text', )
        
        # print(response)
        
        # Future enhancement: Implement proper parsing logic here
        # if enable_structured_data:
        #     return self._parse_response(response)
        
        return response.content
    
    def _parse_response(self, response: str) -> MedicalNodes:
        """
        Parse LLM response into structured MedicalNodes format.
        This is a placeholder for future implementation of structured data parsing.
        
        Args:
            response (str): Raw LLM response
            
        Returns:
            MedicalNodes: Structured medical information
        """
        # TODO: Implement structured parsing logic
        # Example implementation:
        # sections = response.split("\n\n")
        # for section in sections:
        #     if "Patient Symptoms & Observations" in section:
        #         symptoms = [
        #             MedicalNode(
        #                 description=item.strip("- "), 
        #                 category="symptom"
        #             )
        #             for item in section.split("\n") 
        #             if item.strip().startswith("-")
        #         ]
        # ...
        
        return MedicalNodes(
            symptoms=[],
            conditions=[],
            history=[],
            exam_findings=[],
            diagnostics=[],
            interventions=[]
        )

def extract_nodes(case_text: str) -> Dict:
    """
    Convenience function for extracting nodes from case text.
    
    Args:
        case_text (str): Raw patient case text
        
    Returns:
        Dict: Extracted medical nodes
    """
    extractor = NodeExtractor()
    nodes = extractor.extract_nodes(case_text)
    return nodes.dict()
