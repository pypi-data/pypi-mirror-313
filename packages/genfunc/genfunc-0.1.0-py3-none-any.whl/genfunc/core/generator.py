import importlib
import logging
from pathlib import Path
from typing import Any, Optional

from .llm_providers.base import BaseLLMProvider
from .utils import sanitize_function_name

# from .utils import validate_python_code

class FuncGenerator:
    def __init__(self, provider: BaseLLMProvider):
        self.provider = provider
        self.helpers_dir = Path('./helpers')
        self.helpers_dir.mkdir(exist_ok=True)
        
    def generate(self, prompt: str, call: bool = False, output_path: Optional[str]=None, **kwargs) -> Optional[Any]:
        """
        Generate a Python function based on the prompt and optionally call it
        
        Args:
            prompt (str): Description of the function to generate
            call (bool): Whether to call the function immediately
            output_path (Optional[str]): Custom path to save the generated function
            **kwargs: Arguments to pass to the generated function if call=True
            
        Returns:
            Optional[Any]: Result of the function call if call=True, None otherwise
        """
        try:
            # Generate the function code - modify prompt to enforce parameter names
            if kwargs:
                param_names = ', '.join(kwargs.keys())
                modified_prompt = f"{prompt} using parameters ({param_names})"
                function_code = self.provider.generate_function(modified_prompt)
            else:
                function_code = self.provider.generate_function(prompt)
            
            # Validate the generated code
            # if not validate_python_code(function_code):
            #     raise ValueError("Generated code is not valid Python")
            
            # Extract function name and get potential output path
            function_name, default_path = sanitize_function_name(function_code, output_path=output_path)
            
            if default_path is not None:
                # Function name is default, append to existing file
                target_path = Path(default_path if default_path else self.helpers_dir / "helpers.py")
                target_path.parent.mkdir(exist_ok=True)
                
                # Append newlines for spacing
                with open(target_path, 'a+') as f:
                    f.write('\n\n')
                    f.write(function_code)
                
                file_path = target_path
            else:
                # Use function name as filename
                file_path = self.helpers_dir / f"{function_name}.py"
                with open(file_path, 'w') as f:
                    f.write(function_code)
            
            logging.info(f"Generated function saved to {file_path}")
            
            if call:
                # Import and call the function
                spec = importlib.util.spec_from_file_location(function_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                function = getattr(module, function_name)
                return function(**kwargs)
            
            return None
            
        except Exception as e:
            logging.error(f"Error in generate: {str(e)}")
            raise