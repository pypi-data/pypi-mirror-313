import pytest
from genfunc.core.utils import sanitize_function_name, validate_python_code

def test_sanitize_function_name():
    # Test valid function code
    code = """
def add_numbers(a, b):
    return a + b
"""
    assert sanitize_function_name(code) == ("add_numbers", None)
    
    # Test function with decorators
    code = """
@decorator
def some_function():
    pass
"""
    assert sanitize_function_name(code) == ("some_function", None)
    
    # Test invalid code
    code = "not a function"
    assert sanitize_function_name(code) == ("helpers", None)
    
    # Test multiple functions (should return first function name)
    code = """
def first_function():
    pass
    
def second_function():
    pass
"""
    assert sanitize_function_name(code) == ("first_function", None)

    # Test function with import statements
    code = """
import math
from typing import List

def calculate_circle_area():
    return math.pi * radius * radius
"""
    assert sanitize_function_name(code) == ("calculate_circle_area", None)

    # Test with custom output path
    code = "invalid code"
    output_path = "./custom/path"
    assert sanitize_function_name(code, "default", output_path) == ("default", output_path)

    # Test function with type annotations
    code = """
def typed_function(a: int, b: str) -> bool:
    return True
"""
    assert sanitize_function_name(code) == ("typed_function", None)

    # Test function with complex type annotations
    code = """
from typing import List, Dict, Optional, Union
def complex_types(
    a: List[int],
    b: Dict[str, Union[int, str]],
    c: Optional[bool] = None
) -> Optional[List[Dict[str, Any]]]:
    return None
"""
    assert sanitize_function_name(code) == ("complex_types", None)

    # Test function with *args and **kwargs
    code = """
def variadic_func(*args: tuple[int, ...], **kwargs: dict[str, Any]) -> None:
    pass
"""
    assert sanitize_function_name(code) == ("variadic_func", None)

    # Test async function with type annotations
    code = """
async def async_typed(data: bytes, timeout: float = 1.0) -> Coroutine[Any, Any, str]:
    return 'done'
"""
    assert sanitize_function_name(code) == ("async_typed", None)

    # Mega test combining all elements
    code = """
import math, asyncio
from typing import (
    List, Dict, Optional, Union, Any, 
    Callable, Coroutine, TypeVar, Generic
)
from dataclasses import dataclass
from abc import ABC, abstractmethod

T = TypeVar('T')

@dataclass
class Config:
    value: int

@staticmethod
@abstractmethod
@property
async def mega_boss_function(
    required_arg: int,
    optional_arg: str = "default",
    *args: tuple[int, ...],
    config: Optional[Config] = None,
    complex_type: Dict[str, List[Union[int, str]]] = None,
    callback: Callable[[int], Coroutine[Any, Any, T]] = None,
    **kwargs: dict[str, Any]
) -> Union[Coroutine[Any, Any, List[Dict[str, Optional[T]]]], None]:
    '''
    This is a docstring with multiple lines
    that includes all possible Python features
    '''
    try:
        async with contextlib.asynccontextmanager() as ctx:
            result = await callback(
                required_arg + sum(args)
            )
    except Exception as e:
        raise ValueError("Complex error") from e
    finally:
        return result
"""
    assert sanitize_function_name(code) == ("mega_boss_function", None)

def test_validate_python_code():
    # Test valid code
    valid_code = """
def test_function():
    return "Hello, World!"
"""
    assert validate_python_code(valid_code) is True
    
    # Test invalid syntax
    invalid_code = """
def broken_function()
    return "Missing colon"
"""
    assert validate_python_code(invalid_code) is False
    
    # Test empty code
    assert validate_python_code("") is True
    
    # Test code with invalid indentation
    invalid_indentation = """
def test_function():
return "Bad indentation"
"""
    assert validate_python_code(invalid_indentation) is False
    
    # Test code with valid complex syntax
    complex_code = """
@decorator
def complex_function(a: int, b: str = "default") -> dict:
    try:
        result = {"success": True}
    except Exception as e:
        raise ValueError("Something went wrong")
    finally:
        return result
"""
    assert validate_python_code(complex_code) is True
