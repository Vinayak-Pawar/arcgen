"""
Test suite for AI provider system

Tests provider manager, security features, and auto-detection.
"""

import os
import pytest
from unittest.mock import patch, MagicMock

from backend.ai_providers import AIProviderManager, ProviderConfig
from backend.ai_providers.security import (
    validate_custom_endpoint,
    validate_url_safety,
    sanitize_library_name,
    SecurityError,
)
from backend.ai_providers.provider_config import (
    get_provider_config,
    supports_reasoning,
    PROVIDER_CONFIGS,
)


class TestSecurity:
    """Test security features"""
    
    def test_ssrf_protection_blocks_custom_url_without_key(self):
        """CRITICAL: Must block custom URL without API key"""
        with pytest.raises(SecurityError, match="API key is required"):
            validate_custom_endpoint(
                base_url="https://evil.com",
                api_key=None,
                provider_name="openai"
            )
    
    def test_ssrf_protection_allows_url_with_key(self):
        """Should allow custom URL with API key"""
        # Should not raise
        validate_custom_endpoint(
            base_url="https://custom.com",
            api_key="sk-custom-key",
            provider_name="openai"
        )
    
    def test_ssrf_protection_allows_no_customization(self):
        """Should allow default configuration"""
        # Should not raise
        validate_custom_endpoint(
            base_url=None,
            api_key=None,
            provider_name="openai"
        )
    
    def test_url_safety_requires_https(self):
        """Should reject non-HTTPS URLs"""
        assert not validate_url_safety("http://external.com")
    
    def test_url_safety_allows_localhost_http(self):
        """Should allow HTTP for localhost"""
        assert validate_url_safety("http://localhost:8000")
        assert validate_url_safety("http://127.0.0.1:8000")
    
    def test_url_safety_blocks_private_ips(self):
        """Should block private IP ranges"""
        assert not validate_url_safety("https://10.0.0.1")
        assert not validate_url_safety("https://192.168.1.1")
        assert not validate_url_safety("https://172.16.0.1")
    
    def test_library_name_sanitization(self):
        """Should sanitize library names to prevent path traversal"""
        assert sanitize_library_name("aws4") == "aws4"
        assert sanitize_library_name("../../etc/passwd") == "etcpasswd"
        assert sanitize_library_name("AWS-2.0_Beta") == "aws-2.0_beta"
        assert sanitize_library_name("cisco19") == "cisco19"


class TestProviderConfig:
    """Test provider configuration"""
    
    def test_all_providers_have_config(self):
        """All supported providers should have configuration"""
        providers = [
            "openai", "anthropic", "google", "azure",
            "bedrock", "ollama", "openrouter", "deepseek",
            "siliconflow", "nvidia"
        ]
        for provider in providers:
            config = get_provider_config(provider)
            assert config.name == provider
    
    def test_invalid_provider_raises_error(self):
        """Should reject invalid provider names"""
        with pytest.raises(ValueError, match="Unsupported provider"):
            get_provider_config("invalid_provider")
    
    def test_reasoning_detection(self):
        """Should correctly detect reasoning models"""
        # OpenAI reasoning models
        assert supports_reasoning("openai", "o1-preview")
        assert supports_reasoning("openai", "gpt-5-turbo")
        assert not supports_reasoning("openai", "gpt-4-turbo")
        
        # Anthropic reasoning models
        assert supports_reasoning("anthropic", "claude-3-5-sonnet")
        assert supports_reasoning("anthropic", "claude-4-opus")
        
        # Google reasoning models
        assert supports_reasoning("google", "gemini-2.5-pro")
        assert supports_reasoning("google", "gemini-3-flash")
        assert not supports_reasoning("google", "gemini-1.5-pro")
        
        # DeepSeek reasoning models
        assert supports_reasoning("deepseek", "deepseek-r1")
        assert not supports_reasoning("deepseek", "deepseek-chat")


class TestProviderManager:
    """Test provider manager"""
    
    @pytest.fixture
    def manager(self):
        """Create manager instance"""
        return AIProviderManager()
    
    @pytest.fixture
    def clean_env(self):
        """Clean environment variables before each test"""
        env_vars = [
            "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_GENERATIVE_AI_API_KEY",
            "AZURE_API_KEY", "DEEPSEEK_API_KEY", "NVIDIA_API_KEY",
            "ARCGEN_LLM_PROVIDER"
        ]
        original = {}
        for var in env_vars:
            original[var] = os.environ.pop(var, None)
        
        yield
        
        # Restore
        for var, value in original.items():
            if value is not None:
                os.environ[var] = value
    
    def test_auto_detection_single_provider(self, manager, clean_env):
        """Should auto-detect when exactly one provider is configured"""
        os.environ["OPENAI_API_KEY"] = "sk-test"
        
        detected = manager.detect_provider()
        assert detected == "openai"
    
    def test_auto_detection_multiple_providers(self, manager, clean_env):
        """Should return None when multiple providers are configured"""
        os.environ["OPENAI_API_KEY"] = "sk-test"
        os.environ["ANTHROPIC_API_KEY"] = "sk-ant-test"
        
        detected = manager.detect_provider()
        assert detected is None
    
    def test_auto_detection_no_providers(self, manager, clean_env):
        """Should return None when no providers are configured"""
        detected = manager.detect_provider()
        assert detected is None
    
    def test_get_client_with_explicit_provider(self, manager, clean_env):
        """Should get client for explicitly specified provider"""
        os.environ["OPENAI_API_KEY"] = "sk-test"
        
        with patch('backend.ai_providers.provider_manager.OpenAI') as mock_openai:
            mock_openai.return_value = MagicMock()
            
            client, metadata = manager.get_client(provider="openai", model="gpt-4")
            
            assert metadata["provider"] == "openai"
            assert metadata["model"] == "gpt-4"
            assert metadata["supports_tools"] is True
    
    def test_get_client_ssrf_protection(self, manager, clean_env):
        """Should enforce SSRF protection"""
        with pytest.raises(SecurityError):
            manager.get_client(
                provider="openai",
                model="gpt-4",
                overrides={"base_url": "https://evil.com"}  # Missing api_key
            )
    
    def test_get_client_with_overrides(self, manager, clean_env):
        """Should use client overrides for API key"""
        with patch('backend.ai_providers.provider_manager.OpenAI') as mock_openai:
            mock_openai.return_value = MagicMock()
            
            client, metadata = manager.get_client(
                provider="openai",
                model="gpt-4",
                overrides={
                    "api_key": "sk-user-key",
                    "base_url": "https://custom.com"
                }
            )
            
            # Should have called OpenAI with user's key
            mock_openai.assert_called_once()
            call_args = mock_openai.call_args
            assert call_args.kwargs["api_key"] == "sk-user-key"


class TestProviderIntegration:
    """Integration tests for provider system"""
    
    @pytest.fixture
    def manager(self):
        return AIProviderManager()
    
    def test_openai_client_creation(self, manager):
        """Test OpenAI client can be created (if API key available)"""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")
        
        client, metadata = manager.get_client(provider="openai", model="gpt-4")
        
        assert metadata["provider"] == "openai"
        assert metadata["supports_tools"] is True
        assert client is not None
    
    def test_anthropic_client_creation(self, manager):
        """Test Anthropic client can be created (if API key available)"""
        if not os.getenv("ANTHROPIC_API_KEY"):
            pytest.skip("ANTHROPIC_API_KEY not set")
        
        client, metadata = manager.get_client(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022"
        )
        
        assert metadata["provider"] == "anthropic"
        assert metadata["supports_reasoning"] is True
        assert client is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
