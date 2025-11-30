"""
Сервис базы данных
Обрабатывает подключение к SQL базе данных и извлечение данных клиентов
"""

import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine, text
from typing import Dict, Any, List, Optional, Tuple
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Загрузить переменные окружения
load_dotenv()

class DatabaseService:
    """Сервис для работы с базой данных клиентов"""

    def __init__(self, connection_string: Optional[str] = None):
        """
        Инициализация сервиса базы данных

        Args:
            connection_string: Строка подключения к БД
                              (если None, берется из переменных окружения)
        """
        self.connection_string = connection_string or self._get_connection_string()
        self.engine = None
        self._connect()

        # Маппинг полей БД к полям модели (расширяемый)
        self.field_mapping = {
            # Базовые поля модели
            'age': ['age'],
            'gender': ['gender'],
            'region': ['adminarea', 'region'],
            'city_type': ['city_smart_name'],

            # Финансовые поля
            'monthly_income': ['incomeValue'],
            'credit_score': ['uniV5'],  # скоринговый балл V5
            'income_category': ['incomeValueCategory'],

            # BKI поля
            'bki_active_products': ['bki_total_active_products', 'hdb_bki_total_active_products'],
            'bki_total_products': ['bki_total_products', 'hdb_bki_total_products'],
            'bki_max_overdue': ['hdb_bki_total_max_overdue_sum'],
            'bki_max_limit': ['bki_total_max_limit', 'hdb_bki_total_max_limit'],
            'bki_requests_count': ['hdb_bki_total_cnt'],

            # Балансы и обороты
            'current_balance_avg': ['curr_rur_amt_cm_avg', 'total_rur_amt_cm_avg'],
            'current_balance_current': ['curr_rur_amt_curr_v2', 'dda_rur_amt_curr_v2'],
            'credit_turnover_avg': ['avg_credit_turn_rur', 'turn_cur_cr_avg_v2'],
            'debit_turnover_avg': ['avg_debet_turn_rur', 'turn_cur_db_avg_v2'],

            # Поведенческие характеристики
            'mobile_sessions': ['mob_total_sessions'],
            'mobile_days': ['mob_cnt_days'],
            'mobile_coverage': ['mob_cover_days'],
            'avg_daily_transactions': ['avg_amount_daily_transactions_90d'],
            'days_last_transaction': ['days_to_last_transaction'],
            'days_last_request': ['days_after_last_request'],

            # Категории трат
            'spending_supermarket': ['avg_amount_cashflowcategory_supermarkety'],
            'spending_products': ['avg_amount_cashflowcategory_producty'],
            'spending_food': ['avg_amount_cashflowcategory_kafe'],
            'spending_cash_atm': ['avg_amount_sum_cashflowcategory_nalychka_bankomat'],
            'spending_electronics': ['avg_amount_cashflowcategory_electro_money'],

            # Транзакции по категориям
            'trans_supermarket_count': ['transaction_category_supermarket_sum_cnt_m2'],
            'trans_supermarket_percent': ['transaction_category_supermarket_percent_cnt_2m'],

            # Телеком данные
            'voice_calls_out': ['cntVoiceOutMob6m'],
            'sms_incoming': ['smsInWavg6m'],
            'business_contacts': ['businessTelSubs'],

            # Региональные данные
            'region_income': ['per_capita_income_rur_amt'],
            'timezone_diff': ['tz_msk_timedelta'],

            # Флаги и статусы
            'salary_account_flag': ['accountsalary_out_flag'],
            'active_flag': ['client_active_flag'],
            'nonresident_flag': ['nonresident_flag'],
            'blacklist_flag': ['blacklist_flag'],

            # Кредиты в других банках
            'other_bank_credits': ['other_credits_count'],
            'pil_credits': ['pil'],

            # Просрочки и риски
            'overdue_sum': ['ovrd_sum', 'total_sum'],
            'blocks_count': ['cntBlockWavg6m'],

            # Время жизни
            'competitor_lifetime': ['lifetimeComp'],
            'winback_count': ['winback_cnt'],

            # Приложения
            'has_cian_app': ['vert_has_app_ru_cian_main'],
            'has_raiffeisen_app': ['vert_has_app_ru_raiffeisennews'],
            'has_tinkoff_app': ['vert_has_app_ru_tinkoff_investing'],
            'has_vtb_app': ['vert_has_app_ru_vtb_invest'],

            # Кредитные продукты
            'alfa_cards_count': ['acard'],

            # Прибыль/операционный доход
            'profit_12m': ['profit_income_out_rur_amt_12m'],
            'profit_9m': ['profit_income_out_rur_amt_9m'],
            'profit_last_4m': ['profit_income_out_rur_amt_l2m'],
        }

    def _get_connection_string(self) -> str:
        """Получить строку подключения из переменных окружения"""
        db_type = os.getenv('DB_TYPE', 'postgresql')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'clients_data')
        db_user = os.getenv('DB_USER', 'user')
        db_password = os.getenv('DB_PASSWORD', 'password')

        if db_type == 'postgresql':
            return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        elif db_type == 'mysql':
            return f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        elif db_type == 'sqlite':
            return f"sqlite:///{db_name}.db"
        else:
            raise ValueError(f"Неподдерживаемый тип БД: {db_type}")

    def _connect(self):
        """Подключиться к базе данных"""
        try:
            self.engine = create_engine(self.connection_string)
            # Тест подключения
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Подключение к базе данных успешно установлено")
        except Exception as e:
            logger.error(f"Не удалось подключиться к базе данных: {e}")
            raise

    def get_client_columns(self) -> List[str]:
        """Получить список всех колонок в таблице клиентов"""
        try:
            query = """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'clients_data'
                ORDER BY ordinal_position
            """

            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                columns = [row[0] for row in result.fetchall()]

            logger.info(f"Найдено {len(columns)} колонок в таблице clients_data")
            return columns

        except Exception as e:
            logger.error(f"Не удалось получить список колонок: {e}")
            return []

    def get_client_data(self, client_id: int) -> Optional[Dict[str, Any]]:
        """Получить данные клиента по ID"""
        try:
            query = f"SELECT * FROM clients_data WHERE id = {client_id}"

            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                row = result.fetchone()

            if row:
                # Преобразовать Row в словарь
                columns = result.keys()
                client_data = dict(zip(columns, row))

                # Маппировать поля к ожидаемому формату
                mapped_data = self._map_fields(client_data)

                logger.info(f"Получены данные клиента ID {client_id}")
                return mapped_data
            else:
                logger.warning(f"Клиент с ID {client_id} не найден")
                return None

        except Exception as e:
            logger.error(f"Ошибка при получении данных клиента {client_id}: {e}")
            return None

    def get_client_data_paginated(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Получить данные клиентов с пагинацией"""
        try:
            query = f"SELECT * FROM clients_data LIMIT {limit} OFFSET {offset}"

            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                columns = result.keys()
                rows = result.fetchall()

            clients_data = []
            for row in rows:
                client_dict = dict(zip(columns, row))
                mapped_data = self._map_fields(client_dict)
                clients_data.append(mapped_data)

            logger.info(f"Получены данные {len(clients_data)} клиентов (limit={limit}, offset={offset})")
            return clients_data

        except Exception as e:
            logger.error(f"Ошибка при получении данных клиентов: {e}")
            return []

    def get_clients_count(self) -> int:
        """Получить общее количество клиентов"""
        try:
            query = "SELECT COUNT(*) FROM clients_data"

            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                count = result.scalar()

            return count or 0

        except Exception as e:
            logger.error(f"Ошибка при подсчете клиентов: {e}")
            return 0

    def _map_fields(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Маппировать поля из БД к ожидаемому формату модели"""
        mapped_data = {}
        additional_features = {}

        # Проходим по всем полям в raw_data
        for db_field, value in raw_data.items():
            # Ищем соответствие в маппинге
            found_mapping = False
            for model_field, possible_db_fields in self.field_mapping.items():
                if db_field.lower() in [f.lower() for f in possible_db_fields]:
                    # Специальная обработка для некоторых полей
                    if model_field == 'gender':
                        # Преобразование пола в стандартный формат
                        gender_str = str(value).lower()
                        if 'жен' in gender_str:
                            mapped_data[model_field] = 'F'
                        elif 'муж' in gender_str:
                            mapped_data[model_field] = 'M'
                        else:
                            mapped_data[model_field] = 'O'
                    elif model_field in ['region', 'city_type']:
                        # Очистка от пустых значений
                        if value and str(value).strip() not in ['', ' ', 'nan', 'None']:
                            mapped_data[model_field] = str(value).strip()
                        else:
                            mapped_data[model_field] = 'unknown'
                    else:
                        # Обычное маппинг с обработкой None/nan значений
                        if value is not None and str(value).lower() not in ['nan', 'none']:
                            try:
                                # Попытка преобразовать в число если это число
                                if isinstance(value, str) and value.replace('.', '').replace('-', '').isdigit():
                                    mapped_data[model_field] = float(value) if '.' in value else int(value)
                                else:
                                    mapped_data[model_field] = value
                            except (ValueError, TypeError):
                                mapped_data[model_field] = value
                        else:
                            mapped_data[model_field] = 0 if model_field in [
                                'monthly_income', 'credit_score', 'bki_active_products',
                                'current_balance_avg', 'mobile_sessions', 'alfa_cards_count'
                            ] else None

                    found_mapping = True
                    break

            # Если поле не найдено в маппинге, добавляем в дополнительные признаки
            if not found_mapping and db_field not in ['id', 'dt']:  # Исключаем системные поля
                additional_features[db_field] = value

        # Устанавливаем значения по умолчанию для обязательных полей
        defaults = {
            'age': 30,
            'gender': 'O',
            'region': 'unknown',
            'city_type': 'unknown',
            'monthly_income': 0,
            'credit_score': 0.5,  # uniV5 по умолчанию
            'bki_active_products': 0,
            'current_balance_avg': 0,
            'mobile_sessions': 0,
            'alfa_cards_count': 0
        }

        for field, default_value in defaults.items():
            if field not in mapped_data or mapped_data[field] is None:
                mapped_data[field] = default_value

        # Добавляем дополнительные признаки
        if additional_features:
            mapped_data['additional_features'] = additional_features

        return mapped_data

    def update_field_mapping(self, model_field: str, db_fields: List[str]):
        """Обновить маппинг полей (для расширения поддержки новых полей)"""
        self.field_mapping[model_field] = db_fields
        logger.info(f"Обновлен маппинг для поля {model_field}: {db_fields}")

    def get_database_stats(self) -> Dict[str, Any]:
        """Получить статистику базы данных"""
        try:
            total_clients = self.get_clients_count()
            columns = self.get_client_columns()

            # Получить пример данных для анализа
            sample_data = self.get_client_data_paginated(limit=10, offset=0)

            stats = {
                "total_clients": total_clients,
                "total_columns": len(columns),
                "column_names": columns[:20],  # Показать первые 20 колонок
                "sample_mapped_fields": list(sample_data[0].keys()) if sample_data else [],
                "has_additional_features": any('additional_features' in client for client in sample_data[:5])
            }

            return stats

        except Exception as e:
            logger.error(f"Ошибка при получении статистики БД: {e}")
            return {"error": str(e)}

# Глобальный экземпляр сервиса базы данных
database_service = DatabaseService()
