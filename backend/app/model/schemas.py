"""
Схемы Pydantic для API Альфа-доходы
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class ClientData(BaseModel):
    """Схема данных клиента для кредитного скоринга"""

    # Доступные поля из базы данных
    age: int = Field(..., ge=0, le=120, description="Возраст клиента")
    gender: str = Field(..., description="Пол клиента (M/F/O)")
    region: str = Field(..., description="Регион клиента")
    city_type: str = Field(..., description="Тип города")

    # Финансовые показатели
    monthly_income: float = Field(0, ge=0, description="Месячный доход")
    credit_score: float = Field(0, ge=0, le=1, description="Кредитный скоринг (0-1)")
    income_category: int = Field(0, ge=0, le=10, description="Категория дохода")

    # Балансы и обороты
    current_balance_avg: float = Field(0, description="Средний баланс на счетах")
    credit_turnover_avg: float = Field(0, description="Кредитовый оборот")
    debit_turnover_avg: float = Field(0, description="Дебетовый оборот")

    # BKI данные
    bki_active_products: float = Field(0, ge=0, description="Активные кредитные продукты")
    bki_total_products: float = Field(0, ge=0, description="Всего кредитных продуктов")
    bki_max_overdue: float = Field(0, ge=0, description="Максимальная просрочка")
    bki_max_limit: float = Field(0, ge=0, description="Максимальный кредитный лимит")
    bki_requests_count: float = Field(0, ge=0, description="Количество запросов в BKI")

    # Поведенческие характеристики
    mobile_sessions: int = Field(0, ge=0, description="Сессии в мобильном приложении")
    mobile_days: int = Field(0, ge=0, description="Дни использования приложения")
    avg_daily_transactions: float = Field(0, ge=0, description="Средний дневной оборот")
    days_last_transaction: int = Field(0, ge=0, description="Дни с последней транзакции")

    # Категории расходов
    spending_supermarket: float = Field(0, ge=0, description="Расходы в супермаркетах")
    spending_products: float = Field(0, ge=0, description="Расходы на продукты")
    spending_food: float = Field(0, ge=0, description="Расходы в кафе")
    spending_cash_atm: float = Field(0, ge=0, description="Снятие наличных")
    spending_electronics: float = Field(0, ge=0, description="Электронные деньги")

    # Транзакционная активность
    trans_supermarket_count: int = Field(0, ge=0, description="Транзакции в супермаркетах")
    trans_supermarket_percent: float = Field(0, ge=0, le=1, description="Процент транзакций в супермаркетах")

    # Телеком данные
    voice_calls_out: float = Field(0, ge=0, description="Исходящие звонки")
    sms_incoming: float = Field(0, ge=0, description="Входящие SMS")
    business_contacts: int = Field(0, ge=0, description="Бизнес контакты")

    # Региональные данные
    region_income: float = Field(0, ge=0, description="Доход в регионе")

    # Флаги и статусы
    salary_account_flag: int = Field(0, ge=0, le=1, description="Зарплатный счет")
    active_flag: int = Field(1, ge=0, le=1, description="Активный клиент")
    nonresident_flag: int = Field(0, ge=0, le=1, description="Нерезидент")
    blacklist_flag: int = Field(0, ge=0, le=1, description="Черный список")

    # Кредиты в других банках
    other_bank_credits: int = Field(0, ge=0, description="Кредиты в других банках")
    pil_credits: int = Field(0, ge=0, description="Кредиты наличными")

    # Риски
    overdue_sum: float = Field(0, ge=0, description="Сумма просрочек")
    blocks_count: float = Field(0, ge=0, description="Количество блокировок")

    # История
    competitor_lifetime: int = Field(0, ge=0, description="Время у конкурента")
    winback_count: int = Field(0, ge=0, description="Количество возвращений")

    # Приложения конкурентов
    has_cian_app: int = Field(0, ge=0, le=1, description="Приложение ЦИАН")
    has_raiffeisen_app: int = Field(0, ge=0, le=1, description="Приложение Райффайзен")
    has_tinkoff_app: int = Field(0, ge=0, le=1, description="Приложение Тинькофф")
    has_vtb_app: int = Field(0, ge=0, le=1, description="Приложение ВТБ")

    # Продукты Альфа-Банка
    alfa_cards_count: int = Field(0, ge=0, description="Карты Альфа-Банка")

    # Операционный доход
    profit_12m: float = Field(0, description="Операционный доход 12м")
    profit_9m: float = Field(0, description="Операционный доход 9м")
    profit_last_4m: float = Field(0, description="Операционный доход последние 4м")

    # Дополнительные признаки
    additional_features: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Дополнительные признаки из базы данных"
    )

    class Config:
        extra = "allow"

class CreditScoreResponse(BaseModel):
    """Ответ кредитного скоринга"""
    credit_score: int = Field(..., ge=1, le=999, description="Кредитный рейтинг (1-999)")
    score_components: Dict[str, float] = Field(..., description="Компоненты рейтинга")
    risk_category: str = Field(..., description="Категория риска")
    recommendations: list = Field(..., description="Рекомендации")

class DatabaseStatsResponse(BaseModel):
    """Ответ статистики базы данных"""
    total_clients: int = Field(..., description="Всего клиентов")
    total_columns: int = Field(..., description="Всего колонок")
    mapped_fields: list = Field(..., description="Отображенные поля")
    timestamp: str = Field(..., description="Время запроса")

    @validator('gender')
    def validate_gender(cls, v):
        if v.upper() not in ['M', 'F', 'O']:
            raise ValueError('Пол должен быть M, F или O')
        return v.upper()

    @validator('city_type')
    def validate_city_type(cls, v):
        valid_types = ['metropolitan', 'regional', 'rural']
        if v.lower() not in valid_types:
            raise ValueError(f'Тип города должен быть одним из: {valid_types}')
        return v.lower()

class PredictionRequest(BaseModel):
    """Схема для запроса предсказания API"""
    client_data: ClientData
    include_explanations: bool = Field(True, description="Включить объяснения SHAP")
    include_recommendations: bool = Field(True, description="Включить рекомендации по продуктам")

class PredictionResponse(BaseModel):
    """Схема для ответа предсказания API"""
    prediction_id: str = Field(..., description="Уникальный идентификатор предсказания")
    predicted_income: float = Field(..., description="Предсказанный годовой доход")
    confidence_score: float = Field(..., ge=0, le=1, description="Оценка уверенности модели")
    timestamp: str = Field(..., description="Время предсказания")

    explanations: Optional[Dict[str, Any]] = Field(None, description="Объяснения SHAP")
    recommendations: Optional[List[Dict[str, Any]]] = Field(None, description="Рекомендации по продуктам")

    model_metadata: Dict[str, Any] = Field(..., description="Информация о модели")

class ExplanationResponse(BaseModel):
    """Схема для ответа endpoint объяснений"""
    prediction_id: str
    feature_importance: Dict[str, float] = Field(..., description="Оценки важности признаков")
    shap_values: Dict[str, Any] = Field(..., description="SHAP значения для признаков")
    feature_contributions: List[Dict[str, Any]] = Field(..., description="Детали вклада признаков")
    base_value: float = Field(..., description="Базовое значение SHAP")
    model_metadata: Dict[str, Any]

class RecommendationResponse(BaseModel):
    """Схема для ответа endpoint рекомендаций"""
    prediction_id: str
    client_profile: Dict[str, Any] = Field(..., description="Сводка профиля клиента")
    recommended_products: List[Dict[str, Any]] = Field(..., description="Рекомендуемые банковские продукты")
    rationale: str = Field(..., description="Обоснование рекомендаций")
    risk_assessment: Dict[str, Any] = Field(..., description="Детали оценки рисков")

class HealthResponse(BaseModel):
    """Схема для ответа проверки здоровья"""
    status: str = Field(..., description="Статус API")
    timestamp: str = Field(..., description="Текущее время")
    version: str = Field(..., description="Версия API")
    model_loaded: bool = Field(..., description="Статус загрузки модели")
    model_metadata: Optional[Dict[str, Any]] = Field(None, description="Информация о модели")

class ErrorResponse(BaseModel):
    """Схема для ответов с ошибками"""
    error: str = Field(..., description="Тип ошибки")
    message: str = Field(..., description="Человеко-читаемое сообщение об ошибке")
    details: Optional[Dict[str, Any]] = Field(None, description="Дополнительные детали ошибки")
    timestamp: str = Field(..., description="Время ошибки")
