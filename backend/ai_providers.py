"""
Multi-Provider AI System for Arcgen
Adapted from next-ai-draw-io's ai-providers.ts
Supports OpenAI, Anthropic, Google, Azure, Ollama, and NVIDIA
"""

import os
from enum import Enum
from typing import Optional, Dict, Any, List, AsyncGenerator
from pydantic import BaseModel
import json
import openai
from anthropic import Anthropic
import google.generativeai as genai
from tools import get_tools_for_ai, validate_tool_call, shape_library_manager
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from ollama import Client as OllamaClient


class Provider(str, Enum):
    """Supported AI providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    AZURE = "azure"
    OLLAMA = "ollama"
    NVIDIA = "nvidia"


class AIModelConfig(BaseModel):
    """Configuration for AI model"""
    provider: Provider
    model_id: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: Optional[float] = 0.2
    max_tokens: Optional[int] = 2048
    reasoning_budget_tokens: Optional[int] = None
    custom_headers: Optional[Dict[str, str]] = None


class ClientOverrides(BaseModel):
    """Client-side overrides for provider configuration"""
    provider: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model_id: Optional[str] = None
    temperature: Optional[float] = None


# Provider-specific environment variable mappings
PROVIDER_ENV_VARS = {
    Provider.OPENAI: "OPENAI_API_KEY",
    Provider.ANTHROPIC: "ANTHROPIC_API_KEY",
    Provider.GOOGLE: "GOOGLE_API_KEY",
    Provider.AZURE: "AZURE_API_KEY",
    Provider.OLLAMA: None,  # No API key needed
    Provider.NVIDIA: "NVIDIA_API_KEY",
}

# Allowed client-provided providers (for security)
ALLOWED_CLIENT_PROVIDERS = [
    Provider.OPENAI,
    Provider.ANTHROPIC,
    Provider.GOOGLE,
    Provider.AZURE,
    Provider.NVIDIA,
]


class AIProviderManager:
    """Manages multiple AI providers and their clients"""

    def __init__(self):
        self._clients = {}
        self._current_config: Optional[AIModelConfig] = None

    def get_model_config(self, overrides: Optional[ClientOverrides] = None) -> AIModelConfig:
        """Get AI model configuration with optional overrides"""

        # Determine provider
        provider_str = overrides.provider if overrides and overrides.provider else os.getenv("AI_PROVIDER", "nvidia")
        try:
            provider = Provider(provider_str.lower())
        except ValueError:
            provider = Provider.NVIDIA

        # Get model ID
        model_id = overrides.model_id if overrides and overrides.model_id else os.getenv("AI_MODEL")
        if not model_id:
            # Default models for each provider
            default_models = {
                Provider.OPENAI: "gpt-4o",
                Provider.ANTHROPIC: "claude-3-5-sonnet-20241022",
                Provider.GOOGLE: "gemini-pro",
                Provider.AZURE: "gpt-4o",
                Provider.OLLAMA: "llama3.2",
                Provider.NVIDIA: "meta/llama-3.1-70b-instruct",
            }
            model_id = default_models.get(provider, "meta/llama-3.1-70b-instruct")

        # Get API key (client override takes precedence for security)
        api_key = None
        if overrides and overrides.api_key:
            api_key = overrides.api_key
        else:
            env_var = PROVIDER_ENV_VARS.get(provider)
            if env_var:
                api_key = os.getenv(env_var)

        # Get base URL
        base_url = overrides.base_url if overrides and overrides.base_url else None
        if not base_url:
            # Default base URLs
            default_urls = {
                Provider.OPENAI: "https://api.openai.com/v1",
                Provider.ANTHROPIC: "https://api.anthropic.com",
                Provider.GOOGLE: "https://generativelanguage.googleapis.com",
                Provider.AZURE: None,  # Uses resource name
                Provider.OLLAMA: "http://localhost:11434",
                Provider.NVIDIA: "https://integrate.api.nvidia.com/v1",
            }
            base_url = default_urls.get(provider)

        # Get temperature
        temperature = overrides.temperature if overrides and overrides.temperature else float(os.getenv("TEMPERATURE", "0.2"))

        config = AIModelConfig(
            provider=provider,
            model_id=model_id,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
        )

        self._current_config = config
        return config

    def get_client(self, config: AIModelConfig):
        """Get or create client for the given configuration"""
        cache_key = f"{config.provider.value}:{config.model_id}:{config.base_url}"

        if cache_key in self._clients:
            return self._clients[cache_key]

        client = None

        try:
            if config.provider == Provider.OPENAI:
                client = openai.OpenAI(
                    api_key=config.api_key,
                    base_url=config.base_url,
                )
            elif config.provider == Provider.ANTHROPIC:
                client = Anthropic(
                    api_key=config.api_key,
                    base_url=config.base_url,
                )
            elif config.provider == Provider.GOOGLE:
                genai.configure(api_key=config.api_key)
                client = genai.GenerativeModel(config.model_id)
            elif config.provider == Provider.AZURE:
                # Azure OpenAI setup
                if config.base_url:
                    client = openai.AzureOpenAI(
                        api_key=config.api_key,
                        azure_endpoint=config.base_url,
                        api_version="2024-02-01",
                    )
                else:
                    # Use resource name approach
                    resource_name = os.getenv("AZURE_RESOURCE_NAME")
                    if resource_name:
                        client = openai.AzureOpenAI(
                            api_key=config.api_key,
                            azure_endpoint=f"https://{resource_name}.openai.azure.com/",
                            api_version="2024-02-01",
                        )
            elif config.provider == Provider.OLLAMA:
                client = OllamaClient(host=config.base_url or "http://localhost:11434")
            elif config.provider == Provider.NVIDIA:
                # NVIDIA uses OpenAI-compatible API
                client = openai.OpenAI(
                    api_key=config.api_key,
                    base_url=config.base_url,
                )

        except Exception as e:
            raise ValueError(f"Failed to initialize {config.provider.value} client: {str(e)}")

        if client:
            self._clients[cache_key] = client

        return client

    async def generate_diagram(self, prompt: str, config: AIModelConfig) -> Dict[str, Any]:
        """Generate diagram using tool-based architecture"""
        client = self.get_client(config)

        if not client:
            raise ValueError(f"No client available for provider {config.provider.value}")

        # Enhanced system prompt with tool instructions
        system_prompt = """You are an expert diagram creation assistant specializing in draw.io XML generation.
