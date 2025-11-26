"""
Health check endpoint for Polix backend.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Literal

router = APIRouter(prefix="/health", tags=["health"])


class HealthResponse(BaseModel):
    """Health check response model."""
    status: Literal["ok"]
    message: str


@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Simple health check endpoint.
    
    Returns:
        HealthResponse: Status OK with message
    """
    return HealthResponse(status="ok", message="Polix backend is running")

