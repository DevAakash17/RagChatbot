"""
Main entry point for the Chunker Service.
"""
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from typing import Dict, Any

from chunker_service.api.routes import router as api_router
from chunker_service.core.config import settings
from chunker_service.core.logging import setup_logging
from chunker_service.core.errors import ChunkerServiceError


# Setup logging
logger = setup_logging()

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for chunking documents and storing embeddings",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log requests and responses."""
    start_time = time.time()

    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")

    # Process request
    try:
        response = await call_next(request)

        # Log response
        process_time = time.time() - start_time
        logger.info(f"Response: {response.status_code} ({process_time:.4f}s)")

        return response
    except Exception as e:
        # Log error
        process_time = time.time() - start_time
        logger.error(f"Error: {str(e)} ({process_time:.4f}s)")

        # Return error response
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error"}
        )


@app.exception_handler(ChunkerServiceError)
async def chunker_service_error_handler(request: Request, exc: ChunkerServiceError):
    """Handle ChunkerServiceError exceptions."""
    logger.error(f"ChunkerServiceError: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "details": exc.details}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to the Chunker Service",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health"
    }


if __name__ == "__main__":
    """Run the application."""
    uvicorn.run(
        "chunker_service.main:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )
