from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..model.dto.income_prediction_dto import (
    IncomePredictionsListResponse,
    IncomePredictionStatistics
)
from ..service.income_prediction_service import IncomePredictionService
from ..main import get_db

router = APIRouter(prefix="/predictions", tags=["income-predictions"])

@router.get("/", response_model=IncomePredictionsListResponse)
async def find_all_predictions(
    client_id: Optional[int] = Query(None, description="Filter by client ID"),
    min_predicted_income: Optional[float] = Query(None, description="Minimum predicted income filter"),
    max_predicted_income: Optional[float] = Query(None, description="Maximum predicted income filter"),
    limit: Optional[int] = Query(None, description="Limit number of results"),
    db: Session = Depends(get_db)
):
    prediction_service = IncomePredictionService(db)
    predictions = prediction_service.find_all_predictions(
        client_id=client_id,
        min_predicted_income=min_predicted_income,
        max_predicted_income=max_predicted_income,
        limit=limit
    )

    return IncomePredictionsListResponse(
        predictions=predictions,
        total_count=len(predictions)
    )

@router.get("/statistics", response_model=IncomePredictionStatistics)
async def get_prediction_statistics(db: Session = Depends(get_db)):
    """Get statistics about income predictions"""
    prediction_service = IncomePredictionService(db)
    return prediction_service.get_prediction_statistics()
