from pydantic import BaseModel
from typing import List
from datetime import datetime

class ProductRecommendationResponse(BaseModel):
    id: int
    client_id: int
    product_name: str
    created_at: datetime

    class Config:
        from_attributes = True

class CreateRecommendationRequest(BaseModel):
    client_id: int
    product_name: str

class GenerateRecommendationsRequest(BaseModel):
    client_id: int

class GenerateRecommendationsResponse(BaseModel):
    client_id: int
    recommendations: List[str]

class PopularProductsResponse(BaseModel):
    products: List[str]
    count: int
