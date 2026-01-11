"""
LLM Provider abstraction layer.
Supports: OpenAI, Anthropic (Claude), Ollama, vLLM, and OpenAI-compatible APIs.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import os


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    @abstractmethod
    def chat(self, messages: List[Dict], max_tokens: int = 500, temperature: float = 0.7) -> str:
        """Send messages and get response"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI API provider (GPT-4, GPT-3.5, etc.)"""

    def __init__(self, api_key: str, model: str = "gpt-4o", base_url: Optional[str] = None):
        from openai import OpenAI
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

    def chat(self, messages: List[Dict], max_tokens: int = 500, temperature: float = 0.7) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()

    @property
    def name(self) -> str:
        return f"OpenAI ({self.model})"


class AnthropicProvider(LLMProvider):
    """Anthropic API provider (Claude)"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        from anthropic import Anthropic
        self.model = model
        self.client = Anthropic(api_key=api_key)

    def chat(self, messages: List[Dict], max_tokens: int = 500, temperature: float = 0.7) -> str:
        # Extract system message if present
        system_content = ""
        chat_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system_content += msg["content"] + "\n"
            else:
                chat_messages.append(msg)

        # Ensure messages alternate between user and assistant
        if not chat_messages:
            chat_messages = [{"role": "user", "content": "Please respond."}]

        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_content.strip() if system_content else None,
            messages=chat_messages
        )
        return response.content[0].text.strip()

    @property
    def name(self) -> str:
        return f"Anthropic ({self.model})"


class OllamaProvider(LLMProvider):
    """Ollama local provider"""

    def __init__(self, model: str = "llama3.1", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url.rstrip("/")

    def chat(self, messages: List[Dict], max_tokens: int = 500, temperature: float = 0.7) -> str:
        import requests

        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": temperature
                }
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()["message"]["content"].strip()

    @property
    def name(self) -> str:
        return f"Ollama ({self.model})"


class VLLMProvider(LLMProvider):
    """vLLM provider (OpenAI-compatible API)"""

    def __init__(self, model: str, base_url: str = "http://localhost:8000/v1", api_key: str = "EMPTY"):
        from openai import OpenAI
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def chat(self, messages: List[Dict], max_tokens: int = 500, temperature: float = 0.7) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()

    @property
    def name(self) -> str:
        return f"vLLM ({self.model})"


class OpenAICompatibleProvider(LLMProvider):
    """Generic OpenAI-compatible API provider (LM Studio, LocalAI, etc.)"""

    def __init__(self, model: str, base_url: str, api_key: str = "EMPTY"):
        from openai import OpenAI
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def chat(self, messages: List[Dict], max_tokens: int = 500, temperature: float = 0.7) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()

    @property
    def name(self) -> str:
        return f"OpenAI-Compatible ({self.model})"


def get_llm_provider() -> LLMProvider:
    """
    Factory function to create LLM provider based on environment configuration.

    Environment variables:
        LLM_PROVIDER: openai, anthropic, ollama, vllm, openai-compatible
        LLM_MODEL: Model name (default varies by provider)
        LLM_BASE_URL: Base URL for API (optional for some providers)

        Provider-specific:
        OPENAI_API_KEY: For OpenAI
        ANTHROPIC_API_KEY: For Anthropic/Claude
    """
    provider_type = os.getenv("LLM_PROVIDER", "openai").lower()
    model = os.getenv("LLM_MODEL")
    base_url = os.getenv("LLM_BASE_URL")

    if provider_type == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required for OpenAI provider")
        return OpenAIProvider(
            api_key=api_key,
            model=model or "gpt-4o",
            base_url=base_url
        )

    elif provider_type == "anthropic" or provider_type == "claude":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required for Anthropic provider")
        return AnthropicProvider(
            api_key=api_key,
            model=model or "claude-sonnet-4-20250514"
        )

    elif provider_type == "ollama":
        return OllamaProvider(
            model=model or "llama3.1",
            base_url=base_url or "http://localhost:11434"
        )

    elif provider_type == "vllm":
        if not model:
            raise ValueError("LLM_MODEL environment variable is required for vLLM provider")
        return VLLMProvider(
            model=model,
            base_url=base_url or "http://localhost:8000/v1",
            api_key=os.getenv("OPENAI_API_KEY", "EMPTY")
        )

    elif provider_type == "openai-compatible":
        if not model:
            raise ValueError("LLM_MODEL environment variable is required for OpenAI-compatible provider")
        if not base_url:
            raise ValueError("LLM_BASE_URL environment variable is required for OpenAI-compatible provider")
        return OpenAICompatibleProvider(
            model=model,
            base_url=base_url,
            api_key=os.getenv("OPENAI_API_KEY", "EMPTY")
        )

    else:
        raise ValueError(f"Unknown LLM provider: {provider_type}. "
                        f"Supported: openai, anthropic, ollama, vllm, openai-compatible")


# Global provider instance (lazy loaded)
_provider: Optional[LLMProvider] = None


def get_provider() -> LLMProvider:
    """Get or create the global LLM provider instance"""
    global _provider
    if _provider is None:
        _provider = get_llm_provider()
    return _provider


def chat(messages: List[Dict], max_tokens: int = 500, temperature: float = 0.7) -> str:
    """Convenience function to chat using the configured provider"""
    return get_provider().chat(messages, max_tokens, temperature)
