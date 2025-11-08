"""
HackerHardware.net - FastAPI Backend
Main application entry point with modular routing and middleware
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from backend.api.v1 import router as api_v1_router
from backend.middleware.security import SecurityHeadersMiddleware
from backend.middleware.rate_limit import RateLimitMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan manager for startup/shutdown tasks."""
    # Startup
    print("🚀 HackerHardware.net API starting...")
    yield
    # Shutdown
    print("🔌 HackerHardware.net API shutting down...")


# Initialize FastAPI application
app = FastAPI(
    title="HackerHardware.net API",
    description="Edge autonomy infrastructure - API layer",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan,
)


# ============================================
# Middleware Configuration
# ============================================

# Security headers
app.add_middleware(SecurityHeadersMiddleware)

# Rate limiting
app.add_middleware(RateLimitMiddleware)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hackerhardware.net",
        "https://*.hackerhardware.net",
        "http://localhost:3000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-RateLimit-Remaining"],
)

# Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Trusted host protection
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "hackerhardware.net",
        "*.hackerhardware.net",
        "localhost",
        "127.0.0.1",
    ],
)


# ============================================
# Exception Handlers
# ============================================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle 404 Not Found errors."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "path": str(request.url.path),
        },
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Handle 500 Internal Server Error."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
        },
    )


# ============================================
# API Routes
# ============================================

# Include v1 API routes
app.include_router(api_v1_router, prefix="/api/v1")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "HackerHardware.net API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/v1/docs",
        "architecture": "edge autonomy infrastructure",
    }


# ============================================
# Application Entry Point
# ============================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True,
    )
