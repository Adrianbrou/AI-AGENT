from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """
    Abstract base class for LLM providers.

    All providers must implement generate() with the same signature
    so the agent loop in main.py stays provider-agnostic.
    """

    @abstractmethod
    def generate(self, messages):
        """
        Send messages to the LLM and return a response object.

        Args:
            messages (list): Conversation history as a list of Content objects.

        Returns:
            A response object with .text and .function_calls properties.
        """
        pass