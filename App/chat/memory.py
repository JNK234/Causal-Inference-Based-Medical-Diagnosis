"""
Simple memory implementation for chat sessions.
"""
from typing import List, Dict

class ChatMemory:
    def __init__(self):
        self.messages: List[Dict[str, str]] = []
        self.current_stage = "NODE_EXTRACTION"
        self.stage_results = {}
    
    def add_message(self, role: str, content: str):
        """Add a message to memory."""
        self.messages.append({
            "role": role,
            "content": content
        })
    
    def get_messages(self) -> List[Dict[str, str]]:
        """Get all messages."""
        return self.messages
    
    def store_stage_result(self, result: str):
        """Store result for current stage."""
        self.stage_results[self.current_stage] = result
    
    def get_stage_result(self) -> str:
        """Get result for current stage."""
        return self.stage_results.get(self.current_stage, "")
    
    def clear(self):
        """Clear all memory."""
        self.messages = []
        self.stage_results = {}
