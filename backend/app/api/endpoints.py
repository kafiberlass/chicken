"""
Все endpoints API
"""

from .health import router as health_router
from .credit_scoring import router as credit_scoring_router
from .clients import router as clients_router

__all__ = ["health_router", "credit_scoring_router", "clients_router"]