Your primary function is creating clear, well-organized visual diagrams through precise XML specifications.

When you are asked to create a diagram, briefly describe your plan about the layout and structure to avoid object overlapping or edge crossing the objects. (2-3 sentences max), then use display_diagram tool to generate the XML.
After generating or editing a diagram, you don't need to say anything. The user can see the diagram - no need to describe it.

## App Context
You are an AI agent inside a web app with draw.io diagram editor. You can read and modify diagrams by generating draw.io XML code through tool calls.

## Available Tools
You utilize the following tools:
---Tool1---
tool name: display_diagram
description: Display a NEW diagram on draw.io. Use this when creating a diagram from scratch or when major structural changes are needed.
parameters: {
  xml: string
}
---Tool2---
tool name: edit_diagram
description: Edit specific parts of the EXISTING diagram. Use this when making small targeted changes like adding/removing elements, changing labels, or adjusting properties. This is more efficient than regenerating the entire diagram.
parameters: {
  edits: Array<{search: string, replace: string}>
}
---Tool3---
tool name: append_diagram
description: Continue generating diagram XML when display_diagram was truncated due to output length limits. Only use this after display_diagram truncation.
parameters: {
  xml: string  // Continuation fragment (NO wrapper tags like <mxGraphModel> or <root>)
}
---Tool4---
tool name: get_shape_library
description: Get shape/icon library documentation. Use this to discover available icon shapes (AWS, Azure, GCP, Kubernetes, etc.) before creating diagrams with cloud/tech icons.
parameters: {
  library: string  // Library name: aws4, azure2, gcp2, kubernetes, cisco19, flowchart, bpmn, etc.
}

IMPORTANT: Choose the right tool:
- Use display_diagram for: Creating new diagrams, major restructuring, or when the current diagram XML is empty
- Use edit_diagram for: Small modifications, adding/removing elements, changing text/colors, repositioning items
- Use append_diagram for: ONLY when display_diagram was truncated due to output length - continue generating from where you stopped
- Use get_shape_library for: Discovering available icons/shapes when creating cloud architecture or technical diagrams (call BEFORE display_diagram)

