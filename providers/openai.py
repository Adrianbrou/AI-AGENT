from openai import OpenAI
from prompts.prompts import system_prompt
from .base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    """
    OpenAI LLM provider using the openai SDK.

    Wraps the OpenAI chat completions API to match the BaseLLMProvider
    interface so the agent loop in main.py stays provider-agnostic.
    """

    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def generate(self, messages):
        # Convert messages from Gemini Content format to OpenAI dict format
        openai_messages = [{"role": "system", "content": system_prompt}]
        for msg in messages:
            role = msg.role if msg.role != "model" else "assistant"
            for part in msg.parts:
                if hasattr(part, "text") and part.text:
                    openai_messages.append({"role": role, "content": part.text})

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=openai_messages,
            temperature=0,
        )
        return OpenAIResponse(response)


class OpenAIResponse:
    """
    Adapter that wraps an OpenAI response to match the interface
    that main.py expects (i.e. .text and .function_calls properties).
    """

    def __init__(self, response):
        self._response = response

    @property
    def text(self):
        return self._response.choices[0].message.content

    @property
    def function_calls(self):
        # OpenAI function calling not wired up yet — returns None
        # so the agent treats every response as a final answer.
        return None

    @property
    def candidates(self):
        return []

    @property
    def usage_metadata(self):
        return None