from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """Base class for LLM providers"""
    
    @abstractmethod
    def initialize(self, api_key: str, **kwargs) -> None:
        """Initialize the LLM provider with API key and optional parameters"""
        pass
    
    @abstractmethod
    def generate_function(self, prompt: str) -> str:
        """Generate Python function code based on the prompt"""
        pass
