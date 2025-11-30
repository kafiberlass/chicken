import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from data_explorer import DataExplorer

def analyze_missing_columns(df, threshold=0.5, full_analysis=False, sort_alphabetical=False):
    """
    Анализ пропусков в DataFrame

    Parameters:
    - df: DataFrame для анализа
    - threshold: порог для удаления (0.0-1.0)
    - full_analysis: если True - показывать все столбцы с пропусками, если False - только выше порога
    - sort_alphabetical: если True - сортировать по алфавиту, если False - по убыванию процента пропусков
    """

    missing_percent = df.isnull().sum() / len(df)

    if full_analysis:
        # Режим полного анализа - все столбцы с пропусками
        missing_sorted = missing_percent[missing_percent > 0]
        print("ВСЕ столбцы с пропусками:")
    else:
        # Режим только столбцы выше порога
        missing_sorted = missing_percent[missing_percent > threshold]
        print(f"Столбцы с пропусками > {threshold:.0%}:")

    if sort_alphabetical:
        missing_sorted = missing_sorted.sort_index()
    else:
        missing_sorted = missing_sorted.sort_values(ascending=False)

    for col, percent in missing_sorted.items():
        missing_count = df[col].isnull().sum()
        print(f"{col}: {percent:.1%} ({missing_count} пропусков)")

    columns_to_drop = missing_sorted.index.tolist()

    print(f"\nВсего найдено: {len(columns_to_drop)} столбцов")
    return columns_to_drop


def analyze_rows_statistics(df, threshold=0.5, return_rows_to_drop=False):
    """
    Статистика пропусков по строкам с возможностью получить ID для удаления

    Parameters:
    - df: DataFrame для анализа
    - threshold: порог для определения строк к удалению (0.0-1.0)
    - return_rows_to_drop: если True - возвращает ID строк выше порога

    Returns:
    - Если return_rows_to_drop=False: возвращает Series с количеством пропусков по строкам
    - Если return_rows_to_drop=True: возвращает tuple (statistics_series, rows_to_drop_ids)
    """
    missing_per_row = df.isnull().sum(axis=1)
    total_columns = df.shape[1]
    missing_percent_per_row = missing_per_row / total_columns
    
    print("СТАТИСТИКА ПО СТРОКАМ:")
    print(f"Всего строк: {len(df)}")
    print(f"Всего столбцов: {total_columns}")
    print(f"Максимально возможное пропусков в строке: {total_columns}")
    print()
    
    # Распределение пропусков
    print("Распределение пропусков по строкам:")
    print(f"Строк без пропусков: {(missing_per_row == 0).sum()} ({(missing_per_row == 0).sum()/len(df):.1%})")
    print(f"Строк с 50%+ пропусками: {(missing_per_row > total_columns*0.5).sum()} ({(missing_per_row > total_columns*0.5).sum()/len(df):.1%})")
    print(f"Строк с 90%+ пропусками: {(missing_per_row > total_columns*0.9).sum()} ({(missing_per_row > total_columns*0.9).sum()/len(df):.1%})")
    
    # Получаем ID строк для удаления (выше порога)
    rows_to_drop_ids = missing_percent_per_row[missing_percent_per_row > threshold].index.tolist()
    print(f"\nСтрок для удаления (порог {threshold:.0%}): {len(rows_to_drop_ids)}")
    
    if return_rows_to_drop:
        return missing_per_row, rows_to_drop_ids
    else:
        return missing_per_row


def convert_basic_columns(df):
    df_copy = df.copy()

    # id -> int
    if 'id' in df_copy.columns:
        df_copy['id'] = pd.to_numeric(df_copy['id'], errors='coerce', downcast='integer')

    # w -> float
    if 'w' in df_copy.columns:
        df_copy['w'] = (df_copy['w'].astype(str)
                        .str.replace(r'\.', '', regex=True)
                        .str.replace(r',', '.', regex=True))
        df_copy['w'] = pd.to_numeric(df_copy['w'], errors='coerce')

    # target -> float
    if 'target' in df_copy.columns:
        df_copy['target'] = (df_copy['target'].astype(str)
                             .str.replace(r'\.', '', regex=True)
                             .str.replace(r',', '.', regex=True))
        df_copy['target'] = pd.to_numeric(df_copy['target'], errors='coerce')

    return df_copy

