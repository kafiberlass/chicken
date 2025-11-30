"""
Endpoints для работы с клиентами из базы данных
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..database.client_service import client_service
from ..service.credit_scoring import credit_scorer
from ..service.financial_offers import financial_offers_service

router = APIRouter()

@router.get("/clients/{client_id}/credit-score")
async def get_client_credit_score(client_id: int, include_offers: bool = True):
    """Получить кредитный рейтинг клиента из базы данных"""
    try:
        # Получение данных клиента
        client_data = client_service.get_client_data(client_id)
        if not client_data:
            raise HTTPException(
                status_code=404,
                detail=f"Клиент с ID {client_id} не найден"
            )

        # Расчет рейтинга
        result = credit_scorer.calculate_credit_score(client_data)

        response = {
            "client_id": client_id,
            "credit_scoring": result,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Добавление финансовых предложений
        if include_offers and result.get('credit_score'):
            offers = financial_offers_service.generate_offers(
                client_data,
                result['credit_score']
            )
            response["financial_offers"] = offers

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка обработки клиента {client_id}: {str(e)}"
        )

@router.get("/database/stats")
async def get_database_stats():
    """Получить статистику базы данных"""
    try:
        stats = client_service.get_database_stats()
        return {
            "database_stats": stats,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка получения статистики БД: {str(e)}"
        )
