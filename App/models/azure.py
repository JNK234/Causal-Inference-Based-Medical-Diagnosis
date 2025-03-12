"""
Azure OpenAI model integration.
Handles all interactions with Azure OpenAI service.
"""
import logging
from langchain_openai import AzureOpenAI, AzureChatOpenAI
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class AzureModel:
    def __init__(self):
        """Initialize Azure OpenAI model."""
        try:
            self.llm = AzureChatOpenAI(
                deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                azure_endpoint=os.getenv("AZURE_OPENAI_API_BASE"),
                openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
                temperature=0.5,
                max_tokens=9000
            )
            
        except Exception as e:
            logging.error(f"Failed to initialize Azure OpenAI LLM: {str(e)}")
            raise

    def generate(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate response from a list of messages.
        
        Args:
            messages (List[Dict[str, str]]): List of message dictionaries
            
        Returns:
            str: Generated response
        """
        # Format messages into a single string
        # formatted_messages = "\n".join([f"{message['role']}: {message['content']}" for message in messages])
        
        # Convert it into list
        formatted_messages = [(message["role"], message["content"]) for message in messages]
        return self.invoke(formatted_messages)

    def invoke(self, prompt: str) -> str:
        """
        Generate response from a single prompt.
        
        Args:
            prompt (str): Input prompt
            
        Returns:
            str: Generated response
        """
        try:
            return self.llm.invoke(prompt)
        except Exception as e:
            logging.error(f"Error invoking Azure OpenAI: {str(e)}")
            raise