def analyze_realistic_selection(df):
    """Анализ отобранных признаков"""

    # Анализ заполненности
    total_rows = len(df)
    print(f"Всего клиентов: {total_rows}")
    print("\nЗАПОЛНЕННОСТЬ ПРИЗНАКОВ:")

    for col in df.columns:
        if col not in ['id', 'w', 'target']:
            filled_count = df[col].notna().sum()
            filled_pct = (filled_count / total_rows) * 100
            print(f"  {col}: {filled_count} ({filled_pct:.1f}%)")

    # Типы данных
    print(f"\nТИПЫ ДАННЫХ:")
    for dtype in df.dtypes.unique():
        cols = df.dtypes[df.dtypes == dtype].index.tolist()
        print(f"  {dtype}: {len(cols)} колонок")
        if dtype == 'object':
            for col in cols[:5]:  # покажем первые 5 object-колонок
                sample = df[col].dropna().head(3).tolist() if not df[col].isna().all() else []
                print(f"    - {col}: {sample}")


def identify_problem_features(df):
    """Выявляем признаки которые все еще требуют обработки"""
    problems = []

    problem_features = {
        'high_missing': [],      # >30% пропусков
        'object_type': [],       # Строковые типы
        'low_variance': []       # Мало уникальных значений
    }

    for col in df.columns:
        if col not in ['id', 'w', 'target']:
            # Пропуски
            missing_pct = (df[col].isna().sum() / len(df)) * 100
            if missing_pct > 30:
                problem_features['high_missing'].append((col, missing_pct))

            # Типы данных
            if df[col].dtype == 'object':
                problem_features['object_type'].append(col)
                problems.append(col)

            # Дисперсия (для не-null значений)
            if not df[col].isna().all():
                unique_count = df[col].nunique()
                if unique_count < 5:  # Мало уникальных значений
                    problem_features['low_variance'].append((col, unique_count))

    print("\n⚠️  ПРОБЛЕМНЫЕ ПРИЗНАКИ ДЛЯ ОБРАБОТКИ:")
    print(f"Высокие пропуски (>30%): {len(problem_features['high_missing'])}")
    for col, pct in problem_features['high_missing']:
        print(f"   - {col}: {pct:.1f}% пропусков")

    print(f"Строковые типы: {len(problem_features['object_type'])}")
    for col in problem_features['object_type']:
        print(f"   - {col}")

    print(f"Мало уникальных значений: {len(problem_features['low_variance'])}")

    return problem_features


def convert_numeric_strings(df, problems):
    """Преобразует строковые числовые признаки в float"""

    for col in problems:
        if col in df.columns and df[col].dtype == 'object':
            # Сохраняем информацию о пропусках до преобразования
            original_non_null = df[col].notna().sum()

            # Заменяем запятые на точки и преобразуем в float
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(',', '.', regex=False),
                errors='coerce'
            )

            # Проверяем результат
            new_non_null = df[col].notna().sum()
            print(f"{col}: {original_non_null} → {new_non_null} не-null значений")

    return df

