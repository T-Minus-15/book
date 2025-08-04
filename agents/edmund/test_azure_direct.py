#!/usr/bin/env python3
"""
Direct test of Edmund using Azure OpenAI with the correct endpoint
"""

import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

def test_edmund_azure():
    """Test Edmund using Azure OpenAI"""
    
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    
    if not api_key or not endpoint:
        print("❌ Missing Azure OpenAI credentials")
        return
    
    print(f"🔗 Endpoint: {endpoint}")
    print(f"🔑 API Key: {api_key[:20]}...{api_key[-10:]}")
    
    try:
        # Create Azure OpenAI client
        client = AzureOpenAI(
            api_version="2024-12-01-preview",
            azure_endpoint=endpoint,
            api_key=api_key
        )
        
        print("✅ Azure OpenAI client created successfully")
        
        # Edmund's system prompt
        edmund_prompt = """You are Edmund, the Engineer from the T-Minus-15 methodology team. You are a no-nonsense AI engineer who loves to build things that work and fix things that don't. You thrive on coding, automation, and solving tough technical problems with elegant solutions. You are deeply versed in the T-Minus-15 methodology and embody engineering excellence that drives successful DevOps teams from idea to production."""
        
        # Test the model
        response = client.chat.completions.create(
            model="gpt-4o",  # Your deployed model
            messages=[
                {"role": "system", "content": edmund_prompt},
                {"role": "user", "content": "Hello Edmund, introduce yourself and tell me about T-Minus-15"}
            ],
            max_tokens=500,
            temperature=0.1
        )
        
        print("\n" + "="*60)
        print("🤖 EDMUND IS ALIVE! 🎉")
        print("="*60)
        print(f"🤖 Edmund's Response:\n{response.choices[0].message.content}")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_edmund_azure()