from abc import ABC, abstractmethod
from typing import Dict, Any, List
from langchain_mistralai import ChatMistralAI
import config

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.llm = ChatMistralAI(
            model="mistral-large-latest",
            mistral_api_key=config.MISTRAL_API_KEY,
            temperature=0.7
        )
        self.memory = []
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return output"""
        pass
    
    def add_to_memory(self, data: Dict[str, Any]):
        """Add data to agent memory"""
        self.memory.append(data)
    
    def get_memory(self) -> List[Dict[str, Any]]:
        """Get agent memory"""
        return self.memory
    
    def clear_memory(self):
        """Clear agent memory"""
        self.memory = []
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "name": self.name,
            "description": self.description,
            "memory_size": len(self.memory),
            "status": "active"
        }
