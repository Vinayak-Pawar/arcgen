#!/usr/bin/env python3
"""
Test if NVIDIA API supports tool/function calling
"""
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://integrate.api.nvidia.com/v1"
)

# Simple tool definition
tools = [{
    "type": "function",
    "function": {
        "name": "display_diagram",
        "description": "Display a diagram",
        "parameters": {
            "type": "object",
            "properties": {
                "xml": {"type": "string", "description": "The XML content"}
            },
            "required": ["xml"]
        }
    }
}]

print("🔄 Testing NVIDIA API with tools...")
print("   (timeout: 30 seconds)")

try:
    response = client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[{"role": "user", "content": "Create a simple diagram"}],
        temperature=0.2,
        max_tokens=500,
        tools=tools,
        tool_choice="auto",
        timeout=30.0
    )
    
    print("\n✅ Response received!")
    print(f"Finish reason: {response.choices[0].finish_reason}")
    
    message = response.choices[0].message
    if hasattr(message, 'tool_calls') and message.tool_calls:
        print(f"✓ Tool calls: {len(message.tool_calls)}")
        for tc in message.tool_calls:
            print(f"  - {tc.function.name}")
    else:
        print(f"✓ Text response: {message.content[:100]}...")
        
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    if "tool" in str(e).lower() or "function" in str(e).lower():
        print("\n⚠️  NVIDIA API may not support tool/function calling")
        print("   Try using the API without tools (direct XML generation)")
