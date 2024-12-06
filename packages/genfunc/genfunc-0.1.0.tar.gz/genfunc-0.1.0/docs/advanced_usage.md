# Advanced Usage

## Provider Configuration

### OpenAI Configuration

```python
func.initialize(
    provider="openai",
    api_key="your_api_key",
    model="gpt-4",  # Specify model version
)
```

### Anthropic Configuration

```python
func.initialize(
    provider="anthropic",
    api_key="your_api_key",
    model="claude-3-5-haiku-latest"  # Specify model version
)
```

## Function Management

### Accessing Generated Functions

All generated functions are stored in the `./helpers/` directory. You can:

1. Import them directly:
```python
from helpers.your_function import your_function
```

2. Modify them manually:
```python
# Edit the file in ./helpers/generated_function.py
```

### Function Naming

Functions are automatically named based on their purpose. You can find them in:
```
./helpers/
├── add_numbers.py
├── calculate_factorial.py
└── process_data.py
```

## Logging

```python
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Now you'll see detailed logs
func.generate("Create a function...")
```

## Best Practices

1. **Clear Prompts**: Write clear, specific prompts for better results
2. **Validation**: Always validate generated functions before production use
3. **Version Control**: Track generated functions in version control
4. **Error Handling**: Implement proper error handling for production use
5. **Testing**: Test generated functions thoroughly