class RobustAutoDataPreprocessor:
    def __init__(self):
        self.explorer = DataExplorer()
        self.numeric_imputer = None
        self.fitted_columns_ = []
        self.is_fitted = False

    def fit(self, df):
        """Анализирует данные и создает стратегии обработки"""
        self.explorer.analyze_data(df)
        self.fitted_columns_ = df.columns.tolist()

        numeric_cols = (self.explorer.numeric_columns +
                       self.explorer.string_numeric_columns)

        if numeric_cols:
            self.numeric_imputer = SimpleImputer(strategy='median')
            temp_df = df[numeric_cols].copy()

            for col in self.explorer.string_numeric_columns:
                if col in temp_df.columns:
                    temp_df[col] = self._safe_convert_to_numeric(temp_df[col])

            self.numeric_imputer.fit(temp_df)

        self.is_fitted = True
        return self

    def _safe_convert_to_numeric(self, series):
        """Безопасно преобразует строки в числа, заменяя запятые на точки"""
        converted = pd.to_numeric(
            series.astype(str).str.replace(',', '.', regex=False),
            errors='coerce'
        )
        return converted

    def transform(self, df):
        """Применяет преобразования, обрабатывая новые пропуски"""
        if not self.is_fitted:
            raise ValueError("Сначала вызови fit()!")

        df_copy = df.copy()

        # Проверяем колонки
        new_columns = set(df_copy.columns) - set(self.fitted_columns_)
        missing_columns = set(self.fitted_columns_) - set(df_copy.columns)

        if new_columns:
            print(f"В тестовых данных появились новые колонки: {new_columns}")
            df_copy = df_copy.drop(columns=new_columns)

        if missing_columns:
            print(f"В тестовых данных отсутствуют колонки: {missing_columns}")
            for col in missing_columns:
                df_copy[col] = np.nan

        # 1. ПРЕОБРАЗУЕМ СТРОКОВЫЕ ЧИСЛА ДО импьютера
        for col in self.explorer.string_numeric_columns:
            if col in df_copy.columns:
                df_copy[col] = self._safe_convert_to_numeric(df_copy[col])
                print(f"Преобразовано: {col} → numeric")

        # 2. Заполняем пропуски в числовых колонках
        numeric_cols = (self.explorer.numeric_columns +
                       self.explorer.string_numeric_columns)

        available_numeric_cols = [col for col in numeric_cols if col in df_copy.columns]

        if available_numeric_cols and self.numeric_imputer:
            # Убедимся, что все данные числовые перед импьютацией
            for col in available_numeric_cols:
                if df_copy[col].dtype == 'object':
                    df_copy[col] = self._safe_convert_to_numeric(df_copy[col])

            temp_data = self.numeric_imputer.transform(df_copy[available_numeric_cols])
            df_copy[available_numeric_cols] = temp_data
            print(f"Заполнены пропуски в {len(available_numeric_cols)} числовых колонках")

        # 3. Обрабатываем категориальные колонки
        for col in self.explorer.categorical_columns:
            if col in df_copy.columns:
                unique_count = df_copy[col].nunique()
                if unique_count < 10:
                    df_copy[col] = df_copy[col].astype('category').cat.codes
                    print(f"Закодировано: {col} ({unique_count} категорий)")

        # 4. Заполняем оставшиеся пропуски
        remaining_missing = df_copy.isnull().sum().sum()
        if remaining_missing > 0:
            print(f"Осталось пропусков: {remaining_missing}")

            # Сначала пробуем заполнить числовые колонки медианой
            numeric_cols = df_copy.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if df_copy[col].isna().any():
                    median_val = df_copy[col].median()
                    df_copy[col] = df_copy[col].fillna(median_val)

            # Остальные заполняем нулями
            df_copy = df_copy.fillna(0)
            print(f"Оставшиеся пропуски заполнены")

        return df_copy

    def fit_transform(self, df):
        return self.fit(df).transform(df)


def quick_preprocess(train_df, test_df=None):
    """
    Быстрая автоматическая обработка данных
    """
    print("Быстрая автоматическая обработка")

    preprocessor = RobustAutoDataPreprocessor()

    # Обрабатываем тренировочные данные
    train_processed = preprocessor.fit_transform(train_df)

    if test_df is not None:
        # Обрабатываем тестовые данные
        test_processed = preprocessor.transform(test_df)
        return train_processed, test_processed
    else:
        return train_processed
    

