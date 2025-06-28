import os
import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Dict, Any
from dotenv import load_dotenv

from .api.routes import router as api_router
from .core.mcp_server import MCPServer
from .integrations.integration_manager import IntegrationManager

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mcp_server")

# Global instances
integration_manager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for the FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Initializing MCP Server...")
    
    # Initialize integration manager
    global integration_manager
    integration_manager = IntegrationManager(
        api_key=os.getenv("DEEPSEEK_API_KEY", "sk-1bd5de3f31db429cb8cbe73875537c5c")
    )
    
    try:
        await integration_manager.initialize()
        logger.info("Integrations initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize integrations: {str(e)}")
        raise
    
    try:
        yield
    except GeneratorExit:
        # Properly handle generator exit
        pass
    finally:
        # Shutdown
        logger.info("Shutting down MCP Server...")
        if integration_manager:
            await integration_manager.close()
        integration_manager = None

# Initialize FastAPI application
app = FastAPI(
    title="Advanced MCP SQLMap Server",
    description="Advanced Model Context Protocol server for vulnerability discovery using SQLMap",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

# Additional routes for server management
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Advanced MCP SQLMap Server",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/status")
async def get_status():
    """Get server status"""
    try:
        # Simulate an error for testing
        if os.getenv("SIMULATE_STATUS_ERROR"):
            raise Exception("Simulated status error")
            
        return {
            "status": "healthy",
            "integrations": {
                "langchain": integration_manager is not None,
                "openwebui": integration_manager is not None
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting server status: {str(e)}"
        )

def start_server(host: str = "0.0.0.0", 
                 port: int = 8000, 
                 reload: bool = False,
                 config: Dict[str, Any] = None):
    """
    Start the MCP server
    
    Args:
        host: Host to bind the server to
        port: Port to run the server on
        reload: Enable auto-reload for development
        config: Additional configuration options
    """
    try:
        # Check environment variables
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            logger.warning("DEEPSEEK_API_KEY not found in environment variables")
        
        # Apply configuration if provided
        if config:
            for key, value in config.items():
                setattr(app.state, key, value)
        
        # Start server
        uvicorn.run(
            "server.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
        
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise RuntimeError("Failed to start server") from e

if __name__ == "__main__":
    # Load environment variables
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        logger.warning("DEEPSEEK_API_KEY not found in environment variables")
    
    # Start server with default configuration
    start_server(reload=True)