## Layout Constraints
- Keep all diagram elements within viewport: x coordinates 0-800, y coordinates 0-600
- Maximum width for containers: 700 pixels, height: 550 pixels
- Start positioning from margins (x=40, y=40) and keep elements grouped closely
- Use compact layouts that fit entire diagram in one view

## XML Generation Rules
- Generate ONLY mxCell elements - NO wrapper tags, NO explanations, NO markdown
- Use vertex="1" for shapes, edge="1" for connectors
- Start IDs from "2" (1 is reserved for root)
- Use parent="1" for all elements
- NEVER include XML comments (<!-- ... -->) - they break edit_diagram patterns
- Return XML only via tool calls, never in text responses

For cloud/tech diagrams, ALWAYS call get_shape_library first to discover available professional icons. Use the exact shape names and syntax provided by the library. For example:
- AWS: Use "shape=mxgraph.aws4.ec2" for EC2 instances
- Azure: Use "shape=mxgraph.azure2.virtual_machine" for VMs
- GCP: Use "shape=mxgraph.gcp2.compute_engine" for Compute Engine
- Kubernetes: Use "shape=mxgraph.kubernetes.pod" for pods

This ensures your diagrams use authentic, professional cloud service icons instead of generic shapes."""

        try:
            # Make the tool call
            tool_result = await self._call_with_tools(
                client=client,
                config=config,
                system_prompt=system_prompt,
                user_prompt=prompt
            )

            return tool_result

        except Exception as e:
            raise ValueError(f"Failed to generate diagram with {config.provider.value}: {str(e)}")

    async def _call_with_tools(self, client, config: AIModelConfig, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Make AI call with tool support"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        tools = get_tools_for_ai(config.provider.value)

        if config.provider == Provider.OPENAI or config.provider == Provider.NVIDIA:
            response = client.chat.completions.create(
                model=config.model_id,
                messages=messages,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                tools=tools,
                tool_choice="auto"
            )

            # Process tool calls
            message = response.choices[0].message
            if hasattr(message, 'tool_calls') and message.tool_calls:
                result = await self._process_tool_calls(message.tool_calls)
                if result:
                    return result

            # Fallback: check if the response contains XML directly
            content = message.content or ""
            if "<mxCell" in content and "vertex=" in content:
                # Extract XML from response
                start = content.find("<mxCell")
                if start >= 0:
                    xml_content = content[start:]
                    # Clean up any trailing content
                    end_markers = ["```", "</mxGraphModel>", "\n\n"]
                    for marker in end_markers:
                        end_pos = xml_content.find(marker)
                        if end_pos >= 0:
                            xml_content = xml_content[:end_pos]
                    return {"type": "display_diagram", "xml": xml_content.strip()}

            # Final fallback to text response
            return {"type": "text", "content": content}

        elif config.provider == Provider.ANTHROPIC:
            # Anthropic tool calling setup
            tools_for_anthropic = []
            for tool in tools:
                tools_for_anthropic.append({
                    "name": tool["name"],
                    "description": tool["description"],
                    "input_schema": tool["parameters"]
                })

            response = await client.messages.create(
                model=config.model_id,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
                tools=tools_for_anthropic,
                tool_choice={"type": "auto"}
            )

            # Process tool calls for Anthropic
            if response.stop_reason == "tool_use":
                return await self._process_anthropic_tool_calls(response.content)
            else:
                return {"type": "text", "content": response.content[0].text}

        elif config.provider == Provider.GOOGLE:
            # Google doesn't support tools well, fallback to text
            response = await client.generate_content_async(
                contents=[{"parts": [{"text": f"{system_prompt}\n\nUser: {user_prompt}"}]}],
                generation_config=genai.types.GenerationConfig(
                    temperature=config.temperature,
                    max_output_tokens=config.max_tokens,
                )
            )
            return {"type": "text", "content": response.text}

        elif config.provider == Provider.AZURE:
            response = client.chat.completions.create(
                model=config.model_id,
                messages=messages,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                tools=tools,
                tool_choice="auto"
            )

            message = response.choices[0].message
            if hasattr(message, 'tool_calls') and message.tool_calls:
                return await self._process_tool_calls(message.tool_calls)
            else:
                return {"type": "text", "content": message.content}

        elif config.provider == Provider.OLLAMA:
            # Ollama doesn't support tools, fallback to text
            response = client.chat(
                model=config.model_id,
                messages=messages,
                options={
                    "temperature": config.temperature,
                    "num_predict": config.max_tokens,
                }
            )
            return {"type": "text", "content": response['message']['content']}

        else:
            raise ValueError(f"Provider {config.provider.value} not yet implemented")

    async def _process_tool_calls(self, tool_calls) -> Dict[str, Any]:
        """Process tool calls from OpenAI/Azure style responses"""
        results = []

        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            if tool_name == "display_diagram":
                # Return the XML directly
                return {
                    "type": "display_diagram",
                    "xml": tool_args["xml"]
                }

            elif tool_name == "edit_diagram":
                # Return edit operations
                return {
                    "type": "edit_diagram",
                    "edits": tool_args["edits"]
                }

            elif tool_name == "append_diagram":
                # Return append operation
                return {
                    "type": "append_diagram",
                    "xml": tool_args["xml"]
                }

            elif tool_name == "get_shape_library":
                # Return shape library info
                library_info = shape_library_manager.get_library_info(tool_args["library"])
                return {
                    "type": "shape_library",
                    "library": tool_args["library"],
                    "info": library_info
                }

        # If no specific tool result, return general response
        return {"type": "text", "content": "Tool call processed"}

    async def _process_anthropic_tool_calls(self, content) -> Dict[str, Any]:
        """Process tool calls from Anthropic responses"""
        for item in content:
            if item.type == "tool_use":
                tool_name = item.name
                tool_args = item.input

                if tool_name == "display_diagram":
                    return {
                        "type": "display_diagram",
                        "xml": tool_args["xml"]
                    }
                elif tool_name == "edit_diagram":
                    return {
                        "type": "edit_diagram",
                        "edits": tool_args["edits"]
                    }
                elif tool_name == "append_diagram":
                    return {
                        "type": "append_diagram",
                        "xml": tool_args["xml"]
                    }
                elif tool_name == "get_shape_library":
                    library_info = shape_library_manager.get_library_info(tool_args["library"])
                    return {
                        "type": "shape_library",
                        "library": tool_args["library"],
                        "info": library_info
                    }

        return {"type": "text", "content": "No tool calls found"}

    def validate_provider_config(self, provider: Provider, api_key: Optional[str] = None) -> bool:
        """Validate that provider configuration is complete"""
        if provider == Provider.OLLAMA:
            return True  # No API key needed

        required_key = PROVIDER_ENV_VARS.get(provider)
        if required_key and not (api_key or os.getenv(required_key)):
            return False

        if provider == Provider.AZURE:
            has_base_url = bool(os.getenv("AZURE_BASE_URL"))
            has_resource_name = bool(os.getenv("AZURE_RESOURCE_NAME"))
            return has_base_url or has_resource_name

        return True

    def get_available_providers(self) -> List[Dict[str, Any]]:
        """Get list of available providers with their status"""
        providers = []

        for provider in Provider:
            is_configured = self.validate_provider_config(provider)
            providers.append({
                "name": provider.value,
                "label": provider.value.title(),
                "configured": is_configured,
                "requires_key": provider != Provider.OLLAMA,
                "default_model": self._get_default_model(provider),
            })

        return providers

    def _get_default_model(self, provider: Provider) -> str:
        """Get default model for provider"""
        defaults = {
            Provider.OPENAI: "gpt-4o",
            Provider.ANTHROPIC: "claude-3-5-sonnet-20241022",
            Provider.GOOGLE: "gemini-pro",
            Provider.AZURE: "gpt-4o",
            Provider.OLLAMA: "llama3.2",
            Provider.NVIDIA: "meta/llama-3.1-70b-instruct",
        }
        return defaults.get(provider, "gpt-4o")


# Global instance
ai_provider_manager = AIProviderManager()


def get_ai_provider_manager() -> AIProviderManager:
    """Get the global AI provider manager instance"""
    return ai_provider_manager
