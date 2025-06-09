# Edmund (the Engineer) - Azure AI Foundry Agent

Edmund is an AI agent specialized in development tasks and deeply versed in the T-Minus-15 methodology. This directory contains all the necessary configuration and deployment files for deploying Edmund to Azure AI Foundry.

## 🚀 Quick Start

### Prerequisites
- Azure subscription with AI Foundry access
- Azure CLI installed and configured
- GitHub repository access
- Required secrets configured in GitHub repository

### Deploy Edmund
```bash
# Trigger deployment via GitHub Actions
gh workflow run deploy-edmund.yml

# Or deploy to specific environment
gh workflow run deploy-edmund.yml -f environment=development
```

## 📁 Directory Structure

```
/agents/edmund/
├── edmund.md                    # Agent personality, role, and capabilities
├── agent-config.json           # Azure AI Foundry agent configuration
├── knowledge-sources.json      # Knowledge base configuration
├── deployment.yaml             # Kubernetes deployment manifest
├── requirements.txt            # Python dependencies
├── mcp-config.json             # MCP server configurations (future)
└── README.md                   # This documentation
```

## 🤖 About Edmund

Edmund is the Engineer in the T-Minus-15 methodology team. He specializes in:

- **Code Development**: Writing clean, maintainable, and scalable code
- **DevOps Implementation**: CI/CD pipelines, infrastructure-as-code, automation
- **Architecture & Design**: Solution architecture and technical design decisions
- **Code Reviews**: Thorough, constructive feedback on code quality
- **Technical Problem Solving**: Debugging and optimizing system performance
- **T-Minus-15 Expertise**: Deep knowledge of the 15-step methodology

### Key Capabilities
- Infrastructure-as-Code guidance
- CI/CD pipeline setup and optimization
- Code quality and security reviews
- Performance optimization
- Test automation strategies
- API design and microservices architecture

## ⚙️ Configuration

### Agent Configuration (`agent-config.json`)
- **Model**: GPT-4 Turbo via Azure OpenAI
- **Temperature**: 0.1 (focused, deterministic responses)
- **Knowledge Source**: Auto-indexed from https://github.com/bengweeks/T-Minus-15
- **Security**: Content filtering, sensitive data detection, rate limiting

### Knowledge Sources (`knowledge-sources.json`)
- **Primary**: T-Minus-15 methodology repository (daily refresh)
- **Secondary**: Azure AI Foundry documentation (weekly refresh)
- **Tertiary**: DevOps best practices from industry sources

### Deployment (`deployment.yaml`)
- **Platform**: Azure AI Foundry + Kubernetes
- **Scaling**: 1-3 replicas with auto-scaling
- **Monitoring**: Health checks, telemetry, metrics collection
- **Security**: Managed identity, TLS, content filtering

## 🔧 MCP Server Integrations (Future)

Edmund is configured with placeholder MCP (Model Context Protocol) server integrations for:

- **Azure DevOps**: Work items, pipelines, repositories, pull requests
- **GitHub**: Issues, pull requests, actions, repository management  
- **Docker Registry**: Container image management
- **Kubernetes**: Cluster and resource management

These integrations are disabled by default and can be enabled when MCP servers are deployed.

## 🚀 Deployment Process

### Automatic Deployment
The deployment is fully automated via GitHub Actions:

1. **Validation**: Configuration files are validated for syntax and completeness
2. **Security Scan**: Code is scanned for security vulnerabilities and secrets
3. **Package Creation**: Deployment package is created with environment variables
4. **Azure Deployment**: Agent is deployed to Azure AI Foundry
5. **Health Check**: Post-deployment verification and health checks

### Manual Deployment
For manual deployment or troubleshooting:

```bash
# 1. Ensure Azure CLI is logged in
az login

# 2. Create or verify resource group
az group create --name tminus15-dev-rg --location eastus

# 3. Create or verify AI Foundry workspace
az ml workspace create \
  --resource-group tminus15-dev-rg \
  --name tminus15-ai-workspace \
  --location eastus

# 4. Deploy Edmund agent
az ml model create \
  --resource-group tminus15-dev-rg \
  --workspace-name tminus15-ai-workspace \
  --name edmund \
  --version 1.0.0 \
  --path ./agents/edmund \
  --type agent
```

## 🔒 Security Configuration

### Required Secrets
Configure these secrets in your GitHub repository:

```bash
# Azure credentials
AZURE_CREDENTIALS          # Service principal credentials JSON
AZURE_SUBSCRIPTION_ID      # Azure subscription ID
AZURE_TENANT_ID            # Azure tenant ID  
AZURE_CLIENT_ID            # Azure client ID

# GitHub access
GITHUB_TOKEN               # GitHub personal access token

# Future MCP integrations
AZURE_DEVOPS_PAT          # Azure DevOps personal access token
DOCKER_REGISTRY_USERNAME   # Docker registry username
DOCKER_REGISTRY_PASSWORD   # Docker registry password
```

