"""
Модуль расчета кредитного рейтинга клиентов Альфа-Банка
Кредитный рейтинг рассчитывается по шкале от 1 до 999
"""

import math
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class CreditScorer:
    """Класс для расчета кредитного рейтинга"""

    def __init__(self):
        # Базовые веса для различных факторов
        self.weights = {
            'bki_factors': 0.35,      # BKI данные (35%)
            'financial_factors': 0.25, # Финансовые показатели (25%)
            'behavioral_factors': 0.20, # Поведенческие факторы (20%)
            'demographic_factors': 0.15, # Демографические факторы (15%)
            'risk_factors': 0.05      # Факторы риска (5%)
        }

        # Максимальные значения для нормализации
        self.max_values = {
            'avg_credit_turn_rur': 500000,
            'curr_rur_amt_cm_avg': 1000000,
            'incomeValue': 1000000,
            'bki_total_products': 20,
            'mob_total_sessions': 365,
            'age': 100
        }

    def calculate_credit_score(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Рассчитать кредитный рейтинг клиента

        Args:
            client_data: Словарь с данными клиента

        Returns:
            Dict с рейтингом и деталями расчета
        """
        try:
            # Расчет отдельных компонентов
            bki_score = self._calculate_bki_score(client_data)
            financial_score = self._calculate_financial_score(client_data)
            behavioral_score = self._calculate_behavioral_score(client_data)
            demographic_score = self._calculate_demographic_score(client_data)
            risk_score = self._calculate_risk_score(client_data)

            # Взвешенная сумма
            total_score = (
                bki_score * self.weights['bki_factors'] +
                financial_score * self.weights['financial_factors'] +
                behavioral_score * self.weights['behavioral_factors'] +
                demographic_score * self.weights['demographic_factors'] +
                risk_score * self.weights['risk_factors']
            )

            # Преобразование в шкалу 1-999
            # Используем sigmoid функцию для плавного распределения
            normalized_score = self._sigmoid_normalize(total_score)

            # Финальный рейтинг
            credit_score = max(1, min(999, round(normalized_score)))

            return {
                'credit_score': credit_score,
                'score_components': {
                    'bki_score': round(bki_score, 2),
                    'financial_score': round(financial_score, 2),
                    'behavioral_score': round(behavioral_score, 2),
                    'demographic_score': round(demographic_score, 2),
                    'risk_score': round(risk_score, 2)
                },
                'total_weighted_score': round(total_score, 2),
                'risk_category': self._get_risk_category(credit_score),
                'recommendations': self._get_recommendations(credit_score, client_data)
            }

        except Exception as e:
            logger.error(f"Ошибка расчета кредитного рейтинга: {e}")
            return {
                'credit_score': None,
                'error': str(e),
                'score_components': {},
                'risk_category': 'unknown',
                'recommendations': []
            }

    def _calculate_bki_score(self, data: Dict[str, Any]) -> float:
        """Расчет BKI компонента (макс 1000 баллов)"""
        score = 1000  # Начальный балл

        # Количество активных кредитных продуктов (отрицательный фактор)
        active_products = data.get('bki_total_active_products', 0) or data.get('hdb_bki_total_active_products', 0)
        if active_products > 5:
            score -= 200
        elif active_products > 2:
            score -= 100
        elif active_products == 0:
            score += 50  # Положительный фактор для безкредитных клиентов

        # Максимальная просрочка
        max_overdue = data.get('hdb_bki_total_max_overdue_sum', 0) or data.get('total_sum', 0)
        if max_overdue > 50000:
            score -= 300
        elif max_overdue > 10000:
            score -= 200
        elif max_overdue > 1000:
            score -= 100
        elif max_overdue == 0:
            score += 100  # Отличная кредитная история

        # Количество обращений в BKI
        bki_requests = data.get('hdb_bki_total_cnt', 0)
        if bki_requests > 50:
            score -= 150
        elif bki_requests > 20:
            score -= 50

        # Дни с последнего продукта
        days_last_product = data.get('hdb_bki_last_product_days', 0)
        if days_last_product < 30:
            score -= 50  # Недавно брал кредит

        # Максимальный лимит по кредитам
        max_limit = data.get('bki_total_max_limit', 0) or data.get('hdb_bki_total_max_limit', 0)
        if max_limit > 500000:
            score += 50  # Высокий лимит = хорошая кредитная история

        return max(0, min(1000, score))

    def _calculate_financial_score(self, data: Dict[str, Any]) -> float:
        """Расчет финансового компонента (макс 1000 баллов)"""
        score = 500  # Средний начальный балл

        # Средний баланс на текущих счетах
        avg_balance = data.get('curr_rur_amt_cm_avg', 0) or data.get('total_rur_amt_cm_avg', 0)
        if avg_balance > 200000:
            score += 200
        elif avg_balance > 50000:
            score += 100
        elif avg_balance < 5000:
            score -= 100

        # Обороты по счетам
        credit_turn = data.get('avg_credit_turn_rur', 0) or data.get('turn_cur_cr_avg_v2', 0)
        debit_turn = data.get('avg_debet_turn_rur', 0) or data.get('turn_cur_db_avg_v2', 0)

        if credit_turn > debit_turn * 2:
            score += 100  # Много поступлений
        elif credit_turn < debit_turn:
            score -= 100  # Много трат

        # Доход
        income = data.get('incomeValue', 0)
        if income > 200000:
            score += 150
        elif income > 100000:
            score += 100
        elif income > 50000:
            score += 50
        elif income < 20000:
            score -= 50

        # Категория дохода
        income_cat = data.get('incomeValueCategory', 0)
        score += income_cat * 20  # Каждая категория добавляет баллы

        # Операционный доход
        profit_12m = data.get('profit_income_out_rur_amt_12m', 0)
        if profit_12m > 1000:
            score += 100
        elif profit_12m < 0:
            score -= 200  # Отрицательный доход

        return max(0, min(1000, score))

    def _calculate_behavioral_score(self, data: Dict[str, Any]) -> float:
        """Расчет поведенческого компонента (макс 1000 баллов)"""
        score = 600  # Средний начальный балл

        # Активность в мобильном приложении
        mob_sessions = data.get('mob_total_sessions', 0)
        mob_days = data.get('mob_cnt_days', 0)

        if mob_sessions > 100:
            score += 100
        elif mob_sessions > 50:
            score += 50
        elif mob_sessions < 5:
            score -= 50

        if mob_days > 60:
            score += 100  # Активный пользователь
        elif mob_days < 10:
            score -= 50

        # Транзакционная активность
        avg_daily_trans = data.get('avg_amount_daily_transactions_90d', 0)
        if avg_daily_trans > 1000:
            score += 50
        elif avg_daily_trans < 100:
            score -= 50

        # Количество блокировок
        blocks = data.get('cntBlockWavg6m', 0)
        if blocks > 10:
            score -= 150
        elif blocks > 5:
            score -= 50

        # Звонки и SMS
        voice_out = data.get('cntVoiceOutMob6m', 0)
        sms_in = data.get('smsInWavg6m', 0)

        if voice_out > 200:
            score += 50
        elif voice_out < 20:
            score -= 30

        # Наличие зарплатного счета
        salary_flag = data.get('accountsalary_out_flag', 0)
        if salary_flag == 1:
            score += 100  # Положительный фактор

        # Приложения других банков
        other_bank_apps = (
            data.get('vert_has_app_ru_raiffeisennews', 0) +
            data.get('vert_has_app_ru_tinkoff_investing', 0) +
            data.get('vert_has_app_ru_vtb_invest', 0)
        )
        if other_bank_apps > 0:
            score -= 50  # Использует другие банки

        return max(0, min(1000, score))

    def _calculate_demographic_score(self, data: Dict[str, Any]) -> float:
        """Расчет демографического компонента (макс 1000 баллов)"""
        score = 700  # Высокий начальный балл для стабильности

        # Возраст
        age = data.get('age', 30)
        if 25 <= age <= 65:
            score += 100  # Оптимальный возраст
        elif age < 21 or age > 75:
            score -= 100  # Рискованный возраст

        # Пол (женщины часто имеют лучшую кредитную историю)
        gender = str(data.get('gender', '')).lower()
        if 'жен' in gender:
            score += 50

        # Региональный доход
        region_income = data.get('per_capita_income_rur_amt', 0)
        if region_income > 50000:
            score += 50
        elif region_income < 20000:
            score -= 50

        # Резидентство
        non_resident = data.get('nonresident_flag', 0)
        if non_resident == 1:
            score -= 200  # Нерезидент

        # Черный список
        blacklist = data.get('blacklist_flag', 0)
        if blacklist == 1:
            score -= 500  # В черном списке

        # Активность клиента
        active_flag = data.get('client_active_flag', 1)
        if active_flag == 0:
            score -= 100  # Неактивный клиент

        return max(0, min(1000, score))

    def _calculate_risk_score(self, data: Dict[str, Any]) -> float:
        """Расчет компонента риска (макс 1000 баллов, но влияет отрицательно)"""
        score = 1000  # Начальный балл

        # Просрочки
        overdue_sum = data.get('ovrd_sum', 0) or data.get('total_sum', 0)
        if overdue_sum > 10000:
            score -= 300
        elif overdue_sum > 1000:
            score -= 100

        # Количество кредитов в других банках
        other_credits = data.get('other_credits_count', 0)
        if other_credits > 3:
            score -= 150

        # Время жизни у конкурента
        competitor_lifetime = data.get('lifetimeComp', 0)
        if competitor_lifetime > 365:
            score -= 50  # Долго был у конкурента

        # Количество возвращений (winback)
        winback_cnt = data.get('winback_cnt', 0)
        if winback_cnt > 2:
            score -= 100  # Часто уходил и возвращался

        # Дни до последней транзакции
        days_last_trans = data.get('days_to_last_transaction', 0)
        if days_last_trans > 90:
            score -= 200  # Давно не активен
        elif days_last_trans > 30:
            score -= 50

        return max(0, min(1000, score))

    def _sigmoid_normalize(self, score: float) -> float:
        """Нормализация с помощью sigmoid функции для шкалы 1-999"""
        # Sigmoid преобразование
        sigmoid = 1 / (1 + math.exp(-score / 1000 + 0.5))

        # Преобразование в шкалу 1-999
        normalized = sigmoid * 998 + 1

        return normalized

    def _get_risk_category(self, credit_score: int) -> str:
        """Определение категории риска по кредитному рейтингу"""
        if credit_score >= 800:
            return "excellent"  # Отличный
        elif credit_score >= 700:
            return "good"      # Хороший
        elif credit_score >= 600:
            return "fair"      # Удовлетворительный
        elif credit_score >= 500:
            return "poor"      # Плохой
        elif credit_score >= 300:
            return "bad"       # Очень плохой
        else:
            return "critical"  # Критический

    def _get_recommendations(self, credit_score: int, client_data: Dict[str, Any]) -> list:
        """Генерация рекомендаций на основе рейтинга"""
        recommendations = []

        if credit_score < 500:
            recommendations.extend([
                "Рекомендуется улучшить кредитную историю",
                "Рассмотреть возможность рефинансирования существующих долгов",
                "Увеличить регулярные поступления на счет"
            ])

            # Специфические рекомендации на основе данных
            if client_data.get('total_sum', 0) > 0:
                recommendations.append("Погасить существующие просрочки")
            if client_data.get('mob_total_sessions', 0) < 10:
                recommendations.append("Активнее использовать мобильное приложение банка")

        elif credit_score < 700:
            recommendations.extend([
                "Рассмотреть возможность увеличения кредитного лимита",
                "Поддерживать регулярные поступления на счет",
                "Рассмотреть инвестиционные продукты"
            ])

        else:
            recommendations.extend([
                "Отличная кредитная история!",
                "Можно рассматривать премиальные продукты",
                "Возможность получения более выгодных условий по кредитам"
            ])

        return recommendations


# Глобальный экземпляр скорера
credit_scorer = CreditScorer()
