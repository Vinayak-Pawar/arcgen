"""
LLM Manager for Arcgen

Dynamically routes to different LLM providers based on user configuration.
Supports OpenAI, Anthropic, Google Gemini, NVIDIA NIM, Ollama, and custom endpoints.
"""

import json
from typing import Optional, Dict, Any
from config import LLMConfig, LLMProvider, get_api_key
import httpx


class LLMManager:
    """Manages LLM API calls for different providers"""

    def __init__(self, config: LLMConfig):
        self.config = config
        self.api_key = get_api_key(config)

    async def generate_csv(self, prompt: str) -> str:
        """
        Generate CSV diagram from natural language prompt using configured LLM
        """
        full_prompt = self._build_csv_prompt(prompt)

        if self.config.provider == LLMProvider.OPENAI:
            return await self._call_openai(full_prompt)
        elif self.config.provider == LLMProvider.ANTHROPIC:
            return await self._call_anthropic(full_prompt)
        elif self.config.provider == LLMProvider.GOOGLE:
            return await self._call_google(full_prompt)
        elif self.config.provider == LLMProvider.NVIDIA:
            return await self._call_nvidia(full_prompt)
        elif self.config.provider == LLMProvider.OLLAMA:
            return await self._call_ollama(full_prompt)
        elif self.config.provider == LLMProvider.CUSTOM:
            return await self._call_custom(full_prompt)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.config.provider}")

    def _build_csv_prompt(self, user_prompt: str) -> str:
        """Build the CSV generation prompt"""
        return f"""You are an expert system architect specializing in creating draw.io diagrams from natural language descriptions.

Your task is to generate a CSV format diagram that draw.io can understand. Follow this exact structure:

## Label: %label%
## Style: shape=%shape%;whiteSpace=wrap;html=1;
## Connect: {{"from": "edge_target", "to": "id", "style": "curved=1;endArrow=blockThin;endFill=1;"}}
id,label,shape,edge_target

IMPORTANT: The CSV must have exactly 4 columns: id,label,shape,edge_target

Rules:
1. 'id': Unique sequential numbers starting from 1
2. 'label': Display text for the component (keep under 20 characters)
3. 'shape': Visual appearance (rectangle, rounded=1, actor, ellipse, hexagon, parallelogram, diamond)
4. 'edge_target': ID of component this connects TO (leave empty if no connection)

Shape guidelines:
- actor: Users/clients
- rectangle: Services, databases, applications
- rounded=1: Processes, actions
- ellipse: External systems, clouds
- hexagon: Databases, storage
- diamond: Decisions, gateways
- parallelogram: Data flows, queues

Flow: Start with user/client, create logical left-to-right flow.

Output ONLY the CSV content with proper headers and data rows. No explanations.

System Description: {user_prompt}

Generate the CSV diagram:"""

    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key, base_url=self.config.base_url)

            response = client.chat.completions.create(
                model=self.config.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                top_p=self.config.top_p
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    async def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.config.base_url}/v1/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={
                        "model": self.config.model,
                        "max_tokens": self.config.max_tokens,
                        "temperature": self.config.temperature,
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    timeout=60.0
                )
                response.raise_for_status()
                result = response.json()
                return result["content"][0]["text"]
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")

    async def _call_google(self, prompt: str) -> str:
        """Call Google Gemini API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.config.base_url}/v1beta/models/{self.config.model}:generateContent",
                    params={"key": self.api_key},
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {
                            "temperature": self.config.temperature,
                            "maxOutputTokens": self.config.max_tokens,
                            "topP": self.config.top_p
                        }
                    },
                    timeout=60.0
                )
                response.raise_for_status()
                result = response.json()
                return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            raise Exception(f"Google API error: {str(e)}")

    async def _call_nvidia(self, prompt: str) -> str:
        """Call NVIDIA NIM API (current implementation)"""
        try:
            from openai import OpenAI
            client = OpenAI(
                base_url=self.config.base_url,
                api_key=self.api_key
            )

            response = client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": "You are a system architecture expert that creates draw.io CSV diagrams."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                top_p=self.config.top_p
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"NVIDIA API error: {str(e)}")

    async def _call_ollama(self, prompt: str) -> str:
        """Call local Ollama API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.config.base_url}/chat/completions",
                    json={
                        "model": self.config.model,
                        "messages": [{"role": "user", "content": prompt}],
                        "stream": False,
                        "options": {
                            "temperature": self.config.temperature,
                            "num_predict": self.config.max_tokens,
                            "top_p": self.config.top_p
                        }
                    },
                    timeout=120.0  # Ollama can be slower
                )
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}. Make sure Ollama is running locally.")

    async def _call_custom(self, prompt: str) -> str:
        """Call custom OpenAI-compatible API"""
        try:
            from openai import OpenAI
            client = OpenAI(
                base_url=self.config.base_url,
                api_key=self.api_key
            )

            response = client.chat.completions.create(
                model=self.config.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                top_p=self.config.top_p
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Custom API error: {str(e)}")


# Factory function to create LLM manager
def create_llm_manager(config: LLMConfig) -> LLMManager:
    """Create an LLM manager for the given configuration"""
    return LLMManager(config)


# Test function to validate provider setup
async def test_llm_provider(config: LLMConfig) -> Dict[str, Any]:
    """Test if the LLM provider is working"""
    try:
        manager = create_llm_manager(config)
        # Simple test prompt
        test_prompt = "Generate a simple CSV diagram with just one component: a user."
        csv_result = await manager.generate_csv(test_prompt)

        return {
            "success": True,
            "provider": config.provider.value,
            "model": config.model,
            "message": "LLM provider is working correctly",
            "sample_output": csv_result[:200] + "..." if len(csv_result) > 200 else csv_result
        }
    except Exception as e:
        return {
            "success": False,
            "provider": config.provider.value,
            "error": str(e),
            "message": f"Failed to connect to {config.provider.value}: {str(e)}"
        }
