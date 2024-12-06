import logging
import os
from typing import Dict

from dotenv import load_dotenv


class ConfigError(Exception):
    """Base exception for configuration errors"""
    pass

class MissingAPIKeyError(ConfigError):
    """Raised when a required API key is missing"""
    pass

class Config:
    """Configuration management for Func package"""
    
    @staticmethod
    def _load_api_key(key_name: str) -> str | None:
        """Load and validate a specific API key"""
        api_key = os.getenv(key_name)
        if not api_key or not isinstance(api_key, str) or not api_key.strip():
            return None
        return api_key.strip()
    
    @staticmethod
    def load_config() -> Dict[str, str]:
        """Load configuration from environment variables"""
        load_dotenv()
        config = {}
        
        openai_key = Config._load_api_key('OPENAI_API_KEY')
        anthropic_key = Config._load_api_key('ANTHROPIC_API_KEY')
        
        if openai_key:
            config['OPENAI_API_KEY'] = openai_key
        elif anthropic_key:
            config['ANTHROPIC_API_KEY'] = anthropic_key
        else:
            raise MissingAPIKeyError("Neither OpenAI nor Anthropic API keys found")
            
        logging.info(f"Loaded configuration with {'OpenAI' if openai_key else 'Anthropic'} API key")
        return config