from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClientResponse(BaseModel):
    id: int
    name: Optional[str]
    age: Optional[float]
    incomeValue: Optional[float]

    class Config:
        from_attributes = True

class ClientSearchRequest(BaseModel):
    name: Optional[str] = None
    age: Optional[float] = None
    income: Optional[float] = None
    min_age: Optional[float] = None
    max_age: Optional[float] = None
    min_income: Optional[float] = None
    max_income: Optional[float] = None

class ClientStatisticsResponse(BaseModel):
    total_clients: int
    average_age: float
    average_income: float
    min_age: float
    max_age: float
    min_income: float
    max_income: float

