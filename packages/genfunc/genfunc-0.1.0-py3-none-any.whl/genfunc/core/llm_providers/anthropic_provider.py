import logging
from typing import Optional

from anthropic import Anthropic

from .base import BaseLLMProvider


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude implementation of LLM provider"""
    
    DEFAULT_MODEL = "claude-3-haiku-20240307"
    
    def initialize(self, api_key: str, **kwargs) -> None:
        self.client = Anthropic(api_key=api_key)
        self.model = kwargs.get('model', self.DEFAULT_MODEL)
        logging.info(f"Anthropic provider initialized with model {self.model}")
    
    def generate_function(self, prompt: str) -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": f"Create a Python function that does the following: {prompt}. Provide only the import statements and the function code without any explanation or markdown formatting. For example:\nInput:\nCreate a Python function that adds two numbers.\nOutput:\ndef add_two_numbers(num1, num2):\n    return num1 + num2"
                }]
            )
            return response.content[0].text.strip()
        except Exception as e:
            logging.error(f"Error generating function with Anthropic: {str(e)}")
            raise
