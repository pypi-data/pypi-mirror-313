import os
from pathlib import Path

import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session")
def cleanup_helpers():
    """Clean up helpers directory before and after tests"""
    # Setup
    helpers_dir = Path('./helpers')
    helpers_dir.mkdir(exist_ok=True)
    for file in helpers_dir.glob('*.py'):
        if file.name != '__init__.py':
            file.unlink()
            
    # yield
    
    # # Teardown
    # for file in helpers_dir.glob('*.py'):
    #     if file.name != '__init__.py':
    #         file.unlink()

@pytest.fixture(scope="session")
def openai_api_key():
    """Get OpenAI API key from environment"""
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        pytest.skip("OpenAI API key not found")
    return api_key

@pytest.fixture(scope="session")
def anthropic_api_key():
    """Get Anthropic API key from environment"""
    load_dotenv()
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        pytest.skip("Anthropic API key not found")
    return api_key
