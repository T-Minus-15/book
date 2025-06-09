# Edmund Deployment Setup Guide

## 🚀 Deploy Edmund to Azure AI Foundry

### Prerequisites Checklist
- ✅ Azure subscription: **Labs Demo** (7620f9be-bf91-4297-ada2-659d2695b3a1)
- ✅ Resource group: **copilot-edmund** 
- ✅ Azure OpenAI service deployed with **gpt-4o** model
- ✅ GitHub repository access

## 🔑 Step 1: Configure GitHub Secrets

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions** and add these secrets:

### Required Secrets:

1. **AZURE_SUBSCRIPTION_ID**
   ```
   7620f9be-bf91-4297-ada2-659d2695b3a1
   ```

2. **AZURE_TENANT_ID**
   ```
   19ced85d-73f5-4193-8797-9fdce478db64
   ```

3. **AZURE_CREDENTIALS**
   Create a service principal and add the JSON output:
   ```bash
   az ad sp create-for-rbac \
     --name "T-Minus-15-Edmund-Deploy" \
     --role contributor \
     --scopes /subscriptions/7620f9be-bf91-4297-ada2-659d2695b3a1/resourceGroups/copilot-edmund \
     --sdk-auth
   ```
   Copy the entire JSON output to this secret.

4. **AZURE_OPENAI_ENDPOINT**
   ```
   https://copilot-edmund.openai.azure.com/
   ```

5. **AZURE_OPENAI_API_KEY**
   ```
   [Your actual API key from Azure portal]
   ```

## 🏗️ Step 2: Verify Azure Resources

Check that these resources exist in your Azure subscription:

```bash
# List resources in copilot-edmund resource group
az resource list --resource-group copilot-edmund --output table

# Verify OpenAI service
az cognitiveservices account show \
  --name copilot-edmund \
  --resource-group copilot-edmund

# Check gpt-4o model deployment
az cognitiveservices account deployment list \
  --name copilot-edmund \
  --resource-group copilot-edmund
```

## 🚀 Step 3: Deploy Edmund

### Option 1: Manual Trigger (Recommended)
1. Go to **Actions** tab in your GitHub repository
2. Select **Deploy Edmund Agent** workflow
3. Click **Run workflow**
4. Choose environment: **development**
5. Click **Run workflow**

### Option 2: Push Changes
Any changes to `agents/edmund/` files will automatically trigger deployment:
```bash
git add agents/edmund/
git commit -m "Deploy Edmund agent updates"
git push origin main
```

## 📊 Step 4: Monitor Deployment

### GitHub Actions Monitoring
- Watch the workflow progress in the **Actions** tab
- Check logs for each deployment step
- Verify successful completion

### Azure Portal Monitoring
- Go to [Azure AI Foundry](https://ai.azure.com)
- Navigate to **Labs Demo** subscription
- Check **copilot-edmund** resource group
- Verify agent deployment status

## 🧪 Step 5: Test Edmund

Once deployed, test Edmund using the local test script:

```bash
cd agents/edmund
source venv/bin/activate
python test_azure_direct.py
```

Expected output:
```
🤖 EDMUND IS ALIVE! 🎉
🤖 Edmund's Response: Hey there! I'm Edmund, your no-nonsense engineer...
```

## 🔧 Troubleshooting

### Common Issues:

**1. Authentication Failed**
- Verify AZURE_CREDENTIALS secret is valid JSON
- Check service principal has correct permissions
- Ensure subscription ID is correct

**2. Resource Group Not Found**
- Confirm `copilot-edmund` resource group exists
- Check resource group location (should be East US)
- Verify service principal has access

**3. OpenAI Model Not Found**
- Confirm gpt-4o model is deployed
- Check deployment name matches configuration
- Verify API key and endpoint are correct

**4. Deployment Timeout**
- Check Azure AI Foundry quota limits
- Verify model capacity is available
- Monitor Azure portal for deployment status

### Debug Commands:

```bash
# Check Azure login status
az account show

# List available AI Foundry projects
az ml workspace list --resource-group copilot-edmund

# Check model deployments
az ml online-deployment list --workspace-name edmund-tminus15-project --resource-group copilot-edmund

# View deployment logs
az ml online-deployment get-logs --name edmund-deployment --workspace-name edmund-tminus15-project --resource-group copilot-edmund
```

## 📈 Step 6: Scaling and Monitoring

### Auto-scaling Configuration
The deployment includes automatic scaling:
- **Min instances**: 1
- **Max instances**: 5
- **Scale trigger**: CPU > 70% or Request latency > 2s

### Monitoring Dashboards
- **Azure Monitor**: Application insights and metrics
- **AI Foundry Portal**: Usage analytics and performance
- **GitHub Actions**: Deployment history and status

## 🔒 Security Best Practices

1. **API Key Rotation**: Regularly rotate Azure OpenAI API keys
2. **Service Principal**: Use minimal required permissions
3. **Network Security**: Configure virtual network if needed
4. **Monitoring**: Enable Azure Monitor alerts
5. **Backup**: Regular backup of agent configurations

## 🎉 Success Checklist

- ✅ GitHub secrets configured correctly
- ✅ Azure resources verified and accessible
- ✅ Deployment workflow completed successfully
- ✅ Edmund responds to test requests
- ✅ Monitoring and alerts configured
- ✅ T-Minus-15 knowledge base accessible

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review Azure portal activity logs
3. Examine GitHub Actions workflow logs
4. Test individual components (Azure auth, model access, etc.)

---

**🚀 Once everything is working, Edmund will be ready to help your team implement the T-Minus-15 methodology!**