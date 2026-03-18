from google import genai
from google.genai import types
from prompts.prompts import system_prompt
from call_function.call_function import available_functions
from config import MAX_ITERATIONS
from .base import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):
    """
    Gemini LLM provider using Google's genai SDK.
    """

    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def generate(self, messages):
        return self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
            ),
        )
    