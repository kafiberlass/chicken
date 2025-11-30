from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..model.dto.client_dto import (
    ClientResponse, ClientSearchRequest, ClientStatisticsResponse
)
from ..model.dto.income_prediction_dto import (
    IncomePredictionResponse, CreateIncomePredictionRequest
)
from ..service.client_service import ClientService
from ..service.income_prediction_service import IncomePredictionService
from ..main import get_db

router = APIRouter(prefix="/clients", tags=["clients"])

@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(client_id: int, db: Session = Depends(get_db)):
    """Get a client by ID"""
    client_service = ClientService(db)
    client = client_service.get_client_by_id(client_id)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return client

@router.post("/search", response_model=List[ClientResponse])
async def search_clients(request: ClientSearchRequest, db: Session = Depends(get_db)):
    """Search clients by various criteria"""
    client_service = ClientService(db)

    # Handle range searches
    if request.min_age or request.max_age:
        return client_service.get_clients_by_age_range(request.min_age, request.max_age)

    if request.min_income or request.max_income:
        return client_service.get_clients_by_income_range(request.min_income, request.max_income)

    # Handle specific value searches
    return client_service.search_clients(request.name, request.age, request.income)

@router.get("/stats", response_model=ClientStatisticsResponse)
async def get_client_statistics(db: Session = Depends(get_db)):
    """Get statistics about all clients"""
    client_service = ClientService(db)
    return client_service.get_client_statistics()

@router.get("/{client_id}/income-prediction", response_model=IncomePredictionResponse)
async def get_client_income_prediction(client_id: int, db: Session = Depends(get_db)):
    """Get the latest income prediction for a client"""
    client_service = ClientService(db)
    prediction_service = IncomePredictionService(db)

    # Verify client exists
    client = client_service.get_client_by_id(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    prediction = prediction_service.get_client_income_prediction(client_id)

    if not prediction:
        raise HTTPException(status_code=404, detail="No income prediction found for this client")

    return prediction

@router.post("/income-prediction", response_model=IncomePredictionResponse)
async def create_income_prediction(request: CreateIncomePredictionRequest, db: Session = Depends(get_db)):
    """Create a new income prediction for a client"""
    client_service = ClientService(db)
    prediction_service = IncomePredictionService(db)

    # Verify client exists
    client = client_service.get_client_by_id(request.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return prediction_service.create_income_prediction(request.client_id, request.predicted_income)
