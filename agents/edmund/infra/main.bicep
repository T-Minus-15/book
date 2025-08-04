targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the environment which is used to generate a short unique hash used in all resources.')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

// Optional parameters
@description('Id of the user or app to assign application roles')
param principalId string = ''

// Variables
var abbrs = loadJsonContent('./abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = { 'azd-env-name': environmentName }

// Organize resources in a resource group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: '${abbrs.resourcesResourceGroups}${environmentName}'
  location: location
  tags: tags
}

// The application frontend
module api './app/api.bicep' = {
  name: 'api'
  scope: rg
  params: {
    name: '${abbrs.appContainerApps}api-${resourceToken}'
    location: location
    tags: tags
    identityName: '${abbrs.managedIdentityUserAssignedIdentities}api-${resourceToken}'
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    containerAppsEnvironmentName: containerApps.outputs.environmentName
    containerRegistryName: containerApps.outputs.registryName
    exists: false
    aiHubName: ai.outputs.hubName
    aiProjectName: ai.outputs.projectName
  }
}

// Create an App Service Plan to group applications under the same payment plan and deployment location
module containerApps './core/host/container-apps-environment.bicep' = {
  name: 'container-apps'
  scope: rg
  params: {
    name: '${abbrs.appManagedEnvironments}${resourceToken}'
    location: location
    tags: tags
    monitoring: monitoring.outputs
  }
}

// The application database
// Uncomment if you need a database
// module database './core/database/postgresql/flexibleserver.bicep' = {
//   name: 'database'
//   scope: rg
//   params: {
//     name: '${abbrs.dBforPostgreSQLServers}${resourceToken}'
//     location: location
//     tags: tags
//     sku: {
//       name: 'Standard_B1ms'
//       tier: 'Burstable'
//     }
//     storage: {
//       storageSizeGB: 32
//     }
//     version: '13'
//     authType: 'EntraID'
//     principalId: principalId
//     principalName: principalName
//   }
// }

// Monitor application with Azure Monitor
module monitoring './core/monitor/monitoring.bicep' = {
  name: 'monitoring'
  scope: rg
  params: {
    location: location
    tags: tags
    logAnalyticsName: '${abbrs.operationalInsightsWorkspaces}${resourceToken}'
    applicationInsightsName: '${abbrs.insightsComponents}${resourceToken}'
  }
}

// AI services
module ai './core/ai/ai-services.bicep' = {
  name: 'ai'
  scope: rg
  params: {
    location: location
    tags: tags
    hubName: '${abbrs.machineLearningServicesWorkspaces}hub-${resourceToken}'
    projectName: '${abbrs.machineLearningServicesWorkspaces}project-${resourceToken}'
    keyVaultName: '${abbrs.keyVaultVaults}${resourceToken}'
    storageAccountName: '${abbrs.storageStorageAccounts}${resourceToken}'
    containerRegistryName: '${abbrs.containerRegistryRegistries}${resourceToken}'
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    principalId: principalId
  }
}

// Data outputs
output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
output AZURE_RESOURCE_GROUP string = rg.name

// Generated outputs
output AZURE_CONTAINER_ENVIRONMENT_NAME string = containerApps.outputs.environmentName
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerApps.outputs.registryLoginServer
output AZURE_CONTAINER_REGISTRY_NAME string = containerApps.outputs.registryName

// AI outputs
output AZURE_AI_HUB_NAME string = ai.outputs.hubName
output AZURE_AI_PROJECT_NAME string = ai.outputs.projectName
output AZURE_AI_PROJECT_CONNECTION_STRING string = ai.outputs.projectConnectionString