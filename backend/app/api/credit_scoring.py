"""
Endpoints кредитного скоринга
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..model.schemas import ClientData
from ..service.credit_scoring import credit_scorer
from ..service.financial_offers import financial_offers_service

router = APIRouter()

@router.post("/credit-score")
async def calculate_credit_score(client_data: ClientData, include_offers: bool = True):
    """Рассчитать кредитный рейтинг по данным клиента"""
    try:
        # Преобразование данных
        client_dict = client_data.dict()

        # Расчет рейтинга
        result = credit_scorer.calculate_credit_score(client_dict)

        response = {
            "credit_scoring": result,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Добавление финансовых предложений
        if include_offers and result.get('credit_score'):
            offers = financial_offers_service.generate_offers(
                client_dict,
                result['credit_score']
            )
            response["financial_offers"] = offers

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка расчета кредитного рейтинга: {str(e)}"
        )
