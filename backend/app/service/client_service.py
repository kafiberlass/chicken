from sqlalchemy import and_
from typing import List, Optional
from ..model.client_model import ClientModel
from .base_service import BaseService

class ClientService(BaseService):

    def get_client_by_id(self, client_id: int) -> Optional[ClientModel]:
        return self.db.query(ClientModel).filter(ClientModel.id == client_id).first()

    def get_clients_by_age_range(self, min_age: float = None, max_age: float = None) -> List[ClientModel]:
        query = self.db.query(ClientModel)

        if min_age is not None:
            query = query.filter(ClientModel.age >= min_age)
        if max_age is not None:
            query = query.filter(ClientModel.age <= max_age)

        return query.all()

    def get_clients_by_income_range(self, min_income: float = None, max_income: float = None) -> List[ClientModel]:
        query = self.db.query(ClientModel)

        if min_income is not None:
            query = query.filter(ClientModel.incomeValue >= min_income)
        if max_income is not None:
            query = query.filter(ClientModel.incomeValue <= max_income)

        return query.all()

    def search_clients(self, name: str = None, age: float = None, income: float = None) -> List[ClientModel]:
        query = self.db.query(ClientModel)

        filters = []
        if name:
            filters.append(ClientModel.name.ilike(f"%{name}%"))
        if age:
            filters.append(ClientModel.age == age)
        if income:
            filters.append(ClientModel.incomeValue == income)

        if filters:
            query = query.filter(and_(*filters))

        return query.all()