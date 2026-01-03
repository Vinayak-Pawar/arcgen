"""
AI Provider Manager

Central manager for all AI providers with auto-detection and security features.
Supports OpenAI, Anthropic, Google, Azure, Bedrock, Ollama, and more.
"""

import os
from typing import Optional, Dict, Any, Tuple
from openai import OpenAI, AsyncOpenAI
from anthropic import Anthropic, AsyncAnthropic
import google.generativeai as genai

from .provider_config import (
    ProviderName,
    PROVIDER_CONFIGS,
    DEFAULT_BASE_URLS,
    get_provider_config,
    supports_reasoning,
)
from .security import validate_custom_endpoint, validate_url_safety, SecurityError


class ProviderNotConfiguredError(Exception):
    """Raised when a required provider is not properly configured"""
    pass


class AIProviderManager:
    """
    Manages AI provider initialization and configuration
    
    Features:
    - Auto-detection of configured providers
    - Security validation (SSRF protection)
    - Support for 10+ providers
    - Reasoning/thinking mode support
    - Client-side API key override
    
    Usage:
        manager = AIProviderManager()
        
        # Auto-detect provider
        client = manager.get_client()
        
        # Specific provider
        client = manager.get_client(provider="openai", model="gpt-4")
        
        # With custom config (e.g., user's own API key)
        client = manager.get_client(
            provider="anthropic",
            model="claude-3-5-sonnet",
            overrides={"api_key": "user-key", "base_url": "https://custom.com"}
        )
    """
    
    def __init__(self):
        self._clients: Dict[str, Any] = {}
    
    def detect_provider(self) -> Optional[str]:
        """
        Auto-detect configured provider based on environment variables
        
        Returns:
            Provider name if exactly one is configured, None otherwise
            
        Example:
            >>> os.environ["OPENAI_API_KEY"] = "sk-123"
            >>> manager.detect_provider()
            'openai'
        """
        configured_providers = []
        
        for provider_name, config in PROVIDER_CONFIGS.items():
            # Skip providers that don't need API key (ollama, bedrock)
            if config.env_var is None:
                continue
            
            # Check if API key is set
            if os.getenv(config.env_var):
                # Azure needs additional configuration
                if provider_name == "azure":
                    has_base_url = bool(os.getenv("AZURE_BASE_URL"))
                    has_resource_name = bool(os.getenv("AZURE_RESOURCE_NAME"))
                    if has_base_url or has_resource_name:
                        configured_providers.append(provider_name)
                else:
                    configured_providers.append(provider_name)
        
        # Return provider only if exactly one is configured
        if len(configured_providers) == 1:
            return configured_providers[0]
        
        return None
    
    def validate_provider_credentials(self, provider: str) -> None:
        """
        Validate that required credentials are present for a provider
        
        Args:
            provider: Provider name
            
        Raises:
            ProviderNotConfiguredError: If credentials are missing
        """
        config = get_provider_config(provider)
        
        # Check API key if required
        if config.env_var and not os.getenv(config.env_var):
            raise ProviderNotConfiguredError(
                f"{config.env_var} environment variable is required for {provider} provider. "
                f"Please set it in your .env file."
            )
        
        # Azure-specific validation
        if provider == "azure":
            has_base_url = bool(os.getenv("AZURE_BASE_URL"))
            has_resource_name = bool(os.getenv("AZURE_RESOURCE_NAME"))
            if not (has_base_url or has_resource_name):
                raise ProviderNotConfiguredError(
                    "Azure requires either AZURE_BASE_URL or AZURE_RESOURCE_NAME to be set."
                )
    
    def get_client(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        overrides: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Any, Dict[str, Any]]:
        """
        Get AI client for the specified provider
        
        Args:
            provider: Provider name (auto-detected if None)
            model: Model identifier
            overrides: Client overrides (api_key, base_url, etc.)
            
        Returns:
            Tuple of (client object, metadata dict)
            
        Raises:
            SecurityError: If SSRF protection fails
            ProviderNotConfiguredError: If provider not configured
            ValueError: If provider is invalid
            
        Example:
            >>> client, meta = manager.get_client("openai", "gpt-4")
            >>> response = client.chat.completions.create(...)
        """
        overrides = overrides or {}
        
        # SECURITY: Validate custom endpoint before proceeding
        if overrides.get("base_url"):
            validate_custom_endpoint(
                overrides.get("base_url"),
                overrides.get("api_key"),
                provider or "unknown"
            )
            
            # Additional URL safety check
            if not validate_url_safety(overrides["base_url"]):
                raise SecurityError(
                    f"Invalid or unsafe URL: {overrides['base_url']}"
                )
        
        # Determine provider
        if not provider:
            # Try environment variable first
            provider = os.getenv("ARCGEN_LLM_PROVIDER")
            
            # Try auto-detection
            if not provider:
                provider = self.detect_provider()
            
            if not provider:
                raise ProviderNotConfiguredError(
                    "No AI provider configured. Please set ARCGEN_LLM_PROVIDER "
                    "and the corresponding API key in your .env file."
                )
        
        # Validate provider exists
        get_provider_config(provider)  # Will raise ValueError if invalid
        
        # Validate credentials (unless client is providing their own)
        if not overrides.get("api_key"):
            self.validate_provider_credentials(provider)
        
        # Get client for specific provider
        if provider == "openai":
            return self._get_openai_client(model, overrides)
        elif provider == "anthropic":
            return self._get_anthropic_client(model, overrides)
        elif provider == "google":
            return self._get_google_client(model, overrides)
        elif provider == "azure":
            return self._get_azure_client(model, overrides)
        elif provider == "ollama":
            return self._get_ollama_client(model, overrides)
        elif provider == "deepseek":
            return self._get_deepseek_client(model, overrides)
        elif provider == "nvidia":
            return self._get_nvidia_client(model, overrides)
        else:
            # Generic OpenAI-compatible client
            return self._get_generic_client(provider, model, overrides)
    
    def _get_openai_client(
        self,
        model: Optional[str],
        overrides: Dict[str, Any]
    ) -> Tuple[OpenAI, Dict[str, Any]]:
        """Get OpenAI client"""
        api_key = overrides.get("api_key") or os.getenv("OPENAI_API_KEY")
        base_url = overrides.get("base_url") or os.getenv("OPENAI_BASE_URL")
        
        client = OpenAI(
            api_key=api_key,
            base_url=base_url if base_url else None,
        )
        
        metadata = {
            "provider": "openai",
            "model": model or "gpt-4",
            "supports_reasoning": supports_reasoning("openai", model or ""),
            "supports_tools": True,
            "supports_streaming": True,
        }
        
        return client, metadata
    
    def _get_anthropic_client(
        self,
        model: Optional[str],
        overrides: Dict[str, Any]
    ) -> Tuple[Anthropic, Dict[str, Any]]:
        """Get Anthropic client"""
        api_key = overrides.get("api_key") or os.getenv("ANTHROPIC_API_KEY")
        base_url = overrides.get("base_url") or os.getenv("ANTHROPIC_BASE_URL") or DEFAULT_BASE_URLS["anthropic"]
        
        client = Anthropic(
            api_key=api_key,
            base_url=base_url,
        )
        
        metadata = {
            "provider": "anthropic",
            "model": model or "claude-3-5-sonnet-20241022",
            "supports_reasoning": supports_reasoning("anthropic", model or ""),
            "supports_tools": True,
            "supports_streaming": True,
        }
        
        return client, metadata
    
    def _get_google_client(
        self,
        model: Optional[str],
        overrides: Dict[str, Any]
    ) -> Tuple[Any, Dict[str, Any]]:
        """Get Google Gemini client"""
        api_key = overrides.get("api_key") or os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
        
        genai.configure(api_key=api_key)
        
        # Google uses a different pattern - return the module with metadata
        metadata = {
            "provider": "google",
            "model": model or "gemini-2.0-flash-exp",
            "supports_reasoning": supports_reasoning("google", model or ""),
            "supports_tools": True,
            "supports_streaming": True,
        }
        
        return genai, metadata
    
    def _get_azure_client(
        self,
        model: Optional[str],
        overrides: Dict[str, Any]
    ) -> Tuple[OpenAI, Dict[str, Any]]:
        """Get Azure OpenAI client"""
        from openai import AzureOpenAI
        
        api_key = overrides.get("api_key") or os.getenv("AZURE_API_KEY")
        base_url = overrides.get("base_url") or os.getenv("AZURE_BASE_URL")
        azure_endpoint = os.getenv("AZURE_ENDPOINT")
        api_version = os.getenv("AZURE_API_VERSION", "2024-02-15-preview")
        
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint or base_url,
        )
        
        metadata = {
            "provider": "azure",
            "model": model or "gpt-4",
            "supports_reasoning": True,
            "supports_tools": True,
            "supports_streaming": True,
        }
        
        return client, metadata
    
    def _get_ollama_client(
        self,
        model: Optional[str],
        overrides: Dict[str, Any]
    ) -> Tuple[OpenAI, Dict[str, Any]]:
        """Get Ollama client (OpenAI-compatible)"""
        base_url = overrides.get("base_url") or os.getenv("OLLAMA_BASE_URL") or DEFAULT_BASE_URLS["ollama"]
        
        client = OpenAI(
            api_key="ollama",  # Ollama doesn't use API keys
            base_url=f"{base_url}/v1",
        )
        
        metadata = {
            "provider": "ollama",
            "model": model or "llama2",
            "supports_reasoning": False,
            "supports_tools": True,
            "supports_streaming": True,
        }
        
        return client, metadata
    
    def _get_deepseek_client(
        self,
        model: Optional[str],
        overrides: Dict[str, Any]
    ) -> Tuple[OpenAI, Dict[str, Any]]:
        """Get DeepSeek client (OpenAI-compatible)"""
        api_key = overrides.get("api_key") or os.getenv("DEEPSEEK_API_KEY")
        base_url = overrides.get("base_url") or os.getenv("DEEPSEEK_BASE_URL") or "https://api.deepseek.com"
        
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        
        metadata = {
            "provider": "deepseek",
            "model": model or "deepseek-chat",
            "supports_reasoning": supports_reasoning("deepseek", model or ""),
            "supports_tools": True,
            "supports_streaming": True,
        }
        
        return client, metadata
    
    def _get_nvidia_client(
        self,
        model: Optional[str],
        overrides: Dict[str, Any]
    ) -> Tuple[OpenAI, Dict[str, Any]]:
        """Get NVIDIA NIM client (OpenAI-compatible)"""
        api_key = overrides.get("api_key") or os.getenv("NVIDIA_API_KEY")
        base_url = overrides.get("base_url") or os.getenv("NVIDIA_BASE_URL") or DEFAULT_BASE_URLS["nvidia"]
        
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        
        metadata = {
            "provider": "nvidia",
            "model": model or "meta/llama-3.1-70b-instruct",
            "supports_reasoning": False,
            "supports_tools": True,
            "supports_streaming": True,
        }
        
        return client, metadata
    
    def _get_generic_client(
        self,
        provider: str,
        model: Optional[str],
        overrides: Dict[str, Any]
    ) -> Tuple[OpenAI, Dict[str, Any]]:
        """Get generic OpenAI-compatible client"""
        config = get_provider_config(provider)
        
        api_key = overrides.get("api_key")
        if not api_key and config.env_var:
            api_key = os.getenv(config.env_var)
        
        base_url = overrides.get("base_url")
        if not base_url and config.base_url_var:
            base_url = os.getenv(config.base_url_var)
        if not base_url and provider in DEFAULT_BASE_URLS:
            base_url = DEFAULT_BASE_URLS[provider]
        
        client = OpenAI(
            api_key=api_key or "placeholder",
            base_url=base_url,
        )
        
        metadata = {
            "provider": provider,
            "model": model or "default",
            "supports_reasoning": config.supports_reasoning,
            "supports_tools": config.supports_tools,
            "supports_streaming": config.supports_streaming,
        }
        
        return client, metadata
