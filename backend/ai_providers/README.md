# AI Provider System - Implementation Guide

## Overview

Arcgen now supports **10+ AI providers** with advanced features including:
- ✅ Multi-provider support (OpenAI, Anthropic, Google, Azure, Bedrock, Ollama, etc.)
- ✅ SSRF security protection
- ✅ Auto-provider detection
- ✅ Reasoning/thinking mode support
- ✅ Client-side API key override (bring your own key)

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Provider

Choose ONE of the following providers and set the corresponding environment variable in `.env`:

#### OpenAI
```bash
ARCGEN_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-key-here
ARCGEN_LLM_MODEL=gpt-4
```

#### Anthropic (Claude)
```bash
ARCGEN_LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
ARCGEN_LLM_MODEL=claude-3-5-sonnet-20241022
```

#### Google Gemini
```bash
ARCGEN_LLM_PROVIDER=google
GOOGLE_GENERATIVE_AI_API_KEY=your-google-key
ARCGEN_LLM_MODEL=gemini-2.0-flash-exp
```

#### Azure OpenAI
```bash
ARCGEN_LLM_PROVIDER=azure
AZURE_API_KEY=your-azure-key
AZURE_ENDPOINT=https://your-resource.openai.azure.com
ARCGEN_LLM_MODEL=gpt-4
```

#### AWS Bedrock (uses IAM credentials)
```bash
ARCGEN_LLM_PROVIDER=bedrock
AWS_REGION=us-west-2
ARCGEN_LLM_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
```

#### Ollama (local, no API key needed!)
```bash
ARCGEN_LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
ARCGEN_LLM_MODEL=llama2
```

#### DeepSeek
```bash
ARCGEN_LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your-deepseek-key
ARCGEN_LLM_MODEL=deepseek-chat
```

#### NVIDIA NIM (existing support maintained)
``bash
ARCGEN_LLM_PROVIDER=nvidia
NVIDIA_API_KEY=your-nvidia-key
ARCGEN_LLM_MODEL=meta/llama-3.1-70b-instruct
```

### 3. Usage in Code

```python
from backend.ai_providers import AIProviderManager

# Initialize manager
manager = AIProviderManager()

# Get client (auto-detects provider from env)
client, metadata = manager.get_client()

# Or specify provider explicitly
client, metadata = manager.get_client(
    provider="openai",
    model="gpt-4"
)

# With client override (user's own API key)
client, metadata = manager.get_client(
    provider="anthropic",
    model="claude-3-5-sonnet",
    overrides={
        "api_key": "sk-ant-user-key",
        "base_url": "https://custom-endpoint.com"  # Optional
    }
)

