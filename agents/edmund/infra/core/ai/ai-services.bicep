param location string = resourceGroup().location
param tags object = {}

param hubName string
param projectName string
param keyVaultName string
param storageAccountName string
param containerRegistryName string
param applicationInsightsName string
param principalId string

// Create Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  tags: tags
  properties: {
    tenantId: subscription().tenantId
    sku: {
      name: 'standard'
      family: 'A'
    }
    accessPolicies: !empty(principalId) ? [
      {
        tenantId: subscription().tenantId
        objectId: principalId
        permissions: {
          keys: ['get', 'list']
          secrets: ['get', 'list', 'set']
          certificates: ['get', 'list']
        }
      }
    ] : []
    enableRbacAuthorization: true
  }
}

// Create Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  tags: tags
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
  }
}

// Create Container Registry for the AI Hub
resource aiContainerRegistry 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' = {
  name: containerRegistryName
  location: location
  tags: tags
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
  }
}

// Reference existing Application Insights
resource applicationInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: applicationInsightsName
}

// Create AI Hub (workspace)
resource aiHub 'Microsoft.MachineLearningServices/workspaces@2024-04-01' = {
  name: hubName
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  sku: {
    name: 'Basic'
    tier: 'Basic'
  }
  kind: 'Hub'
  properties: {
    friendlyName: hubName
    keyVault: keyVault.id
    storageAccount: storageAccount.id
    containerRegistry: aiContainerRegistry.id
    applicationInsights: applicationInsights.id
    hbiWorkspace: false
    managedNetwork: {
      isolationMode: 'Disabled'
    }
    publicNetworkAccess: 'Enabled'
  }
}

// Create AI Project (child workspace)
resource aiProject 'Microsoft.MachineLearningServices/workspaces@2024-04-01' = {
  name: projectName
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  sku: {
    name: 'Basic'
    tier: 'Basic'
  }
  kind: 'Project'
  properties: {
    friendlyName: projectName
    hubResourceId: aiHub.id
    managedNetwork: {
      isolationMode: 'Disabled'
    }
    publicNetworkAccess: 'Enabled'
  }
}

// Create OpenAI connection if principalId is provided
resource openAIConnection 'Microsoft.MachineLearningServices/workspaces/connections@2024-04-01' = if (!empty(principalId)) {
  parent: aiProject
  name: 'Default_AzureOpenAI'
  properties: {
    category: 'AzureOpenAI'
    target: 'https://eastus.api.cognitive.microsoft.com/'
    authType: 'AAD'
    isSharedToAll: true
    metadata: {
      ApiType: 'Azure'
      ResourceId: '/subscriptions/${subscription().subscriptionId}/resourceGroups/${resourceGroup().name}/providers/Microsoft.CognitiveServices/accounts/openai-${uniqueString(resourceGroup().id)}'
    }
  }
}

// Grant the principal AI Developer role on the project
resource principalProjectRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(principalId)) {
  name: guid(aiProject.id, principalId, subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '64702f94-c441-49e6-a78b-ef80e0188fee'))
  scope: aiProject
  properties: {
    principalId: principalId
    principalType: 'User'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '64702f94-c441-49e6-a78b-ef80e0188fee')
  }
}

// Grant the principal Storage Blob Data Contributor role on the storage account
resource principalStorageRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(principalId)) {
  name: guid(storageAccount.id, principalId, subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'))
  scope: storageAccount
  properties: {
    principalId: principalId
    principalType: 'User'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe')
  }
}

output hubName string = aiHub.name
output hubId string = aiHub.id
output projectName string = aiProject.name
output projectId string = aiProject.id
output projectConnectionString string = 'azureml://subscriptions/${subscription().subscriptionId}/resourcegroups/${resourceGroup().name}/providers/Microsoft.MachineLearningServices/workspaces/${aiProject.name}'
output keyVaultName string = keyVault.name
output storageAccountName string = storageAccount.name