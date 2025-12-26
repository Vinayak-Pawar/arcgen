"""
LLM Provider Configuration for Arcgen

Similar to Google Colab's userdata.get('secretName') approach,
users can set environment variables for their API keys.

Supported providers:
- openai: OpenAI GPT models
- anthropic: Anthropic Claude models
- google: Google Gemini models
- nvidia: NVIDIA NIM (current default)
- ollama: Local Ollama models
- custom: Custom OpenAI-compatible endpoints
"""

import os
from typing import Dict, Optional
from pydantic import BaseModel, Field
from enum import Enum


class LLMProvider(str, Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    NVIDIA = "nvidia"
    OLLAMA = "ollama"
    CUSTOM = "custom"


class LLMConfig(BaseModel):
    """Configuration for an LLM provider"""
    provider: LLMProvider
    model: str
    api_key_env: str  # Environment variable name for the API key
    base_url: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 2048
    top_p: float = 0.7


# Default configurations for each provider
DEFAULT_CONFIGS = {
    LLMProvider.OPENAI: LLMConfig(
        provider=LLMProvider.OPENAI,
        model="gpt-4",
        api_key_env="OPENAI_API_KEY",
        base_url="https://api.openai.com/v1",
    ),
    LLMProvider.ANTHROPIC: LLMConfig(
        provider=LLMProvider.ANTHROPIC,
        model="claude-3-sonnet-20240229",
        api_key_env="ANTHROPIC_API_KEY",
        base_url="https://api.anthropic.com",
    ),
    LLMProvider.GOOGLE: LLMConfig(
        provider=LLMProvider.GOOGLE,
        model="gemini-pro",
        api_key_env="GOOGLE_API_KEY",
        base_url="https://generativelanguage.googleapis.com",
    ),
    LLMProvider.NVIDIA: LLMConfig(
        provider=LLMProvider.NVIDIA,
        model="meta/llama-3.1-70b-instruct",
        api_key_env="NVIDIA_API_KEY",
        base_url="https://integrate.api.nvidia.com/v1",
    ),
    LLMProvider.OLLAMA: LLMConfig(
        provider=LLMProvider.OLLAMA,
        model="llama2",
        api_key_env="",  # No API key needed for local Ollama
        base_url="http://localhost:11434/v1",
    ),
    LLMProvider.CUSTOM: LLMConfig(
        provider=LLMProvider.CUSTOM,
        model="custom-model",
        api_key_env="CUSTOM_API_KEY",
        base_url="https://your-custom-endpoint.com/v1",
    ),
}


def get_user_llm_config() -> LLMConfig:
    """
    Get the user's configured LLM provider, similar to Google Colab's userdata.get()

    Users can set these environment variables:
    - ARCGEN_LLM_PROVIDER: Which provider to use (openai, anthropic, google, nvidia, ollama, custom)
    - Provider-specific API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.)
    - ARCGEN_LLM_MODEL: Override the default model
    - ARCGEN_CUSTOM_BASE_URL: For custom providers
    """

    # Get provider from environment (default to nvidia for backward compatibility)
    provider_str = os.getenv("ARCGEN_LLM_PROVIDER", "nvidia").lower()
    try:
        provider = LLMProvider(provider_str)
    except ValueError:
        print(f"Warning: Invalid LLM provider '{provider_str}', falling back to nvidia")
        provider = LLMProvider.NVIDIA

    # Get base config
    config = DEFAULT_CONFIGS[provider].copy()

    # Allow model override
    if model_override := os.getenv("ARCGEN_LLM_MODEL"):
        config.model = model_override

    # Allow base URL override (useful for custom providers)
    if base_url_override := os.getenv("ARCGEN_CUSTOM_BASE_URL"):
        config.base_url = base_url_override

    # Allow temperature override
    if temp_override := os.getenv("ARCGEN_LLM_TEMPERATURE"):
        try:
            config.temperature = float(temp_override)
        except ValueError:
            print(f"Warning: Invalid temperature '{temp_override}', using default")

    return config


def get_api_key(config: LLMConfig) -> Optional[str]:
    """
    Get API key for the configured provider, similar to Google Colab's userdata.get()

    Users set environment variables like:
    - OPENAI_API_KEY=sk-your-key-here
    - ANTHROPIC_API_KEY=your-anthropic-key
    """
    if not config.api_key_env:
        return None  # No API key needed (like Ollama)

    api_key = os.getenv(config.api_key_env)
    if not api_key:
        raise ValueError(f"API key not found. Please set {config.api_key_env} environment variable.")

    return api_key


def list_available_providers() -> Dict[str, Dict]:
    """
    Return information about all available providers for the frontend UI
    """
    return {
        provider.value: {
            "name": provider.value.title(),
            "default_model": DEFAULT_CONFIGS[provider].model,
            "requires_api_key": bool(DEFAULT_CONFIGS[provider].api_key_env),
            "api_key_env": DEFAULT_CONFIGS[provider].api_key_env,
            "description": get_provider_description(provider)
        }
        for provider in LLMProvider
    }


def get_provider_description(provider: LLMProvider) -> str:
    """Get human-readable description for each provider"""
    descriptions = {
        LLMProvider.OPENAI: "OpenAI GPT models (GPT-4, GPT-3.5)",
        LLMProvider.ANTHROPIC: "Anthropic Claude models (most capable for complex reasoning)",
        LLMProvider.GOOGLE: "Google Gemini models (fast and cost-effective)",
        LLMProvider.NVIDIA: "NVIDIA NIM API (current default, optimized for AI workloads)",
        LLMProvider.OLLAMA: "Local Ollama models (run models on your own machine)",
        LLMProvider.CUSTOM: "Custom OpenAI-compatible API endpoints"
    }
    return descriptions.get(provider, "Unknown provider")


# Google Colab style helper functions
def get_secret(secret_name: str) -> Optional[str]:
    """
    Google Colab style function to get secrets
    Usage: api_key = get_secret('OPENAI_API_KEY')
    """
    return os.getenv(secret_name)


def set_secret(secret_name: str, value: str):
    """
    Google Colab style function to set secrets
    Note: In production, this would need secure storage
    """
    os.environ[secret_name] = value
    print(f"Secret '{secret_name}' has been set (this is not persistent in production)")


# Export the main configuration
llm_config = get_user_llm_config()
