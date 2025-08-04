#!/bin/bash

# Deploy Edmund Agent to Azure AI Foundry
# Usage: ./deploy_edmund.sh

set -e

echo "🚀 Deploying Edmund Agent to Azure AI Foundry..."

# Configuration
RESOURCE_GROUP="copilot-edmund"
AI_SERVICE_NAME="Copilot-Edmund"
PROJECT_NAME="Copilot-Edmund"
DEPLOYMENT_NAME="gpt-4o"

# Get AI Service endpoint
echo "📍 Getting AI Service details..."
AI_SERVICE_ENDPOINT=$(az cognitiveservices account show \
  --name "$AI_SERVICE_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --query "properties.endpoint" -o tsv 2>/dev/null || echo "")

if [ -z "$AI_SERVICE_ENDPOINT" ]; then
  echo "❌ Could not get AI Service endpoint. Make sure the service exists."
  exit 1
fi

# Construct correct AI Foundry Agent Service endpoint
AI_FOUNDRY_ENDPOINT="${AI_SERVICE_ENDPOINT}api/projects/${PROJECT_NAME}"

echo "🔗 AI Foundry Endpoint: $AI_FOUNDRY_ENDPOINT"

# Get access token
echo "🔑 Getting access token..."
ACCESS_TOKEN=$(az account get-access-token --resource https://cognitiveservices.azure.com --query accessToken -o tsv)

if [ -z "$ACCESS_TOKEN" ]; then
  echo "❌ Could not get access token. Make sure you're logged into Azure CLI."
  exit 1
fi

# Read Edmund's configuration
echo "📖 Reading Edmund configuration..."
if [ ! -f "agent-config.json" ]; then
  echo "❌ agent-config.json not found. Run this script from the agents/edmund directory."
  exit 1
fi

INSTRUCTIONS=$(cat agent-config.json | jq -r '.instructions.systemPrompt')

# Create agent payload
echo "📝 Creating agent payload..."
cat > agent-payload.json << EOF
{
  "name": "edmund-engineer",
  "instructions": "$INSTRUCTIONS",
  "model": "$DEPLOYMENT_NAME",
  "tools": [
    {"type": "code_interpreter"},
    {"type": "file_search"}
  ],
  "metadata": {
    "version": "1.0.0",
    "methodology": "T-Minus-15",
    "deployment_environment": "production",
    "deployed_by": "manual_script",
    "deployed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  }
}
EOF

echo "Agent payload created:"
cat agent-payload.json | jq .

# Deploy agent
echo "🤖 Deploying Edmund agent..."
HTTP_STATUS=$(curl -s -w "%{http_code}" -X POST "$AI_FOUNDRY_ENDPOINT/assistants?api-version=2025-05-01" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d @agent-payload.json \
  -o deployment-response.json)

echo "HTTP Status: $HTTP_STATUS"

if [ "$HTTP_STATUS" -eq 200 ] || [ "$HTTP_STATUS" -eq 201 ]; then
  echo "✅ Edmund agent deployed successfully!"
  
  # Extract agent ID
  AGENT_ID=$(cat deployment-response.json | jq -r '.id' 2>/dev/null || echo "")
  
  if [ "$AGENT_ID" != "" ] && [ "$AGENT_ID" != "null" ]; then
    echo "🆔 Agent ID: $AGENT_ID"
    
    # Test the deployment
    echo "🧪 Testing deployment..."
    
    # Create test thread
    curl -s -X POST "$AI_FOUNDRY_ENDPOINT/threads?api-version=2025-05-01" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"metadata": {"test": "true"}}' \
      -o thread-response.json
    
    THREAD_ID=$(cat thread-response.json | jq -r '.id' 2>/dev/null || echo "")
    
    if [ "$THREAD_ID" != "" ] && [ "$THREAD_ID" != "null" ]; then
      echo "✅ Test thread created: $THREAD_ID"
      
      # Send test message
      curl -s -X POST "$AI_FOUNDRY_ENDPOINT/threads/$THREAD_ID/messages?api-version=2025-05-01" \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"role": "user", "content": "Hello Edmund! Tell me about the T-Minus-15 methodology."}' \
        -o message-response.json
      
      echo "✅ Test message sent to Edmund"
      
      # Run the conversation
      curl -s -X POST "$AI_FOUNDRY_ENDPOINT/threads/$THREAD_ID/runs?api-version=2025-05-01" \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"assistant_id\": \"$AGENT_ID\"}" \
        -o run-response.json
      
      echo "✅ Conversation run initiated"
      echo "📋 Test completed successfully"
    else
      echo "⚠️ Could not create test thread"
    fi
  else
    echo "⚠️ Could not extract agent ID from response"
  fi
  
  echo "📄 Deployment response:"
  cat deployment-response.json | jq .
  
else
  echo "❌ Deployment failed with HTTP status: $HTTP_STATUS"
  echo "Response:"
  cat deployment-response.json
  exit 1
fi

echo ""
echo "🎉 Edmund deployment complete!"
echo "📍 You can find Edmund in the Azure AI Foundry portal at:"
echo "   https://ai.azure.com/resource/agentsList"
echo ""
echo "🧪 To test Edmund, you can:"
echo "   1. Go to the Azure AI Foundry portal"
echo "   2. Find 'edmund-engineer' in your agents list"
echo "   3. Click 'Try in playground'"
echo "   4. Ask: 'What is the T-Minus-15 methodology?'"