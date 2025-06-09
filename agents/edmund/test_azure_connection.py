#!/usr/bin/env python3
"""
Test Azure OpenAI connection and diagnose endpoint issues
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_azure_openai_connection():
    """Test the Azure OpenAI connection and list available models"""
    
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    
    if not api_key or not endpoint:
        print("❌ Missing Azure OpenAI credentials")
        print("Required: AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT")
        return
    
    print(f"🔍 Testing Azure OpenAI connection...")
    print(f"📍 Endpoint: {endpoint}")
    print(f"🔑 API Key: {api_key[:20]}...{api_key[-10:]}")
    
    # Test 1: List available models/deployments
    models_url = f"{endpoint.rstrip('/')}/openai/models"
    
    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        print(f"\n🧪 Testing models endpoint: {models_url}")
        response = requests.get(models_url, headers=headers, params={'api-version': '2024-02-01'})
        
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Successfully connected! Found {len(models.get('data', []))} models:")
            
            for model in models.get('data', []):
                print(f"  📦 {model.get('id', 'Unknown')}")
                
        else:
            print(f"❌ Models endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
    
    # Test 2: Try different API versions
    print(f"\n🧪 Testing different API versions...")
    api_versions = ['2024-02-01', '2023-12-01-preview', '2023-09-01-preview', '2023-06-01-preview']
    
    for api_version in api_versions:
        try:
            test_url = f"{endpoint.rstrip('/')}/openai/models"
            response = requests.get(test_url, headers=headers, params={'api-version': api_version})
            
            if response.status_code == 200:
                print(f"✅ API version {api_version} works!")
            else:
                print(f"❌ API version {api_version} failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ API version {api_version} error: {str(e)}")
    
    # Test 3: Try different endpoint formats
    print(f"\n🧪 Testing different endpoint formats...")
    
    base_endpoint = endpoint.rstrip('/')
    test_endpoints = [
        f"{base_endpoint}/openai/models",
        f"{base_endpoint}/models", 
        f"{base_endpoint}/v1/models",
        f"{base_endpoint}/openai/v1/models"
    ]
    
    for test_endpoint in test_endpoints:
        try:
            response = requests.get(test_endpoint, headers=headers, params={'api-version': '2024-02-01'})
            if response.status_code == 200:
                print(f"✅ Endpoint format works: {test_endpoint}")
            else:
                print(f"❌ Endpoint format failed ({response.status_code}): {test_endpoint}")
        except Exception as e:
            print(f"❌ Endpoint format error: {test_endpoint} - {str(e)}")

if __name__ == "__main__":
    test_azure_openai_connection()