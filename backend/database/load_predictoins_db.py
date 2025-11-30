import pandas as pd

csv_file = "backend/database/predictions.csv"              # исходный CSV
clean_csv_file = "backend/database/predictions_clean.csv"  # очищенный CSV
sql_file = "backend/database/create_income_predictions.sql"
table_name = "income_predictions"
schema = "public"

df = pd.read_csv(csv_file)

expected_columns = ["id", "target"]

if list(df.columns) != expected_columns:
    raise ValueError(
        f"❌ Ошибка: ожидаются колонки {expected_columns}, "
        f"но получены: {list(df.columns)}"
    )

df.replace("None", pd.NA, inplace=True)

df.to_csv(clean_csv_file, index=False)

sql_script = f"""
DROP TABLE IF EXISTS {schema}.{table_name};

CREATE TABLE {schema}.{table_name} (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    predicted_income NUMERIC NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- COPY должен соответствовать колонкам таблицы (кроме SERIAL и created_at)
COPY {schema}.{table_name} (client_id, predicted_income)
FROM '{clean_csv_file}'
CSV HEADER
NULL '';
"""

with open(sql_file, "w", encoding="utf-8") as f:
    f.write(sql_script)

print("Готово!")
print(f"✔ Очищенный CSV сохранён: {clean_csv_file}")
print(f"✔ SQL со структурой и COPY создан: {sql_file}")
