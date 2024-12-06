import logging
from typing import Optional

import openai

from .base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    """OpenAI implementation of LLM provider"""
    
    DEFAULT_MODEL = "gpt-4"
    
    def initialize(self, api_key: str, **kwargs) -> None:
        self.client = openai.OpenAI(api_key=api_key)
        self.model = kwargs.get('model', self.DEFAULT_MODEL)
        logging.info(f"OpenAI provider initialized with model {self.model}")
    
    def generate_function(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a Python expert. Respond ONLY with the Python code in plain text. Do not use markdown formatting, code blocks, or explanations. Ensure the code has correct indentation."},
                    {"role": "user", "content": f"Write a Python function to {prompt}. For example:\nInput:\nCreate a Python function that adds two numbers.\nOutput:\ndef add_two_numbers(num1, num2):\n    return num1 + num2"}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"Error generating function with OpenAI: {str(e)}")
            raise
