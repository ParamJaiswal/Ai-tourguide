"""Base agent class with common functionality."""

from abc import ABC, abstractmethod
from typing import Any, Dict
from app.utils.logger import setup_logger


class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(self, name: str):
        """
        Initialize the base agent.
        
        Args:
            name: Agent name for logging
        """
        self.name = name
        self.logger = setup_logger(f"agent.{name}")
    
    @abstractmethod
    async def process(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Process the agent's task.
        
        Returns:
            Dictionary with processing results
        """
        pass
    
    def format_response(self, success: bool, data: Any = None, error: str = None) -> Dict[str, Any]:
        """
        Format a standardized agent response.
        
        Args:
            success: Whether the operation was successful
            data: Result data if successful
            error: Error message if unsuccessful
        
        Returns:
            Standardized response dictionary
        """
        response = {
            "agent": self.name,
            "success": success
        }
        
        if success:
            response["data"] = data
        else:
            response["error"] = error
        
        return response
