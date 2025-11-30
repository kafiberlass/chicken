"""
Модуль финансовых предложений Альфа-Банка
Генерирует персонализированные финансовые предложения на основе кредитного рейтинга и прогнозируемого дохода
"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class FinancialOffersService:
    """Сервис для генерации финансовых предложений"""

    def __init__(self):
        # Каталог финансовых продуктов
        self.product_catalog = {
            'credit_card': {
                'name': 'Кредитная карта',
                'types': {
                    'standard': {'limit': 50000, 'rate': 25.9, 'cashback': 1.0},
                    'gold': {'limit': 150000, 'rate': 23.9, 'cashback': 2.0},
                    'premium': {'limit': 500000, 'rate': 19.9, 'cashback': 3.0}
                },
                'requirements': {'min_score': 500, 'min_income': 30000}
            },
            'consumer_loan': {
                'name': 'Потребительский кредит',
                'types': {
                    'small': {'amount': 50000, 'rate': 12.9, 'term': 24},
                    'medium': {'amount': 300000, 'rate': 10.9, 'term': 60},
                    'large': {'amount': 1000000, 'rate': 8.9, 'term': 84}
                },
                'requirements': {'min_score': 600, 'min_income': 40000}
            },
            'mortgage': {
                'name': 'Ипотека',
                'types': {
                    'standard': {'rate': 9.9, 'term': 300, 'down_payment': 15},
                    'family': {'rate': 6.9, 'term': 360, 'down_payment': 15},
                    'it': {'rate': 5.9, 'term': 360, 'down_payment': 15}
                },
                'requirements': {'min_score': 700, 'min_income': 80000}
            },
            'deposit': {
                'name': 'Депозит',
                'types': {
                    'savings': {'rate': 7.5, 'term': 365, 'withdrawal': True},
                    'term_6m': {'rate': 8.2, 'term': 180, 'withdrawal': False},
                    'term_1y': {'rate': 9.5, 'term': 365, 'withdrawal': False},
                    'term_3y': {'rate': 10.2, 'term': 1095, 'withdrawal': False}
                },
                'requirements': {'min_score': 300, 'min_amount': 10000}
            },
            'investment': {
                'name': 'Инвестиционные продукты',
                'types': {
                    'brokerage': {'commission': 0.05, 'min_amount': 50000},
                    'iis': {'tax_deduction': 13, 'min_amount': 1000},
                    'pension': {'rate': 8.5, 'min_amount': 1500}
                },
                'requirements': {'min_score': 650, 'min_income': 60000}
            },
            'insurance': {
                'name': 'Страхование',
                'types': {
                    'life': {'coverage': '500000', 'monthly': 500},
                    'health': {'coverage': '200000', 'monthly': 300},
                    'property': {'coverage': '1000000', 'monthly': 800}
                },
                'requirements': {'min_score': 400}
            }
        }

    def generate_offers(self, client_data: Dict[str, Any], credit_score: int) -> Dict[str, Any]:
        """
        Генерировать финансовые предложения на основе данных клиента

        Args:
            client_data: Данные клиента
            credit_score: Кредитный рейтинг (1-999)

        Returns:
            Dict с предложениями и анализом
        """
        try:
            offers = []

            # Анализ профиля клиента
            profile = self._analyze_client_profile(client_data, credit_score)

            # Генерация предложений по категориям
            offers.extend(self._generate_credit_offers(profile))
            offers.extend(self._generate_deposit_offers(profile))
            offers.extend(self._generate_investment_offers(profile))
            offers.extend(self._generate_insurance_offers(profile))

            # Сортировка по приоритету
            offers.sort(key=lambda x: x.get('priority', 0), reverse=True)

            return {
                'client_profile': profile,
                'financial_offers': offers[:10],  # Топ 10 предложений
                'monthly_income_analysis': self._analyze_income_potential(client_data),
                'risk_based_offers': self._get_risk_based_offers(credit_score)
            }

        except Exception as e:
            logger.error(f"Ошибка генерации финансовых предложений: {e}")
            return {
                'error': str(e),
                'financial_offers': [],
                'client_profile': {}
            }

    def _analyze_client_profile(self, client_data: Dict[str, Any], credit_score: int) -> Dict[str, Any]:
        """Анализ профиля клиента для подбора предложений"""
        income = client_data.get('monthly_income', 0)
        age = client_data.get('age', 30)
        bki_products = client_data.get('bki_total_active_products', 0)
        region = client_data.get('region', '')

        # Определение категории клиента
        if income > 200000:
            income_category = 'high'
        elif income > 80000:
            income_category = 'medium_high'
        elif income > 40000:
            income_category = 'medium'
        else:
            income_category = 'low'

        # Определение жизненного этапа
        if age < 25:
            life_stage = 'young'
        elif age < 35:
            life_stage = 'early_career'
        elif age < 50:
            life_stage = 'mid_career'
        else:
            life_stage = 'mature'

        # Определение кредитной нагрузки
        if bki_products == 0:
            credit_load = 'none'
        elif bki_products <= 2:
            credit_load = 'low'
        elif bki_products <= 5:
            credit_load = 'medium'
        else:
            credit_load = 'high'

        return {
            'income_category': income_category,
            'life_stage': life_stage,
            'credit_load': credit_load,
            'credit_score': credit_score,
            'region': region,
            'monthly_income': income,
            'age': age,
            'bki_products': bki_products
        }

    def _generate_credit_offers(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Генерация предложений по кредитным продуктам"""
        offers = []
        credit_score = profile['credit_score']
        income = profile['monthly_income']
        life_stage = profile['life_stage']
        credit_load = profile['credit_load']

        # Кредитные карты
        if credit_score >= 500 and income >= 30000:
            card_type = self._select_card_type(credit_score, income)

            offers.append({
                'product_type': 'credit_card',
                'product_name': self.product_catalog['credit_card']['name'],
                'variant': card_type,
                'details': self.product_catalog['credit_card']['types'][card_type],
                'monthly_payment': 0,  # Кредитка - беспроцентный период
                'priority': 8 if credit_load == 'none' else 6,
                'reason': self._get_credit_card_reason(life_stage, income)
            })

        # Потребительские кредиты
        if credit_score >= 600 and income >= 40000:
            loan_type = self._select_loan_type(income, credit_score)

            loan_details = self.product_catalog['consumer_loan']['types'][loan_type]
            monthly_payment = self._calculate_monthly_payment(
                loan_details['amount'], loan_details['rate'], loan_details['term']
            )

            offers.append({
                'product_type': 'consumer_loan',
                'product_name': self.product_catalog['consumer_loan']['name'],
                'variant': loan_type,
                'details': loan_details,
                'monthly_payment': round(monthly_payment, 2),
                'priority': 7 if credit_load in ['none', 'low'] else 4,
                'reason': f"Кредит до {loan_details['amount']:,} ₽ на {loan_details['term']} месяцев"
            })

        # Ипотека
        if (credit_score >= 700 and income >= 80000 and
            life_stage in ['early_career', 'mid_career'] and
            profile['age'] < 65):

            mortgage_type = 'standard'
            if life_stage == 'mid_career' and income > 150000:
                mortgage_type = 'family'

            offers.append({
                'product_type': 'mortgage',
                'product_name': self.product_catalog['mortgage']['name'],
                'variant': mortgage_type,
                'details': self.product_catalog['mortgage']['types'][mortgage_type],
                'monthly_payment': 0,  # Рассчитывается индивидуально
                'priority': 9,
                'reason': "Ипотечное кредитование с низкой ставкой"
            })

        return offers

    def _generate_deposit_offers(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Генерация предложений по депозитам"""
        offers = []
        income = profile['monthly_income']

        if income >= 30000:  # Накопления возможны
            # Накопительный счет
            offers.append({
                'product_type': 'deposit',
                'product_name': self.product_catalog['deposit']['name'],
                'variant': 'savings',
                'details': self.product_catalog['deposit']['types']['savings'],
                'monthly_income': 0,  # Проценты начисляются
                'priority': 6,
                'reason': "Накопительный счет с свободным пополнением"
            })

            # Срочный депозит
            if income >= 50000:
                deposit_type = 'term_1y' if income >= 100000 else 'term_6m'

                offers.append({
                    'product_type': 'deposit',
                    'product_name': self.product_catalog['deposit']['name'],
                    'variant': deposit_type,
                    'details': self.product_catalog['deposit']['types'][deposit_type],
                    'monthly_income': 0,  # Проценты в конце срока
                    'priority': 5,
                    'reason': f"Высокий процент по срочному депозиту {self.product_catalog['deposit']['types'][deposit_type]['rate']}%"
                })

        return offers

    def _generate_investment_offers(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Генерация предложений по инвестициям"""
        offers = []
        credit_score = profile['credit_score']
        income = profile['monthly_income']
        life_stage = profile['life_stage']

        if credit_score >= 650 and income >= 60000:
            # Брокерское обслуживание
            if income >= 100000:
                offers.append({
                    'product_type': 'investment',
                    'product_name': self.product_catalog['investment']['name'],
                    'variant': 'brokerage',
                    'details': self.product_catalog['investment']['types']['brokerage'],
                    'monthly_income': 0,  # Зависит от инвестиций
                    'priority': 7,
                    'reason': "Брокерское обслуживание для активных инвесторов"
                })

            # ИИС
            offers.append({
                'product_type': 'investment',
                'product_name': self.product_catalog['investment']['name'],
                'variant': 'iis',
                'details': self.product_catalog['investment']['types']['iis'],
                'monthly_income': 0,
                'priority': 6,
                'reason': "Индивидуальный инвестиционный счет с налоговым вычетом"
            })

            # Пенсионные накопления
            if life_stage in ['mid_career', 'mature']:
                offers.append({
                    'product_type': 'investment',
                    'product_name': self.product_catalog['investment']['name'],
                    'variant': 'pension',
                    'details': self.product_catalog['investment']['types']['pension'],
                    'monthly_income': 0,
                    'priority': 5,
                    'reason': "Накопительное пенсионное страхование"
                })

        return offers

    def _generate_insurance_offers(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Генерация предложений по страхованию"""
        offers = []
        credit_score = profile['credit_score']

        if credit_score >= 400:
            # Страхование жизни
            offers.append({
                'product_type': 'insurance',
                'product_name': self.product_catalog['insurance']['name'],
                'variant': 'life',
                'details': self.product_catalog['insurance']['types']['life'],
                'monthly_payment': 500,
                'priority': 4,
                'reason': "Комплексное страхование жизни и здоровья"
            })

            # Страхование здоровья
            offers.append({
                'product_type': 'insurance',
                'product_name': self.product_catalog['insurance']['name'],
                'variant': 'health',
                'details': self.product_catalog['insurance']['types']['health'],
                'monthly_payment': 300,
                'priority': 3,
                'reason': "Добровольное медицинское страхование"
            })

        return offers

    def _select_card_type(self, credit_score: int, income: float) -> str:
        """Выбор типа кредитной карты"""
        if credit_score >= 750 and income >= 100000:
            return 'premium'
        elif credit_score >= 650 and income >= 60000:
            return 'gold'
        else:
            return 'standard'

    def _select_loan_type(self, income: float, credit_score: int) -> str:
        """Выбор типа потребительского кредита"""
        if income >= 150000 and credit_score >= 700:
            return 'large'
        elif income >= 80000 and credit_score >= 650:
            return 'medium'
        else:
            return 'small'

    def _calculate_monthly_payment(self, amount: float, rate: float, term: int) -> float:
        """Расчет ежемесячного платежа по кредиту"""
        monthly_rate = rate / 100 / 12
        payment = amount * (monthly_rate * (1 + monthly_rate) ** term) / ((1 + monthly_rate) ** term - 1)
        return payment

    def _get_credit_card_reason(self, life_stage: str, income: float) -> str:
        """Получение причины для предложения кредитной карты"""
        if life_stage == 'young':
            return "Идеально для молодых клиентов с регулярным доходом"
        elif income >= 80000:
            return "Премиальная карта с повышенным кэшбеком"
        else:
            return "Универсальная карта для повседневных покупок"

    def _analyze_income_potential(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ потенциала дохода для предложений"""
        current_income = client_data.get('monthly_income', 0)
        age = client_data.get('age', 30)

        # Прогноз роста дохода
        if age < 30:
            income_growth = 0.15  # 15% рост в год
            years_to_analyze = 10
        elif age < 40:
            income_growth = 0.10
            years_to_analyze = 15
        else:
            income_growth = 0.05
            years_to_analyze = 20

        future_income = current_income * (1 + income_growth) ** years_to_analyze

        return {
            'current_income': current_income,
            'projected_income': round(future_income, 2),
            'growth_rate': income_growth,
            'years': years_to_analyze,
            'potential_savings': round(future_income * 0.2, 2)  # 20% от дохода на накопления
        }

    def _get_risk_based_offers(self, credit_score: int) -> List[str]:
        """Получение предложений на основе кредитного рейтинга"""
        if credit_score >= 800:
            return [
                "Персональный менеджер для премиум клиентов",
                "Приоритетное обслуживание",
                "Эксклюзивные инвестиционные продукты"
            ]
        elif credit_score >= 700:
            return [
                "Увеличение кредитных лимитов",
                "Снижение процентных ставок",
                "Инвестиционные консультации"
            ]
        elif credit_score >= 600:
            return [
                "Оптимизация кредитного портфеля",
                "Программы улучшения кредитной истории",
                "Накопительные продукты"
            ]
        else:
            return [
                "Финансовая грамотность",
                "Бюджетное планирование",
                "Кредитные каникулы"
            ]

# Глобальный экземпляр сервиса
financial_offers_service = FinancialOffersService()
