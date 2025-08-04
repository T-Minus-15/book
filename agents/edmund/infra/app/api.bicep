param name string
param location string = resourceGroup().location
param tags object = {}

param identityName string
param applicationInsightsName string
param containerAppsEnvironmentName string
param containerRegistryName string
param exists bool
param aiHubName string
param aiProjectName string

@description('CPU cores allocated to a single container instance, e.g., 0.5')
param containerCpuCoreCount string = '0.5'

@description('Memory allocated to a single container instance, e.g., 1Gi')
param containerMemory string = '1.0Gi'

@description('The maximum number of replicas to run. Must not be set to 0.')
param containerMaxReplicas int = 10

@description('The minimum number of replicas to run')
param containerMinReplicas int = 1

@description('The name of the container')
param containerName string = 'main'

@description('The environment variables for the container')
param env array = []

@description('The name of the container image')
param imageName string = ''

@description('The secrets required for the container')
param secrets array = []

@description('The service binds associated with the container')
param serviceBinds array = []

@description('The target port for the container')
param targetPort int = 8000

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: identityName
  location: location
  tags: tags
}

resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' existing = {
  name: containerAppsEnvironmentName
}

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' existing = {
  name: containerRegistryName
}

resource applicationInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: applicationInsightsName
}

resource aiHub 'Microsoft.MachineLearningServices/workspaces@2024-04-01' existing = {
  name: aiHubName
}

resource aiProject 'Microsoft.MachineLearningServices/workspaces@2024-04-01' existing = {
  name: aiProjectName
}

resource app 'Microsoft.App/containerApps@2023-05-01' = {
  name: name
  location: location
  tags: union(tags, {'azd-service-name': 'api'})
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${identity.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: containerAppsEnvironment.id
    configuration: {
      ingress: {
        external: true
        targetPort: targetPort
        transport: 'http'
        allowInsecure: false
      }
      registries: [
        {
          server: containerRegistry.properties.loginServer
          identity: identity.id
        }
      ]
      secrets: union([
        {
          name: 'azure-ai-project-connection-string'
          value: aiProject.properties.discoveryUrl
        }
        {
          name: 'applicationinsights-connection-string'
          value: applicationInsights.properties.ConnectionString
        }
      ], secrets)
    }
    template: {
      containers: [
        {
          image: !empty(imageName) ? imageName : 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
          name: containerName
          env: union([
            {
              name: 'AZURE_CLIENT_ID'
              value: identity.properties.clientId
            }
            {
              name: 'AZURE_AI_PROJECT_CONNECTION_STRING'
              secretRef: 'azure-ai-project-connection-string'
            }
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              secretRef: 'applicationinsights-connection-string'
            }
            {
              name: 'PORT'
              value: string(targetPort)
            }
          ], env)
          resources: {
            cpu: json(containerCpuCoreCount)
            memory: containerMemory
          }
        }
      ]
      scale: {
        minReplicas: containerMinReplicas
        maxReplicas: containerMaxReplicas
      }
      serviceBinds: serviceBinds
    }
  }
}

// Grant the identity containerRegistry pull permissions
resource containerRegistryPullRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(containerRegistry.id, identity.id, subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d'))
  scope: containerRegistry
  properties: {
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId:  subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
  }
}

// Grant the identity AI Developer permissions on the AI project
resource aiProjectDeveloperRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(aiProject.id, identity.id, subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '64702f94-c441-49e6-a78b-ef80e0188fee'))
  scope: aiProject
  properties: {
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '64702f94-c441-49e6-a78b-ef80e0188fee')
  }
}

output defaultDomain string = app.properties.configuration.ingress.fqdn
output identityPrincipalId string = identity.properties.principalId
output imageName string = imageName
output name string = app.name
output uri string = 'https://${app.properties.configuration.ingress.fqdn}'