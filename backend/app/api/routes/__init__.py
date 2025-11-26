"""
API routes module for Polix backend.
"""
from .health import router as health_router
from .query import router as query_router
from .agent import router as agent_router

__all__ = ["health_router", "query_router", "agent_router"]

