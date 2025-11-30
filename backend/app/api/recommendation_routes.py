from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..model.dto.recommendation_dto import (
    ProductRecommendationResponse, CreateRecommendationRequest,
    GenerateRecommendationsRequest, GenerateRecommendationsResponse,
    PopularProductsResponse
)
from ..service.product_recomendations_service import ProductRecommendationsService
from ..service.client_service import ClientService
from ..main import get_db

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/client/{client_id}", response_model=List[ProductRecommendationResponse])
async def get_client_recommendations(client_id: int, db: Session = Depends(get_db)):
    """Get all product recommendations for a specific client"""
    recommendations_service = ProductRecommendationsService(db)
    return recommendations_service.get_recommendations_for_client(client_id)

@router.post("/", response_model=ProductRecommendationResponse)
async def create_recommendation(request: CreateRecommendationRequest, db: Session = Depends(get_db)):
    """Create a new product recommendation for a client"""
    client_service = ClientService(db)
    recommendations_service = ProductRecommendationsService(db)

    # Verify client exists
    client = client_service.get_client_by_id(request.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return recommendations_service.create_recommendation(request.client_id, request.product_name)

@router.post("/generate", response_model=GenerateRecommendationsResponse)
async def generate_recommendations(request: GenerateRecommendationsRequest, db: Session = Depends(get_db)):
    """Generate product recommendations for a client based on their profile"""
    client_service = ClientService(db)
    recommendations_service = ProductRecommendationsService(db)

    # Verify client exists
    client = client_service.get_client_by_id(request.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    recommendations = recommendations_service.generate_recommendations_for_client(request.client_id)

    return GenerateRecommendationsResponse(
        client_id=request.client_id,
        recommendations=recommendations
    )

@router.get("/popular", response_model=PopularProductsResponse)
async def get_popular_products(limit: int = 10, db: Session = Depends(get_db)):
    """Get the most popular recommended products"""
    recommendations_service = ProductRecommendationsService(db)
    products = recommendations_service.get_popular_products(limit)

    return PopularProductsResponse(
        products=products,
        count=len(products)
    )

@router.get("/recent", response_model=List[ProductRecommendationResponse])
async def get_recent_recommendations(limit: int = 20, db: Session = Depends(get_db)):
    """Get the most recent recommendations across all clients"""
    recommendations_service = ProductRecommendationsService(db)
    return recommendations_service.get_recent_recommendations(limit)

@router.delete("/{recommendation_id}")
async def delete_recommendation(recommendation_id: int, db: Session = Depends(get_db)):
    """Delete a specific recommendation"""
    recommendations_service = ProductRecommendationsService(db)

    success = recommendations_service.delete_recommendation(recommendation_id)

    if not success:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    return {"message": "Recommendation deleted successfully"}
