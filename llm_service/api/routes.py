"""
API routes for the LLM service.
"""
from fastapi import APIRouter, HTTPException, Depends, status
from chatbot.llm_service.api.schemas import HealthResponse

from chatbot.llm_service.api.schemas import (
    GenerateTextRequest,
    GenerateTextResponse,
    ErrorResponse,
    TokenUsage
)
from chatbot.llm_service.core.services.llm_service import LLMService
from chatbot.llm_service.utils.errors import LLMServiceError
from chatbot.llm_service.utils.logging import setup_logging


logger = setup_logging(__name__)
router = APIRouter()


@router.post(
    "/generate",
    response_model=GenerateTextResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Generate text",
    description="Generate text based on the input prompt using the specified model."
)
async def generate_text(request: GenerateTextRequest):
    """
    Generate text based on the input prompt.
    
    Args:
        request: Text generation request.
        
    Returns:
        Generated text and metadata.
    """
    try:
        logger.info(f"Received text generation request for model: {request.model}")
        
        result = await LLMService.generate_text(
            prompt=request.prompt,
            model_name=request.model,
            options=request.options
        )
        
        # Convert the result to the response schema
        response = GenerateTextResponse(
            text=result["text"],
            model=result["model"],
            usage=TokenUsage(**result["usage"]),
            finish_reason=result.get("finish_reason")
        )
        
        logger.info(f"Successfully generated text with model: {request.model}")
        return response
        
    except LLMServiceError as e:
        logger.error(f"LLM service error: {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail={
                "message": e.message,
                "status_code": e.status_code,
                "details": e.details
            }
        )
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": f"Unexpected error: {str(e)}",
                "status_code": 500,
                "details": {}
            }
        )


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check the health of the service."
)
async def health_check(
        service: LLMService = Depends(generate_text)
):
    """Health check."""
    try:
        health_info = service.get_health_info()

        return HealthResponse(**health_info)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Health check failed: {str(e)}"}
        )