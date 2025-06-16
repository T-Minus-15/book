"""
Edmund the Engineer - T-Minus-15 AI Agent
Main FastAPI application entry point for Azure Container Apps deployment
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Application lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown"""
    logger.info("Starting Edmund the Engineer AI Agent")
    
    # Initialize Azure AI Foundry connection
    try:
        # This would initialize the AI Foundry project connection
        logger.info("Initializing Azure AI Foundry connection...")
        # await initialize_ai_foundry()
    except Exception as e:
        logger.error(f"Failed to initialize AI Foundry: {e}")
    
    yield
    
    logger.info("Shutting down Edmund the Engineer AI Agent")

# Create FastAPI application
app = FastAPI(
    title="Edmund the Engineer",
    description="T-Minus-15 AI Agent for DevOps and Engineering Excellence",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint"""
    return {
        "message": "Edmund the Engineer - T-Minus-15 AI Agent",
        "status": "operational",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for container orchestration"""
    try:
        # Add any health checks here (database connections, AI service availability, etc.)
        return {
            "status": "healthy",
            "service": "edmund-agent",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.get("/config")
async def get_config() -> Dict[str, Any]:
    """Get current configuration (non-sensitive data only)"""
    return {
        "agent_name": "Edmund the Engineer",
        "specialization": "DevOps and Engineering Excellence",
        "ai_foundry_enabled": bool(os.getenv("AZURE_AI_PROJECT_CONNECTION_STRING")),
        "environment": os.getenv("AZURE_ENV_NAME", "development"),
        "features": [
            "Azure DevOps Integration",
            "Engineering Best Practices",
            "CI/CD Pipeline Optimization",
            "Code Quality Analysis",
            "Technical Documentation"
        ]
    }

@app.post("/chat")
async def chat(message: Dict[str, str]) -> Dict[str, str]:
    """Chat endpoint for interacting with Edmund"""
    try:
        user_message = message.get("message", "")
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # This is where you would integrate with Azure AI Foundry
        # For now, return a simple response
        response = f"Edmund here! I received your message: '{user_message}'. "
        response += "I'm ready to help with DevOps and engineering excellence!"
        
        return {
            "response": response,
            "agent": "Edmund the Engineer",
            "timestamp": "2024-01-01T00:00:00Z"  # You'd use actual timestamp
        }
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/capabilities")
async def get_capabilities() -> Dict[str, Any]:
    """Get Edmund's capabilities and specializations"""
    return {
        "primary_role": "DevOps and Engineering Excellence",
        "capabilities": [
            "Azure DevOps pipeline optimization",
            "CI/CD best practices implementation",
            "Code quality and security analysis",
            "Infrastructure as Code (IaC) guidance",
            "Git workflow optimization",
            "Technical documentation generation",
            "Performance monitoring and optimization",
            "Cloud architecture recommendations"
        ],
        "knowledge_domains": [
            "Azure DevOps Services",
            "Azure Resource Manager",
            "Docker and Kubernetes",
            "Git and version control",
            "Software development lifecycle",
            "Agile and DevOps methodologies",
            "Security best practices",
            "Monitoring and observability"
        ],
        "integration_points": [
            "Azure AI Foundry",
            "Azure DevOps",
            "GitHub",
            "Azure Monitor",
            "Azure Key Vault"
        ]
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        reload=False  # Set to True for development
    )