# Use the client
response = client.chat.completions.create(
    model=metadata["model"],
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Features

### 1. Auto-Detection

If you don't specify a provider, the system will auto-detect based on available API keys:

```python
# Will auto-detect if only one provider is configured
client, metadata = manager.get_client()
```

### 2. SSRF Protection

**CRITICAL SECURITY FEATURE**

The system enforces SSRF (Server-Side Request Forgery) protection:

```python
# ❌ BLOCKED - custom URL without API key (security risk!)
client = manager.get_client(
    provider="openai",
    overrides={"base_url": "https://evil.com"}  # Missing api_key
)
# Raises: SecurityError

# ✅ ALLOWED - custom URL with user's API key
client = manager.get_client(
    provider="openai",
    overrides={
        "base_url": "https://custom.com",
        "api_key": "user-key"  # Safe - user's own key
    }
)
```

### 3. Reasoning/Thinking Mode Support

Automatically enables reasoning for supported models:

```python
# OpenAI o1, o3, gpt-5
client, meta = manager.get_client(provider="openai", model="o1-preview")
# meta["supports_reasoning"] == True

# Anthropic Claude extended thinking
client, meta = manager.get_client(provider="anthropic", model="claude-3-5-sonnet")
# meta["supports_reasoning"] == True

# Google Gemini 2.5/3.0
client, meta = manager.get_client(provider="google", model="gemini-2.5-pro")
# meta["supports_reasoning"] == True

# DeepSeek R1
client, meta = manager.get_client(provider="deepseek", model="deepseek-r1")
# meta["supports_reasoning"] == True
```

### 4. Custom Endpoints

All providers support custom endpoints (except AWS Bedrock and OpenRouter):

```python
# Custom OpenAI-compatible endpoint
client = manager.get_client(
    provider="openai",
    overrides={
        "api_key": "your-key",
        "base_url": "https://api.together.xyz/v1"
    }
)

# Custom Anthropic endpoint
client = manager.get_client(
    provider="anthropic",
    overrides={
        "api_key": "your-key",
        "base_url": "https://api-proxy.example.com/v1"
    }
)
```

## Testing

Run the comprehensive test suite:

```bash
cd backend
pytest tests/test_ai_providers.py -v
```

Test categories:
- **Security Tests**: SSRF protection, URL validation, library name sanitization
- **Configuration Tests**: Provider configs, reasoning detection
- **Integration Tests**: Actual provider connections (if API keys available)

Example test output:
```
tests/test_ai_providers.py::TestSecurity::test_ssrf_protection_blocks_custom_url_without_key PASSED
tests/test_ai_providers.py::TestSecurity::test_url_safety_requires_https PASSED
tests/test_ai_providers.py::TestProviderManager::test_auto_detection_single_provider PASSED
```

## Migration Guide

### From Old System (single NVIDIA provider)

**Before:**
```python
from backend.llm_manager import LLMManager

llm = LLMManager()
response = llm.generate("prompt")
```

**After:**
```python
from backend.ai_providers import AIProviderManager

manager = AIProviderManager()
client, metadata = manager.get_client()

response = client.chat.completions.create(
    model=metadata["model"],
    messages=[{"role": "user", "content": "prompt"}]
)
```

### Environment Variable Changes

**Before:**
```bash
NVIDIA_API_KEY=nvapi-xxx
```

**After (choose one):**
```bash
# Option 1: Keep NVIDIA
ARCGEN_LLM_PROVIDER=nvidia
NVIDIA_API_KEY=nvapi-xxx
ARCGEN_LLM_MODEL=meta/llama-3.1-70b-instruct

# Option 2: Switch to OpenAI
ARCGEN_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-xxx
ARCGEN_LLM_MODEL=gpt-4

# Option 3: Switch to Anthropic
ARCGEN_LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-xxx
ARCGEN_LLM_MODEL=claude-3-5-sonnet-20241022
```

## Architecture

### File Structure

```
backend/
├── ai_providers/
│   ├── __init__.py              # Package exports
│   ├── provider_config.py       # Provider configurations
│   ├── provider_manager.py      # Main manager class
│   └── security.py              # Security utilities
└── tests/
    └── test_ai_providers.py     # Comprehensive tests
```

### Provider Configuration

All providers are defined in `provider_config.py`:

```python
PROVIDER_CONFIGS = {
    "openai": ProviderConfig(
        name="openai",
        env_var="OPENAI_API_KEY",
        base_url_var="OPENAI_BASE_URL",
        supports_reasoning=True,  # o1, o3, gpt-5
        supports_tools=True,
        supports_streaming=True,
    ),
    # ... more providers
}
```

### Security Model

Based on next-ai-draw-io security model (GHSA-9qf7-mprq-9qgm):

1. **SSRF Protection**: Custom base URLs MUST include API key
2. **URL Validation**: HTTPS required (except localhost)
3. **Private IP Blocking**: Blocks internal network ranges
4. **Path Traversal Protection**: Sanitizes library names

## Advanced Usage

### Provider Metadata

The metadata dict contains useful information:

```python
client, metadata = manager.get_client(provider="openai", model="gpt-4")

print(metadata)
# {
#     "provider": "openai",
#     "model": "gpt-4",
#     "supports_reasoning": False,  # gpt-4 doesn't support reasoning
#     "supports_tools": True,
#     "supports_streaming": True,
# }
```

### Dynamic Provider Switching

```python
# Switch based on user preference
user_provider = request.headers.get("X-AI-Provider")
user_api_key = request.headers.get("X-AI-API-Key")

if user_provider and user_api_key:
    # Use user's provider
    client, meta = manager.get_client(
        provider=user_provider,
        overrides={"api_key": user_api_key}
    )
else:
    # Use server's default provider
    client, meta = manager.get_client()
```

### Error Handling

```python
from backend.ai_providers.security import SecurityError
from backend.ai_providers.provider_manager import ProviderNotConfiguredError

try:
    client, meta = manager.get_client(provider="openai")
except SecurityError as e:
    # SSRF protection triggered
    print(f"Security error: {e}")
except ProviderNotConfiguredError as e:
    # Missing API key or configuration
    print(f"Configuration error: {e}")
except ValueError as e:
    # Invalid provider name
    print(f"Invalid provider: {e}")
```

## Next Steps

1. ✅ **Phase 1 Complete**: Multi-provider AI infrastructure
2. ⏳ **Phase 2**: Tool-based architecture (`display_diagram`, `edit_diagram`, etc.)
3. ⏳ **Phase 3**: Shape library system
4. ⏳ **Phase 4-7**: Frontend, history, deployment

See `implementation_plan.md` for the complete roadmap.

## Support

For issues or questions:
1. Check the test suite for examples
2. Review `specific_code_to_copy.md` for patterns
3. See `implementation_plan.md` for architecture decisions

---

**Implemented**: January 2026  
**Based on**: [next-ai-draw-io](https://github.com/DayuanJiang/next-ai-draw-io) provider system  
**Security Model**: GHSA-9qf7-mprq-9qgm SSRF protection
