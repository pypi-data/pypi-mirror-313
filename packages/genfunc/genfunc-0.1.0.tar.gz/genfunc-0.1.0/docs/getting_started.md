# Getting Started with func

## Introduction
func is a Python package that leverages Large Language Models (LLMs) to automatically generate, store, and execute Python functions. This guide will help you get started with using func in your projects.

## Installation

```bash
pip install genfunc
```

## Basic Configuration

1. Set up your API keys (atleast one):

```bash
# Option 1: Environment variables
export OPENAI_API_KEY=your_openai_api_key
export ANTHROPIC_API_KEY=your_anthropic_api_key

# Option 2: .env file
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

2. Initialize func:

```python
from genfunc import func

# Initialize with OpenAI
func.initialize(provider="openai")

# Or initialize with Anthropic
func.initialize(provider="anthropic")
```

## Basic Usage

### Generate a Function

```python
# Generate without calling
func.generate("Create a function that calculates the factorial of a number")

# Generate and call immediately
result = func.generate(
    "Create a function that adds two numbers",
    call=True,
    a=5,
    b=3
)
```

## Next Steps
- Explore [Advanced Usage](advanced_usage.md)
- Check out [Examples](examples.md)