from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/chicken_db")

# Application configuration
APP_NAME = os.getenv("APP_NAME", "Chicken ML API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# CORS configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080")
allowed_origins = [origin.strip() for origin in ALLOWED_ORIGINS.split(",")] if ALLOWED_ORIGINS else ["*"]

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI app
app = FastAPI(
    title=APP_NAME,
    description="Machine Learning API for income prediction and product recommendations",
    version=APP_VERSION,
    debug=DEBUG
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Chicken ML API is running"}

# Import API routes
from .api.client_routes import router as client_router
from .api.recommendation_routes import router as recommendation_router
from .api.income_prediction_routes import router as prediction_router

# Include API routes
app.include_router(client_router)
app.include_router(recommendation_router)
app.include_router(prediction_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
