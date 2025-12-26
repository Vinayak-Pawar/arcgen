#!/usr/bin/env python3
"""
Test script for NVIDIA API integration
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# System prompt template for CSV generation
CSV_GENERATION_PROMPT = """
You are an expert system architect specializing in creating draw.io diagrams from natural language descriptions.

Your task is to generate a CSV format diagram that draw.io can understand. The CSV format should follow this structure:

## Label: %label%
## Style: shape=%shape%;whiteSpace=wrap;html=1;
## Connect: {"from": "edge_target", "to": "id", "style": "curved=1;endArrow=blockThin;endFill=1;"}
id,label,shape,edge_target

Rules for CSV generation:
1. Each row represents a component or connection
2. 'id' should be unique sequential numbers starting from 1
3. 'label' is the display text for the component
4. 'shape' defines the visual appearance (rectangle, rounded=1, actor, etc.)
5. 'edge_target' specifies which component this connects to (leave empty for end nodes)

Common shapes:
- rectangle: Standard rectangle
- rounded=1: Rounded rectangle
- actor: User/person icon
- ellipse: Circle/oval
- hexagon: Hexagon
- parallelogram: Parallelogram
- diamond: Decision point

Guidelines:
- Start with the user/client component
- Create logical flow from left to right
- Use appropriate shapes for different system components
- Include all major components mentioned in the description
- Keep labels clear and concise

Output ONLY the CSV content, no explanations or additional text.
"""

def test_nvidia_api():
    """Test NVIDIA API connection and CSV generation"""
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        print("❌ Error: NVIDIA_API_KEY environment variable not set")
        return False

    try:
        # Initialize client
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key
        )

        # Test prompts
        test_prompts = [
            "User logs into a web application with authentication service",
            "Data flows from BigQuery to Compute Engine for batch processing",
            "Microservices architecture with API Gateway, User Service, and PostgreSQL"
        ]

        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n🔍 Test {i}: {prompt}")
            print("-" * 50)

            # Create the full prompt
            full_prompt = f"{CSV_GENERATION_PROMPT}\n\nSystem Description: {prompt}\n\nGenerate the CSV diagram:"

            # Call API
            response = client.chat.completions.create(
                model="meta/llama-3.1-70b-instruct",
                messages=[
                    {"role": "system", "content": "You are a system architecture expert that creates draw.io CSV diagrams."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.2,
                max_tokens=2048,
                top_p=0.7
            )

            # Get CSV content
            csv_content = response.choices[0].message.content

            # Basic validation
            if not csv_content or not csv_content.strip():
                print("❌ Empty response")
                continue

            lines = csv_content.strip().split('\n')
            print(f"📊 Response length: {len(lines)} lines")

            # Check for basic CSV structure
            if len(lines) >= 5:
                print("✅ Valid CSV structure detected")
                print("📄 First 5 lines:")
                for line in lines[:5]:
                    print(f"  {line}")
                if len(lines) > 5:
                    print(f"  ... ({len(lines) - 5} more lines)")
            else:
                print("⚠️  Response might be too short")
                print("📄 Full response:")
                print(csv_content)

        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Testing NVIDIA API Integration")
    print("=" * 50)

    success = test_nvidia_api()

    if success:
        print("\n🎉 API test completed successfully!")
    else:
        print("\n💥 API test failed. Check your NVIDIA_API_KEY and connection.")
