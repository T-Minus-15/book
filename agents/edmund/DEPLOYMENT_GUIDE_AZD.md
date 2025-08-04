# Edmund Agent - Azure Developer CLI Deployment Guide

This guide covers deploying Edmund the Engineer AI Agent using Azure Developer CLI (azd) with Bicep templates and Azure AI Foundry.

## Prerequisites

1. **Azure CLI** installed and authenticated
2. **Azure Developer CLI (azd)** installed
3. **Docker** installed for local testing
4. **Azure subscription** with appropriate permissions
5. **Python 3.11+** for local development

## Quick Start

1. **Initialize the project:**
   ```bash
   cd agents/edmund
   azd init
   ```

2. **Set your environment:**
   ```bash
   azd env new edmund-dev
   azd env select edmund-dev
   ```

3. **Deploy to Azure:**
   ```bash
   azd up
   ```

## Detailed Setup

### 1. Environment Configuration

Copy the environment template:
```bash
cp .env.example .env
```

Set your Azure environment variables:
```bash
azd env set AZURE_LOCATION eastus
azd env set AZURE_SUBSCRIPTION_ID <your-subscription-id>
```

### 2. Infrastructure Deployment

The Bicep templates will create:
- **Resource Group** for all resources
- **Azure AI Foundry Hub** for AI model management
- **Azure AI Foundry Project** for Edmund's workspace
- **Container Apps Environment** for hosting
- **Container Registry** for Docker images
- **Key Vault** for secrets management
- **Storage Account** for AI Foundry data
- **Application Insights** for monitoring
- **Log Analytics Workspace** for logging

Deploy infrastructure only:
```bash
azd provision
```

### 3. Application Deployment

Build and deploy the Edmund agent:
```bash
azd deploy
```

Or do both provision and deploy:
```bash
azd up
```

### 4. Verify Deployment

Check the deployment:
```bash
azd show
```

Get the application URL:
```bash
azd env get-values | grep URI
```

Test the health endpoint:
```bash
curl https://<your-app-url>/health
```

## Local Development

### Running Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure credentials
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

4. **Test locally:**
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/capabilities
   ```

### Docker Development

Build and run with Docker:
```bash
docker build -t edmund-agent .
docker run -p 8000:8000 --env-file .env edmund-agent
```

## Configuration

### Environment Variables

Key environment variables (set via `azd env set`):

- `AZURE_ENV_NAME`: Environment name (e.g., "edmund-dev")
- `AZURE_LOCATION`: Azure region (e.g., "eastus")
- `AZURE_SUBSCRIPTION_ID`: Your Azure subscription ID
- `AZURE_PRINCIPAL_ID`: Your user object ID for permissions

### AI Foundry Configuration

The deployment automatically creates:
- AI Foundry Hub with shared resources
- AI Foundry Project for Edmund's workspace
- OpenAI connection (requires manual setup for models)
- Proper RBAC permissions for the agent

## Monitoring and Troubleshooting

### View Logs

```bash
# Container Apps logs
az containerapp logs show --name <container-app-name> --resource-group <resource-group>

# Application Insights logs via portal
# Navigate to your Application Insights resource
```

### Common Issues

1. **Authentication errors:**
   - Ensure you're logged in: `az login`
   - Check subscription: `az account show`

2. **Permission errors:**
   - Verify you have Contributor access to the subscription
   - Check that `AZURE_PRINCIPAL_ID` is set correctly

3. **Container deployment failures:**
   - Check Docker build: `docker build -t test .`
   - Verify requirements.txt dependencies

4. **AI Foundry connection issues:**
   - Verify the AI project was created successfully
   - Check that model deployments are available

### Useful Commands

```bash
# Show environment details
azd env get-values

# Redeploy just the application
azd deploy api

# Clean up resources
azd down --force --purge

# View resource group in portal
azd show --output json | jq -r '.services.api.resourceGroupName'
```

## Customization

### Adding New Dependencies

1. Update `requirements.txt`
2. Rebuild and redeploy:
   ```bash
   azd deploy
   ```

### Infrastructure Changes

1. Modify Bicep templates in `infra/`
2. Provision updates:
   ```bash
   azd provision
   ```

### Environment-Specific Settings

Create multiple environments:
```bash
azd env new edmund-prod
azd env select edmund-prod
azd env set AZURE_LOCATION westus2
azd up
```

## Security Considerations

- Secrets are stored in Azure Key Vault
- Container Apps uses managed identity for authentication
- Network access is controlled through Container Apps ingress
- Application Insights data is encrypted at rest
- RBAC permissions follow least-privilege principle

## Cost Optimization

- Container Apps scales to zero when not in use
- Basic SKUs are used for development environments
- Log Analytics has 30-day retention by default
- Consider upgrading to Standard SKUs for production workloads

## Next Steps

1. Configure OpenAI models in AI Foundry
2. Set up CI/CD pipelines with GitHub Actions
3. Implement proper monitoring and alerting
4. Add authentication and authorization
5. Configure custom domain and SSL certificates

For more advanced configuration, see the individual Bicep templates in the `infra/` directory.