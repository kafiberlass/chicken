from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, JSON
from datetime import datetime, timezone
from .base import Base

class IncomePredictionModel(Base):
    __tablename__ = "income_predictions"
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client_data.id"), nullable=False)
    predicted_income = Column(Numeric, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))