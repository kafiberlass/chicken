"""
Основное FastAPI приложение Альфа-доходы
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .endpoints import health, credit_scoring, clients

# Создание FastAPI приложения
app = FastAPI(
    title="Альфа-доходы",
    description="API для предсказания доходов и кредитного скоринга клиентов",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(credit_scoring.router, prefix="/api/v1", tags=["credit-scoring"])
app.include_router(clients.router, prefix="/api/v1", tags=["clients"])

@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "message": "Альфа-доходы API",
        "version": "1.0.0",
        "docs": "/docs"
    }
