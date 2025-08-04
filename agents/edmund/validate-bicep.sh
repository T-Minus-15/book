#!/bin/bash

# Bicep Template Validation Script for Edmund Agent
# This script validates all Bicep templates before deployment

set -e

echo "🔍 Validating Edmund Agent Bicep Templates..."

# Check if Azure CLI is installed and logged in
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first."
    exit 1
fi

# Check if user is logged in
if ! az account show &> /dev/null; then
    echo "❌ Not logged into Azure CLI. Please run 'az login' first."
    exit 1
fi

# Get current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="$SCRIPT_DIR/infra"

echo "📁 Working directory: $SCRIPT_DIR"
echo "🏗️  Infrastructure directory: $INFRA_DIR"

# Check if infra directory exists
if [ ! -d "$INFRA_DIR" ]; then
    echo "❌ Infrastructure directory not found: $INFRA_DIR"
    exit 1
fi

# Validate main.bicep
echo "🔧 Validating main.bicep..."
az deployment sub validate \
    --location eastus \
    --template-file "$INFRA_DIR/main.bicep" \
    --parameters "$INFRA_DIR/main.parameters.json" \
    --parameters environmentName=edmund-test location=eastus principalId="$(az ad signed-in-user show --query id -o tsv)"

if [ $? -eq 0 ]; then
    echo "✅ main.bicep validation passed"
else
    echo "❌ main.bicep validation failed"
    exit 1
fi

# Validate individual modules
echo "🔧 Validating individual Bicep modules..."

# Create a temporary resource group for validation
TEMP_RG="rg-bicep-validation-$(date +%s)"
echo "🏗️  Creating temporary resource group: $TEMP_RG"
az group create --name "$TEMP_RG" --location eastus

# Validate container apps environment
echo "🔧 Validating container-apps-environment.bicep..."
az deployment group validate \
    --resource-group "$TEMP_RG" \
    --template-file "$INFRA_DIR/core/host/container-apps-environment.bicep" \
    --parameters name="cae-test" location=eastus tags='{}' monitoring='{"logAnalyticsWorkspaceCustomerId":"test","logAnalyticsWorkspaceSharedKey":"test"}'

# Validate monitoring
echo "🔧 Validating monitoring.bicep..."
az deployment group validate \
    --resource-group "$TEMP_RG" \
    --template-file "$INFRA_DIR/core/monitor/monitoring.bicep" \
    --parameters logAnalyticsName="log-test" applicationInsightsName="appi-test" location=eastus tags='{}'

# Validate AI services
echo "🔧 Validating ai-services.bicep..."
az deployment group validate \
    --resource-group "$TEMP_RG" \
    --template-file "$INFRA_DIR/core/ai/ai-services.bicep" \
    --parameters hubName="mlw-hub-test" projectName="mlw-project-test" keyVaultName="kv-test$(date +%s)" storageAccountName="st$(date +%s)" containerRegistryName="cr$(date +%s)" applicationInsightsName="appi-test" principalId="$(az ad signed-in-user show --query id -o tsv)" location=eastus tags='{}'

# Clean up temporary resource group
echo "🧹 Cleaning up temporary resource group..."
az group delete --name "$TEMP_RG" --yes --no-wait

echo "✅ All Bicep template validations passed!"
echo ""
echo "🚀 You can now deploy with:"
echo "   azd up"
echo ""
echo "💡 Or validate with a real deployment test:"
echo "   azd provision --preview"