"""
Handlers for processing chat prompts and responses.
"""
from typing import Dict, Optional
from ..models.azure import AzureModel
from ..utils.prompts import NODE_EXTRACTION_PROMPT, format_prompt
from .memory import ChatMemory

class PromptHandler:
    def __init__(self):
        self.azure_model = AzureModel()
        self.memory = ChatMemory()
        
    def process_input(self, user_input: str) -> Dict[str, str]:
        """Process user input based on current stage."""
        if self.memory.current_stage == "NODE_EXTRACTION":
            # Format the node extraction prompt with case details
            prompt = format_prompt(NODE_EXTRACTION_PROMPT, case_text=user_input)
            
            # Get response from Azure
            response = self.azure_model.invoke(prompt)
            
            # Store the result
            self.memory.store_stage_result(response)
            self.memory.add_message("user", user_input)
            self.memory.add_message("assistant", response)
            
            return {
                "stage": self.memory.current_stage,
                "response": response,
                "status": "awaiting_approval"
            }
            
    def handle_approval(self, approved: bool, improvement_text: Optional[str] = None) -> Dict[str, str]:
        """Handle user approval or improvement request."""
        if not approved and improvement_text:
            # Process the improvement
            return self.process_input(improvement_text)
            
        # For now, just return success message since we only have one stage
        return {
            "stage": self.memory.current_stage,
            "response": "Stage completed successfully.",
            "status": "completed"
        }
        
    def get_current_state(self) -> Dict[str, str]:
        """Get current state of the chat session."""
        return {
            "stage": self.memory.current_stage,
            "current_result": self.memory.get_stage_result(),
            "history": self.memory.get_messages()
        }
