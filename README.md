# Альфа-доходы API

API для кредитного скоринга клиентов Альфа-Банка на основе данных из базы данных.

## Описание

API предоставляет:
- **Кредитный скоринг** - расчет рейтинга от 1 до 999
- **Интеграция с БД** - поддержка 200+ колонок данных
- **Автоматическое маппинг** - умное сопоставление полей
- **Анализ рисков** - оценка кредитоспособности

## Быстрый запуск

### Docker (рекомендуется)

```bash
# Сборка и запуск
docker-compose up --build

# API доступен на http://localhost:8000
# Документация на http://localhost:8000/docs
```

### Локальная разработка

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск
cd backend
python main.py
```

## API Endpoints

### Проверка здоровья
```http
GET /api/v1/health
```

### Кредитный скоринг по данным клиента
```http
POST /api/v1/credit-score
Content-Type: application/json

{
  "age": 35,
  "gender": "F",
  "region": "Москва",
  "monthly_income": 80000,
  "bki_active_products": 1,
  ...
}
```

### Кредитный скоринг клиента из БД
```http
GET /api/v1/clients/{client_id}/credit-score
```

### Финансовые предложения
API автоматически включает персонализированные финансовые предложения на основе:
- Кредитного рейтинга
- Уровня дохода
- Жизненного этапа клиента
- Кредитной нагрузки

**Включенные продукты:**
- 💳 Кредитные карты (стандартная/золотая/премиум)
- 🏠 Потребительские кредиты
- 🏠 Ипотечные кредиты
- 💰 Депозиты и накопительные счета
- 📈 Инвестиционные продукты
- 🛡️ Страховые продукты

### Статистика базы данных
```http
GET /api/v1/database/stats
```

## Структура проекта

```
backend/
├── main.py                    # Точка входа
├── app/
│   ├── api/
│   │   ├── app.py            # Основное приложение FastAPI
│   │   ├── endpoints.py      # Все endpoints
│   │   ├── health.py         # Health check
│   │   ├── credit_scoring.py # Кредитный скоринг
│   │   └── clients.py        # Работа с клиентами
│   ├── model/
│   │   └── schemas.py        # Pydantic схемы
│   ├── service/
│   │   └── credit_scoring.py # Логика скоринга
│   └── database/
│       └── client_service.py # Работа с БД
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Настройка базы данных

Создайте `.env` файл:

```bash
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=clients_data
DB_USER=your_username
DB_PASSWORD=your_password
```

## Формат ответа кредитного скоринга

```json
{
  "credit_scoring": {
    "credit_score": 785,
    "score_components": {
      "bki_score": 850.5,
      "financial_score": 720.3,
      "behavioral_score": 680.2,
      "demographic_score": 750.1,
      "risk_score": 900.4
    },
    "risk_category": "good",
    "recommendations": [
      "Рассмотреть увеличение кредитного лимита",
      "Поддерживать регулярные поступления"
    ]
  },
  "financial_offers": {
    "client_profile": {
      "income_category": "medium_high",
      "life_stage": "mid_career",
      "credit_load": "low"
    },
    "financial_offers": [
      {
        "product_type": "credit_card",
        "product_name": "Кредитная карта",
        "variant": "gold",
        "details": {
          "limit": 150000,
          "rate": 23.9,
          "cashback": 2.0
        },
        "priority": 8,
        "reason": "Премиальная карта с повышенным кэшбеком"
      },
      {
        "product_type": "deposit",
        "product_name": "Депозит",
        "variant": "savings",
        "details": {
          "rate": 7.5,
          "term": 365,
          "withdrawal": true
        },
        "priority": 6,
        "reason": "Накопительный счет с свободным пополнением"
      }
    ],
    "monthly_income_analysis": {
      "current_income": 80000,
      "projected_income": 160000,
      "growth_rate": 0.1,
      "years": 15,
      "potential_savings": 32000
    }
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

## Категории риска

- **excellent** (800-999): Отличная кредитная история
- **good** (700-799): Хорошая кредитная история
- **fair** (600-699): Удовлетворительная
- **poor** (500-599): Плохая кредитная история
- **bad** (300-499): Очень плохая кредитная история
- **critical** (1-299): Критическая ситуация

## Развертывание

### Переменные окружения
```bash
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=clients_data
DB_USER=user
DB_PASSWORD=password
DEBUG=false
```

### Docker Compose
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DB_TYPE=postgresql
      - DB_HOST=host.docker.internal
      - DB_NAME=clients_data
    volumes:
      - ./models:/app/models:ro
```