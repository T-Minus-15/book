#!/usr/bin/env python3
"""
Scoring script for Edmund Agent deployment on Azure AI Foundry.
This script handles incoming requests and interfaces with the agent configuration.
"""

import os
import json
import logging
from typing import Dict, Any, List
import openai
from openai import AzureOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for model and configuration
client = None
agent_config = None

def init():
    """
    Initialize the model and configuration.
    This function is called when the deployment starts.
    """
    global client, agent_config
    
    try:
        # Load agent configuration
        config_path = os.getenv('AGENT_CONFIG_PATH', './agent-config.json')
        with open(config_path, 'r') as f:
            agent_config = json.load(f)
        
        # Initialize Azure OpenAI client
        client = AzureOpenAI(
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-12-01-preview'),
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
        )
        
        logger.info("Edmund Agent initialized successfully")
        logger.info(f"Model: {agent_config.get('model', {}).get('modelName', 'gpt-4o')}")
        
    except Exception as e:
        logger.error(f"Initialization failed: {str(e)}")
        raise


def run(raw_data: str) -> str:
    """
    Process incoming requests and return responses.
    
    Args:
        raw_data: JSON string containing the request data
        
    Returns:
        JSON string containing the response
    """
    try:
        # Parse the input
        data = json.loads(raw_data)
        logger.info(f"Received request: {data}")
        
        # Extract messages from the request
        messages = data.get('messages', [])
        if not messages:
            return json.dumps({
                "error": "No messages provided in the request"
            })
        
        # Add system prompt from agent configuration
        system_prompt = agent_config.get('instructions', {}).get('systemPrompt', '')
        if system_prompt:
            enhanced_messages = [
                {"role": "system", "content": system_prompt}
            ] + messages
        else:
            enhanced_messages = messages
        
        # Get model configuration
        model_config = agent_config.get('model', {})
        model_name = model_config.get('modelName', 'gpt-4o')
        temperature = model_config.get('temperature', 0.1)
        max_tokens = model_config.get('maxTokens', 4096)
        
        # Call Azure OpenAI
        response = client.chat.completions.create(
            model=model_name,
            messages=enhanced_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=model_config.get('topP', 0.95),
            frequency_penalty=model_config.get('frequencyPenalty', 0),
            presence_penalty=model_config.get('presencePenalty', 0)
        )
        
        # Extract the response content
        assistant_message = response.choices[0].message.content
        
        # Prepare the response
        result = {
            "response": assistant_message,
            "agent": {
                "name": agent_config.get('agent', {}).get('name', 'Edmund'),
                "displayName": agent_config.get('agent', {}).get('displayName', 'Edmund (the Engineer)'),
                "version": agent_config.get('agent', {}).get('version', '1.0.0')
            },
            "model": {
                "name": model_name,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        }
        
        logger.info(f"Response generated successfully. Tokens used: {response.usage.total_tokens}")
        return json.dumps(result)
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in request: {str(e)}")
        return json.dumps({
            "error": f"Invalid JSON format: {str(e)}"
        })
    
    except openai.OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        return json.dumps({
            "error": f"AI model error: {str(e)}"
        })
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return json.dumps({
            "error": f"Internal server error: {str(e)}"
        })


def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for the deployment.
    
    Returns:
        Dictionary containing health status
    """
    try:
        # Test that we can load the configuration
        if agent_config is None:
            return {
                "status": "unhealthy",
                "message": "Agent configuration not loaded"
            }
        
        # Test that we can connect to Azure OpenAI (optional test call)
        # Note: This is a simple check, could be enhanced with actual test call
        if client is None:
            return {
                "status": "unhealthy", 
                "message": "Azure OpenAI client not initialized"
            }
        
        return {
            "status": "healthy",
            "agent": {
                "name": agent_config.get('agent', {}).get('name', 'Edmund'),
                "version": agent_config.get('agent', {}).get('version', '1.0.0')
            },
            "model": agent_config.get('model', {}).get('modelName', 'gpt-4o')
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "message": f"Health check error: {str(e)}"
        }


if __name__ == "__main__":
    # For local testing
    init()
    
    # Test with sample data
    test_data = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "Hello Edmund, can you help me with a quick engineering question?"
            }
        ]
    })
    
    result = run(test_data)
    print("Test response:", result)