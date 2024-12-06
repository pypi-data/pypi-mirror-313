import logging
from typing import Optional, Any
from .core.generator import FuncGenerator
from .core.llm_providers.anthropic_provider import AnthropicProvider
from .core.llm_providers.openai_provider import OpenAIProvider
from .core.config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class func:
    _instance = None
    _provider = None
    
    def __init__(self):
        if func._instance is not None:
            raise Exception("func is a singleton. Use func.initialize() instead")
        func._instance = self
    
    @classmethod
    def initialize(cls, provider: str = "openai", **kwargs):
        """Initialize func with specified LLM provider"""
        if cls._instance is None:
            cls._instance = cls()
        
        config = Config.load_config()
        
        if provider == "openai":
            api_key = kwargs.get('api_key', config.get('OPENAI_API_KEY'))
            if not api_key:
                raise ValueError("OpenAI API key is required")
            cls._provider = OpenAIProvider()
            # Use provider's DEFAULT_MODEL if model not specified
            kwargs['model'] = kwargs.get('model', OpenAIProvider.DEFAULT_MODEL)
            cls._provider.initialize(api_key, **kwargs)
        elif provider == "anthropic":
            api_key = kwargs.get('api_key', config.get('ANTHROPIC_API_KEY'))
            if not api_key:
                raise ValueError("Anthropic API key is required")
            cls._provider = AnthropicProvider()
            # Use provider's DEFAULT_MODEL if model not specified
            kwargs['model'] = kwargs.get('model', AnthropicProvider.DEFAULT_MODEL)
            cls._provider.initialize(api_key, **kwargs)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
        return cls._instance
    
    @classmethod
    def generate(cls, prompt: str, call: bool = False, **kwargs) -> Optional[Any]:
        """Generate a function based on the prompt"""
        if cls._instance is None or cls._provider is None:
            raise Exception("func not initialized. Call func.initialize() first")
        
        generator = FuncGenerator(cls._provider)
        return generator.generate(prompt, call, **kwargs)
