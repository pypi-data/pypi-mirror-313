import os
from pathlib import Path

import pytest

from genfunc import func

def test_generate_function(cleanup_helpers, openai_api_key):
    func.initialize(provider="openai", api_key=openai_api_key)
    prompt = "Create a function that adds two numbers"
    result = func.generate(prompt)
    assert result is None
    
    # Check if file was created
    files = list(Path('./helpers').glob('*.py'))
    assert len(files) == 1
    
    # Check if file contains valid Python code
    with open(files[0]) as f:
        code = f.read()
    
    # Basic validation
    assert 'def' in code
    assert 'return' in code

def test_generate_and_call_function(cleanup_helpers, openai_api_key):
    func.initialize(provider="openai", api_key=openai_api_key)
    prompt = "Create a function that adds two numbers"
    result = func.generate(prompt, call=True, a=5, b=3)
    assert result == 8

def test_invalid_provider():
    with pytest.raises(ValueError):
        func.initialize(provider="invalid_provider")

def test_missing_api_key():
    with pytest.raises(ValueError):
        func.initialize(provider="openai", api_key=None)
