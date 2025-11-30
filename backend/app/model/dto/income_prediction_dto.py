from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class IncomePredictionResponse(BaseModel):
    id: int
    client_id: int
    predicted_income: float
    created_at: datetime

    class Config:
        from_attributes = True

class CreateIncomePredictionRequest(BaseModel):
    client_id: int
    predicted_income: float

class IncomePredictionFilter(BaseModel):
    client_id: Optional[int] = None
    min_predicted_income: Optional[float] = None
    max_predicted_income: Optional[float] = None
    limit: Optional[int] = None

class IncomePredictionsListResponse(BaseModel):
    predictions: List[IncomePredictionResponse]
    total_count: int

class IncomePredictionStatistics(BaseModel):
    total_predictions: int
    average_predicted_income: float
    min_predicted_income: float
    max_predicted_income: float
    predictions_per_client_avg: float
