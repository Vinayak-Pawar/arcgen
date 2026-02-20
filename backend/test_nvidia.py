#!/usr/bin/env python3
"""
Quick test script to verify NVIDIA API is working
"""
import os
import sys
from openai import OpenAI

# Load environment
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")
if not api_key:
    print("❌ NVIDIA_API_KEY not found in environment")
    sys.exit(1)

print(f"✓ API Key found: {api_key[:10]}...")

# Test connection
try:
    client = OpenAI(
        api_key=api_key,
        base_url="https://integrate.api.nvidia.com/v1"
    )
    
    print("\n🔄 Testing NVIDIA API connection...")
    print("   (This may take 10-30 seconds...)")
    
    response = client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[{"role": "user", "content": "Say 'Hello'"}],
        temperature=0.2,
        max_tokens=50,
        timeout=30.0  # 30 second timeout
    )
    
    result = response.choices[0].message.content
    print(f"\n✅ Success! Response: {result}")
    print("\n✓ NVIDIA API is working correctly")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nPossible issues:")
    print("  1. API key is invalid or expired")
    print("  2. NVIDIA API is down")
    print("  3. Network connectivity issues")
    print("  4. Rate limiting")
    sys.exit(1)
