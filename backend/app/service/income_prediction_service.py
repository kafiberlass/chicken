from ..model.income_prediction_model import IncomePredictionModel
from typing import List, Optional
from .base_service import BaseService

class IncomePredictionService(BaseService):
    def get_client_income_prediction(self, client_id: int) -> Optional[IncomePredictionModel]:
        return self.db.query(IncomePredictionModel)\
            .filter(IncomePredictionModel.client_id == client_id)\
            .order_by(IncomePredictionModel.created_at.desc())\
            .first()

    def create_income_prediction(self, client_id: int, predicted_income: float) -> IncomePredictionModel:
        prediction = IncomePredictionModel(
            client_id=client_id,
            predicted_income=predicted_income
        )
        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)
        return prediction

    def find_all_predictions(
        self,
        client_id: Optional[int] = None,
        min_predicted_income: Optional[float] = None,
        max_predicted_income: Optional[float] = None,
        limit: Optional[int] = None
    ) -> List[IncomePredictionModel]:
        query = self.db.query(IncomePredictionModel)

        if client_id is not None:
            query = query.filter(IncomePredictionModel.client_id == client_id)

            query = query.filter(IncomePredictionModel.predicted_income >= min_predicted_income)

        if max_predicted_income is not None:
            query = query.filter(IncomePredictionModel.predicted_income <= max_predicted_income)

        query = query.order_by(IncomePredictionModel.created_at.desc())

        if limit is not None:
            query = query.limit(limit)

        return query.all()