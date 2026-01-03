"""
Provider configuration definitions

Maps provider names to environment variables and configuration options.
Based on next-ai-draw-io provider system.
"""

from typing import Dict, Optional, Literal
from dataclasses import dataclass


# Type definition for supported providers
ProviderName = Literal[
    "openai",
    "anthropic",
    "google",
    "azure",
    "bedrock",
    "ollama",
    "openrouter",
    "deepseek",
    "siliconflow",
    "nvidia",  # Keep existing NVIDIA support
]


@dataclass
class ProviderConfig:
    """Configuration for an AI provider"""
    
    name: str
    env_var: Optional[str]  # Environment variable for API key (None if no auth needed)
    base_url_var: Optional[str] = None  # Environment variable for custom endpoint
    supports_reasoning: bool = False  # Supports reasoning/thinking modes
    supports_streaming: bool = True  # Supports streaming responses
    supports_tools: bool = True  # Supports function/tool calling
    requires_additional_config: bool = False  # Needs extra config beyond API key


# Provider configuration mapping
PROVIDER_CONFIGS: Dict[str, ProviderConfig] = {
    "openai": ProviderConfig(
        name="openai",
        env_var="OPENAI_API_KEY",
        base_url_var="OPENAI_BASE_URL",
        supports_reasoning=True,  # o1, o3, gpt-5
        supports_streaming=True,
        supports_tools=True,
    ),
    "anthropic": ProviderConfig(
        name="anthropic",
        env_var="ANTHROPIC_API_KEY",
        base_url_var="ANTHROPIC_BASE_URL",
        supports_reasoning=True,  # Extended thinking
        supports_streaming=True,
        supports_tools=True,
    ),
    "google": ProviderConfig(
        name="google",
        env_var="GOOGLE_GENERATIVE_AI_API_KEY",
        base_url_var="GOOGLE_BASE_URL",
        supports_reasoning=True,  # Gemini 2.5/3.0
        supports_streaming=True,
        supports_tools=True,
    ),
    "azure": ProviderConfig(
        name="azure",
        env_var="AZURE_API_KEY",
        base_url_var="AZURE_BASE_URL",
        supports_reasoning=True,
        supports_streaming=True,
        supports_tools=True,
        requires_additional_config=True,  # Needs AZURE_RESOURCE_NAME or baseURL
    ),
    "bedrock": ProviderConfig(
        name="bedrock",
        env_var=None,  # Uses AWS credentials or IAM role
        supports_reasoning=True,  # Claude/Nova via Bedrock
        supports_streaming=True,
        supports_tools=True,
        requires_additional_config=True,  # AWS region, credentials
    ),
    "ollama": ProviderConfig(
        name="ollama",
        env_var=None,  # No authentication needed
        base_url_var="OLLAMA_BASE_URL",
        supports_reasoning=False,
        supports_streaming=True,
        supports_tools=True,
    ),
    "openrouter": ProviderConfig(
        name="openrouter",
        env_var="OPENROUTER_API_KEY",
        base_url_var="OPENROUTER_BASE_URL",
        supports_reasoning=False,
        supports_streaming=True,
        supports_tools=True,
    ),
    "deepseek": ProviderConfig(
        name="deepseek",
        env_var="DEEPSEEK_API_KEY",
        base_url_var="DEEPSEEK_BASE_URL",
        supports_reasoning=True,  # DeepSeek R1
        supports_streaming=True,
        supports_tools=True,
    ),
    "siliconflow": ProviderConfig(
        name="siliconflow",
        env_var="SILICONFLOW_API_KEY",
        base_url_var="SILICONFLOW_BASE_URL",
        supports_reasoning=False,
        supports_streaming=True,
        supports_tools=True,
    ),
    "nvidia": ProviderConfig(
        name="nvidia",
        env_var="NVIDIA_API_KEY",
        base_url_var="NVIDIA_BASE_URL",
        supports_reasoning=False,
        supports_streaming=True,
        supports_tools=True,
    ),
}


# Default base URLs for providers
DEFAULT_BASE_URLS: Dict[str, str] = {
    "anthropic": "https://api.anthropic.com/v1",
    "siliconflow": "https://api.siliconflow.com/v1",
    "ollama": "http://localhost:11434",
    "nvidia": "https://integrate.api.nvidia.com/v1",
}


# Models that support reasoning/thinking
REASONING_MODELS = {
    "openai": ["o1", "o3", "o4", "gpt-5"],
    "anthropic": ["claude-3-5-sonnet", "claude-3-opus", "claude-4"],
    "google": ["gemini-2", "gemini-3"],
    "bedrock": ["anthropic.claude", "amazon.nova"],
    "deepseek": ["deepseek-r1", "deepseek-reasoner"],
}


def get_provider_config(provider: str) -> ProviderConfig:
    """
    Get configuration for a provider
    
    Args:
        provider: Provider name
        
    Returns:
        ProviderConfig object
        
    Raises:
        ValueError: If provider is not supported
    """
    if provider not in PROVIDER_CONFIGS:
        supported = ", ".join(PROVIDER_CONFIGS.keys())
        raise ValueError(
            f"Unsupported provider: {provider}. "
            f"Supported providers: {supported}"
        )
    return PROVIDER_CONFIGS[provider]


def supports_reasoning(provider: str, model: str) -> bool:
    """
    Check if a model supports reasoning/thinking mode
    
    Args:
        provider: Provider name
        model: Model identifier
        
    Returns:
        True if model supports reasoning
    """
    if provider not in REASONING_MODELS:
        return False
    
    model_lower = model.lower()
    return any(
        keyword in model_lower 
        for keyword in REASONING_MODELS[provider]
    )