### Security Features
- **Content Filtering**: Strict content filtering enabled
- **Sensitive Data Detection**: Automatic detection of API keys, passwords, secrets
- **Rate Limiting**: 60 requests/minute, 1000 requests/hour
- **Authentication**: Managed identity for Azure services
- **TLS Encryption**: All communications encrypted in transit
- **Token Encryption**: MCP tokens encrypted using Azure Key Vault

## 📊 Monitoring & Observability

### Metrics Collected
- Response time and latency
- Token usage and costs
- User satisfaction scores
- Error rates and failure modes
- Knowledge retrieval accuracy

### Health Checks
- **Endpoint**: `/health`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Failure Threshold**: 3 consecutive failures

### Logging
- **Level**: Info (configurable)
- **Export**: Azure Monitor + Application Insights
- **Retention**: 30 days for conversations, 90 days for knowledge cache

## 🔄 Knowledge Management

### Auto-Refresh Schedule
- **T-Minus-15 Repository**: Daily at 02:00 UTC
- **Azure Documentation**: Weekly at 03:00 UTC
- **DevOps Best Practices**: Weekly at 04:00 UTC

### Webhook Triggers
- GitHub repository push events trigger immediate re-indexing
- Pull request events update knowledge base for review

### Fallback Mechanisms
- Cached T-Minus-15 methodology snapshot available offline
- Graceful degradation when external sources are unavailable

## 🌐 Environments

### Development
- **URL**: https://edmund-dev.tminus15.azure.com
- **Resource Group**: tminus15-dev-rg
- **Auto-deploy**: On push to main branch

### Staging
- **URL**: https://edmund-staging.tminus15.azure.com
- **Resource Group**: tminus15-staging-rg
- **Deploy**: Manual trigger via workflow_dispatch

### Production
- **URL**: https://edmund-prod.tminus15.azure.com
- **Resource Group**: tminus15-prod-rg
- **Deploy**: Manual trigger after staging validation

## 🛠️ Development & Customization

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your actual API keys and configuration

# Run configuration tests
python test_config.py

# Run interactive AI tests
python test_edmund_local.py

# Run comprehensive tests
pytest tests/ -v
```

### Customizing Edmund
1. **Personality**: Edit `edmund.md` to adjust personality and capabilities
2. **Configuration**: Modify `agent-config.json` for model parameters
3. **Knowledge Sources**: Update `knowledge-sources.json` for additional sources
4. **Deployment**: Adjust `deployment.yaml` for scaling and resource limits

### Adding New Tools
1. Define tools in `agent-config.json`
2. Add MCP server configuration in `mcp-config.json`
3. Update security permissions as needed
4. Test integration thoroughly before production deployment

## 🐛 Troubleshooting

### Common Issues
1. **Deployment Failures**: Check Azure credentials and permissions
2. **Knowledge Source Errors**: Verify GitHub repository access
3. **Performance Issues**: Review scaling configuration and resource limits
4. **Authentication Errors**: Ensure managed identity is properly configured

### Debug Commands
```bash
# Check agent status
az ml model show --name edmund --version 1.0.0

# View deployment logs
kubectl logs -l app=edmund -n tminus15-agents

# Test knowledge source access
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/bengweeks/T-Minus-15
```

## 📚 Related Documentation

- [T-Minus-15 Methodology](https://github.com/bengweeks/T-Minus-15)
- [Azure AI Foundry Documentation](https://docs.microsoft.com/en-us/azure/ai-foundry/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [GitHub Actions Workflows](../../.github/workflows/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/edmund-enhancement`)
3. Make your changes and test thoroughly
4. Commit your changes (`git commit -am 'Add Edmund enhancement'`)
5. Push to the branch (`git push origin feature/edmund-enhancement`)
6. Create a Pull Request

## 📄 License

This project is licensed under the same license as the T-Minus-15 methodology repository.

---

## 🚀 T-Minus-15: From Idea to Production in 15 Steps

Edmund is part of the T-Minus-15 methodology - a practical framework for elite DevOps teams. Learn more about the complete methodology at [T-Minus-15](https://github.com/bengweeks/T-Minus-15).

**The Avengers of Agile Team:**
- 🎯 **Pepper (Prepper)**: Requirements analysis and backlog management
- 🎨 **Danny (Designer)**: UX/UI design and solution architecture  
- ⚙️ **Edmund (Engineer)**: Development and DevOps implementation
- 🧪 **Teddy (Tester)**: Quality assurance and testing
- 🚀 **Ollie (Operator)**: Deployment and operations
- 📋 **Poppy (Planner)**: Project planning and coordination