# Azure AI Foundry Deployment Guide for Edmund

## 🎯 Current Status

✅ **Azure MCP Server Installed** - Successfully connected to Azure resources  
✅ **Subscription Identified** - Labs Demo (7620f9be-bf91-4297-ada2-659d2695b3a1)  
✅ **Resource Group Found** - copilot-edmund (in East US)  
✅ **Configuration Updated** - Edmund's config now points to correct subscription  

## 🚀 Next Steps: Deploy Models to Azure AI Foundry

### Option 1: Azure Portal (Recommended)

1. **Navigate to Azure AI Foundry**
   - Go to [Azure AI Foundry](https://ai.azure.com)
   - Select subscription: **Labs Demo**
   - Navigate to the **copilot-edmund** workspace

2. **Deploy Models**
   - Go to **Model catalog** or **Deployments**
   - Deploy these models:
     - **gpt-4o** (recommended for Edmund)
     - **gpt-4** (fallback option)
     - **gpt-35-turbo** (cost-effective testing)

3. **Note Deployment Names**
   - Record the exact deployment names (e.g., "gpt-4o-deployment")
   - We'll need these to update Edmund's configuration

### Option 2: Azure CLI Commands

If you have Azure CLI installed locally, run these commands:

```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "7620f9be-bf91-4297-ada2-659d2695b3a1"

# List AI Foundry workspaces
az ml workspace list --resource-group copilot-edmund

# Deploy a model (example)
az ml model deploy \
  --workspace-name copilot-edmund \
  --model gpt-4o \
  --deployment-name gpt-4o-deployment \
  --instance-type Standard_DS3_v2
```

### Option 3: PowerShell/Azure REST API

```powershell
# Login to Azure
Connect-AzAccount

# Set subscription context
Set-AzContext -SubscriptionId "7620f9be-bf91-4297-ada2-659d2695b3a1"

# Get AI Foundry workspace info
Get-AzResource -ResourceGroupName "copilot-edmund" -ResourceType "Microsoft.MachineLearningServices/workspaces"
```

## 🔧 Update Edmund Configuration

Once models are deployed, update Edmund's configuration:

1. **Update endpoint URL** in `.env`:
   ```bash
   AZURE_OPENAI_ENDPOINT=https://your-workspace-name.openai.azure.com/
   ```

2. **Update model names** in `test_edmund_local.py`:
   ```python
   model_names = ["your-deployment-name", "gpt-4o-deployment", "gpt-4"]
   ```

## 🧪 Test Edmund

After models are deployed:

```bash
cd agents/edmund
source venv/bin/activate
python test_edmund_local.py
```

## 📊 Available Azure MCP Commands

You can also use the Azure MCP Server to manage resources:

```bash
# List all resources in copilot-edmund resource group
npx @azure/mcp@latest extension az --command "resource list --resource-group copilot-edmund" --auth-method credential

# List ML workspaces
npx @azure/mcp@latest extension az --command "ml workspace list --resource-group copilot-edmund" --auth-method credential

# Check model deployments
npx @azure/mcp@latest extension az --command "ml model list --workspace-name copilot-edmund --resource-group copilot-edmund" --auth-method credential
```

## 🎉 Expected Result

Once models are deployed, Edmund will be able to:
- ✅ Connect to Azure AI Foundry workspace
- ✅ Use GPT-4o for responses
- ✅ Demonstrate T-Minus-15 expertise
- ✅ Provide technical guidance
- ✅ Test all capabilities locally

## 🚨 Troubleshooting

**If deployment fails:**
1. Check Azure permissions for the copilot-edmund resource group
2. Verify AI Foundry workspace exists and is accessible
3. Ensure sufficient quota for model deployments
4. Try deploying smaller models first (gpt-35-turbo)

**If authentication fails:**
1. Run `az login` to authenticate
2. Check subscription access: `az account show`
3. Verify resource group permissions

## 📞 Support

If you encounter issues:
1. Check the Azure portal for deployment status
2. Review Azure Activity Log for errors
3. Use Azure MCP Server commands for diagnostics

---

**Next**: Deploy models and then we can test Edmund with real Azure AI capabilities! 🚀