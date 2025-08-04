#!/usr/bin/env python3
"""
Simple test of Edmund using direct HTTP requests
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def test_edmund_simple():
    """Test Edmund with a simple HTTP request"""
    
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    
    # Try different URL patterns for Azure OpenAI
    test_urls = [
        f"{endpoint.rstrip('/')}/openai/chat/completions",
        f"{endpoint.rstrip('/')}/v1/chat/completions", 
        f"{endpoint.rstrip('/')}/chat/completions"
    ]
    
    edmund_prompt = """You are Edmund, the Engineer from the T-Minus-15 methodology team. You are a no-nonsense AI engineer who loves to build things that work and fix things that don't. You thrive on coding, automation, and solving tough technical problems with elegant solutions. You are deeply versed in the T-Minus-15 methodology and embody engineering excellence that drives successful DevOps teams from idea to production."""
    
    payload = {
        "messages": [
            {"role": "system", "content": edmund_prompt},
            {"role": "user", "content": "Hello Edmund, introduce yourself and tell me about T-Minus-15"}
        ],
        "max_tokens": 500,
        "temperature": 0.1
    }
    
    headers = {
        'Content-Type': 'application/json',
        'api-key': api_key
    }
    
    for url in test_urls:
        print(f"\n🧪 Testing URL: {url}")
        
        try:
            # Try with different models
            models = ["gpt-4o", "gpt-4", "gpt-35-turbo"]
            
            for model in models:
                test_payload = payload.copy()
                test_payload["model"] = model
                
                response = requests.post(
                    url,
                    headers=headers,
                    json=test_payload,
                    params={'api-version': '2024-02-01'}
                )
                
                print(f"  📦 Model {model}: Status {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    message = result['choices'][0]['message']['content']
                    
                    print(f"✅ SUCCESS with {model}!")
                    print("=" * 60)
                    print("🤖 EDMUND'S RESPONSE:")
                    print(message)
                    print("=" * 60)
                    return True
                    
                elif response.status_code != 404:
                    print(f"    Response: {response.text[:200]}...")
                    
        except Exception as e:
            print(f"    Error: {str(e)}")
    
    print("\n❌ All tests failed")
    return False

if __name__ == "__main__":
    test_edmund_simple()