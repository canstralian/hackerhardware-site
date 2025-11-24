"""
HackerHardware.net - FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from routers import health, nodes, security, intelligence
from core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("Starting HackerHardware.net API")
    yield
    logger.info("Shutting down HackerHardware.net API")


# Initialize FastAPI app
app = FastAPI(
    title="HackerHardware.net API",
    description="Living edge-intelligence ecosystem API",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(nodes.router, prefix="/api/v1/nodes", tags=["nodes"])
app.include_router(security.router, prefix="/api/v1/security", tags=["security"])
app.include_router(intelligence.router, prefix="/api/v1/intelligence", tags=["intelligence"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "HackerHardware.net API",
        "version": "1.0.0",
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
