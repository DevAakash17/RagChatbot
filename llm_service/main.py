"""
Main application entry point.
"""
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from chatbot.llm_service.api.routes import router as api_router
from chatbot.llm_service.config.settings import settings
from chatbot.llm_service.utils.errors import LLMServiceError
from chatbot.llm_service.utils.logging import setup_logging


logger = setup_logging(__name__)


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        openapi_url="/openapi.json",
        docs_url="/docs",
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add exception handlers
    @app.exception_handler(LLMServiceError)
    async def llm_service_error_handler(request: Request, exc: LLMServiceError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.message,
                "status_code": exc.status_code,
                "details": exc.details
            }
        )
    
    # Include API routes
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "ok"}

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "Welcome to the Embedding Service",
            "docs": "/docs",
            "health": "/health"
        }
    
    return app


app = create_application()


if __name__ == "__main__":
    logger.info(f"Starting {settings.PROJECT_NAME}")
    uvicorn.run(
        "chatbot.llm_service.main:app",
        host="0.0.0.0",
        port=8001,
        reload=settings.DEBUG
    )