class AdvancedSalaryEnricher:
    """Продвинутое добавление зарплат с резервными стратегиями"""

    def __init__(self, salary_df, region_col='Среднемесячная зп', salary_col='2023'):
        self.salary_df = salary_df
        self.region_col = region_col
        self.salary_col = salary_col
        self.salary_mapping_ = {}
        self.region_hierarchy_ = {}
        self.fallback_salary_ = None

    def fit(self, df, y=None):  # Добавляем y=None для совместимости с sklearn
        """Создаем маппинги и стратегии"""
        # Основной маппинг
        salary_regions = self.salary_df[self.region_col].str.lower().str.strip()
        self.salary_mapping_ = dict(zip(salary_regions, self.salary_df[self.salary_col]))

        # Создаем иерархию регионов
        self._build_region_hierarchy(df)

        # Резервная зарплата
        self.fallback_salary_ = self.salary_df[self.salary_col].median()


        return self

    def _build_region_hierarchy(self, df):
        """Строим иерархию регионов для лучшего матчинга"""
        if 'city_smart_name' in df.columns and 'adminarea' in df.columns:
            for city, region in zip(df['city_smart_name'], df['adminarea']):
                if pd.notna(city) and pd.notna(region):
                    city_norm = str(city).lower().strip()
                    region_norm = str(region).lower().strip()
                    self.region_hierarchy_[city_norm] = region_norm

    def transform(self, df):
        """Добавляем зарплаты с интеллектуальным матчингом"""
        df_copy = df.copy()

        # Нормализуем названия
        df_copy['_adminarea_norm'] = df_copy['adminarea'].str.lower().str.strip()
        df_copy['_addrref_norm'] = df_copy['addrref'].str.lower().str.strip()
        if 'city_smart_name' in df_copy.columns:
            df_copy['_city_norm'] = df_copy['city_smart_name'].str.lower().str.strip()

        # Интеллектуальный поиск зарплаты
        def find_salary_advanced(row):
            # Приоритет 1: прямое совпадение adminarea
            if row['_adminarea_norm'] in self.salary_mapping_:
                return self.salary_mapping_[row['_adminarea_norm']]

            # Приоритет 2: прямое совпадение addrref
            elif row['_addrref_norm'] in self.salary_mapping_:
                return self.salary_mapping_[row['_addrref_norm']]

            # Приоритет 3: через город -> регион
            elif ('_city_norm' in row and
                  row['_city_norm'] in self.region_hierarchy_ and
                  self.region_hierarchy_[row['_city_norm']] in self.salary_mapping_):
                return self.salary_mapping_[self.region_hierarchy_[row['_city_norm']]]

            # Приоритет 4: резервная зарплата
            else:
                return self.fallback_salary_

        # Добавляем зарплату
        df_copy['salary'] = df_copy.apply(find_salary_advanced, axis=1)

        # Анализ покрытия
        self._analyze_coverage(df_copy)

        # Удаляем временные и исходные колонки
        temp_cols = ['_adminarea_norm', '_addrref_norm', '_city_norm',
                    'adminarea', 'addrref', 'city_smart_name']
        df_copy = df_copy.drop([col for col in temp_cols if col in df_copy.columns], axis=1)

        return df_copy

    def _analyze_coverage(self, df):
        """Анализирует качество матчинга"""
        total = len(df)
        matched = df['salary'].notna().sum()

        print(f"\n СТАТИСТИКА МАТЧИНГА ЗАРПЛАТ:")
        print(f" Найдены зарплаты для: {matched}/{total} ({matched/total*100:.1f}%)")
        print(f" Диапазон зарплат: {df['salary'].min():.0f} - {df['salary'].max():.0f}")
        print(f" Средняя зарплата: {df['salary'].mean():.0f}")

    def fit_transform(self, df, y=None):
        return self.fit(df, y).transform(df)