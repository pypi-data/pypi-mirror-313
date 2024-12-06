import ast
import logging
from typing import Optional
import textwrap

def sanitize_function_name(code: str, default:str='helpers', output_path: Optional[str]=None) -> tuple[str, Optional[str]]:
    """
    Extract and sanitize function name from the provided code string.
    This function parses the given code to find the first function definition
    (either regular or asynchronous) and returns its name. If no function
    definition is found, it returns a default name. Optionally, it can also
    return an output path if the default name is used.

    Args:
        code (str): The code string to parse and extract the function name from.
        default (str, optional): The default function name to return if no function
            definition is found. Defaults to 'helpers'.
        output_path (Optional[str], optional): The output path to return if the
            default name is used. Defaults to None.

    Returns
        tuple: A tuple containing the function name and the output path. 
            The output path is None if a function name is found.
    """
    try:
        # Dedent the code to handle various indentation styles
        code = textwrap.dedent(code)
        tree = ast.parse(code)
        for node in ast.walk(tree):
            # Check for both regular and async function definitions
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return node.name, None
        return default, output_path
    except Exception as e:
        logging.error(f"Error parsing function code: {str(e)}, using {default}.py")
        return default, output_path

# def validate_python_code(code: str) -> bool:
#     """Validate that the generated code is valid Python"""
#     try:
#         ast.parse(code)
#         return True
#     except SyntaxError:
#         return False

def clean_markdown_code_block(text):
    """
    Removes leading and trailing markdown code block tags (``` and ```python).

    Args:
        text (str): The input text to clean.

    Returns:
        str: The cleaned text without markdown code block tags.
    """
    lines = text.strip().splitlines()
    
    # Remove the first line if it starts with ``` or ```python
    if lines and (lines[0].startswith("```") or lines[0].startswith("```python")):
        lines.pop(0)
    
    # Remove the last line if it is ```
    if lines and lines[-1].strip() == "```":
        lines.pop()
    
    return "\n".join(lines)