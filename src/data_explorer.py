import pandas as pd
import numpy as np

class DataExplorer:
    """Класс для исследования данных и автоматического определения типов колонок"""

    def __init__(self):
        self.column_types = {}
        self.numeric_columns = []
        self.categorical_columns = []
        self.string_numeric_columns = []
        self.high_missing_columns = []

    def analyze_data(self, df, exclude_columns=['id', 'w', 'target']):
        """Анализирует данные и определяет типы колонок"""

        print("Анализ данных")

        for col in df.columns:
            if col in exclude_columns:
                continue

            # Анализ пропусков
            missing_pct = (df[col].isna().sum() / len(df)) * 100
            if missing_pct > 30:
                self.high_missing_columns.append((col, missing_pct))

            # Определение типа данных
            if df[col].dtype in ['int64', 'float64']:
                self.column_types[col] = 'numeric'
                self.numeric_columns.append(col)

            elif df[col].dtype == 'object':
                if self._is_numeric_string(df[col]):
                    self.column_types[col] = 'string_numeric'
                    self.string_numeric_columns.append(col)
                else:
                    self.column_types[col] = 'categorical'
                    self.categorical_columns.append(col)

        self._print_analysis_report(df)
        return self.column_types

    def _is_numeric_string(self, series):
        """Проверяет, являются ли строковые значения числами"""
        non_null = series.dropna()
        if len(non_null) == 0:
            return False

        sample = non_null.head(100)
        numeric_count = 0

        for val in sample:
            str_val = str(val).replace(',', '.').strip()
            try:
                float(str_val)
                numeric_count += 1
            except (ValueError, TypeError):
                pass

        return numeric_count / len(sample) > 0.7  # 70% чисел

    def _print_analysis_report(self, df):
        """Печатает отчет об анализе"""
        print("\nОтчет об анализе данных:")
        print(f"Числовые колонки: {len(self.numeric_columns)}")
        for col in self.numeric_columns:
            unique_vals = df[col].nunique()
            print(f"   - {col}: {df[col].dtype}, {unique_vals} уникальных")

        print(f"Строковые числа: {len(self.string_numeric_columns)}")
        for col in self.string_numeric_columns:
            sample = df[col].dropna().head(3)
            print(f"   - {col}: {list(sample)}")

        print(f"Категориальные: {len(self.categorical_columns)}")
        for col in self.categorical_columns:
            unique_vals = df[col].nunique()
            sample = df[col].dropna().head(3) if unique_vals > 3 else df[col].unique()
            print(f"   - {col}: {unique_vals} уникальных → {list(sample)}")

        print(f"Много пропусков (>30%): {len(self.high_missing_columns)}")
        for col, pct in self.high_missing_columns:
            print(f"   - {col}: {pct:.1f}% пропусков")