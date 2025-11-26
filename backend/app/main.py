"""
Main FastAPI application for Polix backend.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.routes import health_router, query_router, agent_router
from app.core.config import settings
from app.core.logger import get_logger, setup_logging
from app.rag.vectorstore import initialize_vectorstore
from app.mcp.mcp_loader import register_mcp_tools

# Initialize logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    
    Args:
        app: FastAPI application instance
    """
    # Startup
    logger.info("Starting Polix backend...")
    
    try:
        # Initialize vector store
        logger.info("Initializing vector store...")
        initialize_vectorstore()
        logger.info("Vector store initialized")
        
        # Register MCP tools
        if settings.mcp_enabled:
            logger.info("Registering MCP tools...")
            tools = register_mcp_tools()
            logger.info(f"Registered {len(tools)} MCP tools")
        
        logger.info("Polix backend started successfully")
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}", exc_info=True)
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Polix backend...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Polix - Agentic AI Compliance Audit System",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(query_router)
app.include_router(agent_router)


@app.get("/")
async def root():
    """
    Root endpoint.
    
    Returns:
        Welcome message
    """
    return {
        "message": "Welcome to Polix API",
        "version": settings.app_version,
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )

