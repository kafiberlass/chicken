from sqlalchemy import Column, Integer, String, Numeric
from .base import Base

class ClientModel(Base):
    __tablename__ = "client_data"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    age = Column(Numeric)
    incomeValue = Column(Numeric)