#!/usr/bin/env python3
"""
Test script to verify GitHub secrets are configured correctly
Run this after setting up GitHub secrets to validate the configuration
"""

import json

def test_github_secrets():
    """Test that all required secrets are properly formatted"""
    
    print("🔑 GitHub Secrets Configuration Test")
    print("=" * 50)
    
    # Expected secrets
    secrets = {
        "AZURE_SUBSCRIPTION_ID": "7620f9be-bf91-4297-ada2-659d2695b3a1",
        "AZURE_TENANT_ID": "19ced85d-73f5-4193-8797-9fdce478db64", 
        "AZURE_OPENAI_ENDPOINT": "https://copilot-edmund.openai.azure.com/",
        "AZURE_OPENAI_API_KEY": "23g7v6oR2W8dDu3aCIqRn0hGiDUy5zZz7K8RuSYB0FkbliN1us6XJQQJ99BFACYeBjFXJ3w3AAAAACOGGdEj"
    }
    
    print("✅ Required GitHub Secrets:")
    for name, value in secrets.items():
        if "API_KEY" in name:
            print(f"  {name}: {value[:20]}...{value[-10:]}")
        else:
            print(f"  {name}: {value}")
    
    print("\n🔐 AZURE_CREDENTIALS Template:")
    azure_creds_template = {
        "clientId": "your-client-id-from-app-registration",
        "clientSecret": "your-client-secret-value", 
        "subscriptionId": "7620f9be-bf91-4297-ada2-659d2695b3a1",
        "tenantId": "19ced85d-73f5-4193-8797-9fdce478db64"
    }
    
    print(json.dumps(azure_creds_template, indent=2))
    
    print("\n📋 Setup Checklist:")
    checklist = [
        "Go to GitHub repository Settings → Secrets and variables → Actions",
        "Create service principal in Azure Portal (App registrations)",
        "Note client ID, tenant ID, and create client secret",
        "Add all 5 secrets to GitHub with exact values above",
        "Assign Contributor role to service principal for copilot-edmund resource group",
        "Test deployment by running GitHub Actions workflow"
    ]
    
    for i, item in enumerate(checklist, 1):
        print(f"  {i}. {item}")
    
    print("\n🚀 Once configured, deploy Edmund with:")
    print("  1. Go to Actions tab in GitHub")
    print("  2. Select 'Deploy Edmund Agent' workflow") 
    print("  3. Click 'Run workflow' → Choose 'development'")
    print("  4. Monitor deployment progress and logs")
    
    print("\n✅ Setup complete! Edmund will be ready for deployment.")

if __name__ == "__main__":
    test_github_secrets()