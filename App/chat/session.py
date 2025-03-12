"""
Main chat session management.
"""
from typing import Dict, Optional
from .handlers import PromptHandler

class ChatSession:
    def __init__(self):
        self.handler = PromptHandler()
        
    def start_case(self, case_details: str) -> Dict[str, str]:
        """Start a new case with initial details."""
        return self.handler.process_input(case_details)
    
    def approve_stage(self, approved: bool, improvement_text: Optional[str] = None) -> Dict[str, str]:
        """Approve current stage or request improvements."""
        return self.handler.handle_approval(approved, improvement_text)
    
    def get_status(self) -> Dict[str, str]:
        """Get current session status."""
        return self.handler.get_current_state()
    
    def clear_session(self):
        """Clear the current session."""
        self.handler = PromptHandler()
