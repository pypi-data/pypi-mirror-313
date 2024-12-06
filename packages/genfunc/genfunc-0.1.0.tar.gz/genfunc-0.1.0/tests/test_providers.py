import os

import pytest
from dotenv import load_dotenv

from genfunc.core.llm_providers.anthropic_provider import AnthropicProvider
from genfunc.core.llm_providers.openai_provider import OpenAIProvider

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

def test_openai_provider():
    provider = OpenAIProvider()
    provider.initialize(OPENAI_API_KEY)
    
    code = provider.generate_function("Create a function that returns Hello World")
    assert isinstance(code, str)
    assert 'def' in code
    assert 'return' in code

def test_anthropic_provider():
    provider = AnthropicProvider()
    provider.initialize(ANTHROPIC_API_KEY)
    
    code = provider.generate_function("Create a function that returns Hello World")
    assert isinstance(code, str)
    assert 'def' in code
    assert 'return' in code
