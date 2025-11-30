import pandas as pd

csv_file = "backend/database/data.csv"             
clean_csv_file = "backend/database/data_clean.csv" 
table_name = "client_data"
schema = "public"
sql_file = "backend/database/create_client_data.sql"

target_columns = [
    "id",
    "dt",
    "target",
    "turn_cur_cr_avg_act_v2",
    "salary_6to12m_avg",
    "hdb_bki_total_max_limit",
    "dp_ils_paymentssum_avg_12m",
    "hdb_bki_total_cc_max_limit",
    "incomeValue",
    "gender",
    "avg_cur_cr_turn",
    "adminarea",
    "turn_cur_cr_avg_v2",
    "turn_cur_cr_max_v2",
    "hdb_bki_total_pil_max_limit",
    "age",
    "dp_ils_avg_salary_1y",
    "turn_cur_cr_sum_v2",
    "by_category__amount__sum__eoperation_type_name__ishod_d39dc1",
    "turn_cur_db_sum_v2",
    "turn_cur_db_avg_act_v2",
    "dp_ils_avg_salary_2y",
    "curr_rur_amt_cm_avg",
    "turn_cur_db_avg_v2",
    "by_category__amount__sum__eoperation_type_name__vhodj_533a7d",
    "dp_ils_paymentssum_avg_6m",
    "avg_cur_db_turn",
    "hdb_bki_active_cc_max_limit",
    "incomeValueCategory",
    "avg_amount_cashflowcategory_nalychka_bankomat",
    "avg_credit_turn_rur",
    "dp_ils_salary_ratio_1y3y",
    "by_category__amount__sum__eoperation_type_name__perev_0ede3b",
    "turn_cur_cr_7avg_avg_v2",
    "dp_ils_accpayment_avg_12m",
    "curbal_usd_amt_cm_avg",
    "avg_amount_cashflowcategory_supermarkety",
    "avg_loan_cnt_with_insurance",
    "avg_amount_cashflowcategory_gipermarkety",
    "city_smart_name",
    "uniV5",
    "turn_cur_db_max_v2",
    "avg_amount_cashflowcategory_kafe",
    "turn_other_db_max_v2",
    "turn_cur_cr_min_v2",
    "hdb_bki_other_active_pil_outstanding",
    "dp_ewb_last_employment_position",
    "turn_cur_db_min_v2",
    "hdb_bki_total_products",
    "per_capita_income_rur_amt",
    "avg_debet_turn_rur",
    "hdb_relend_active_max_psk",
    "dda_rur_amt_curr_v2",
    "mob_cnt_days",
    "dp_ils_days_from_last_doc",
    "avg_6m_money_transactions",
    "transaction_category_supermarket_percent_cnt_2m",
    "pil",
    "hdb_bki_total_max_overdue_sum",
    "avg_6m_clothing",
    "avg_amount_cashflowcategory_electro_money",
    "addrref",
    "bki_total_auto_cnt",
    "dp_payoutincomedata_payout_avg_3_month",
    "hdb_outstand_sum",
    "avg_3m_money_transactions",
    "dp_address_unique_regions",
    "min_balance_rur_amt_6m_af",
    "transaction_category_supermarket_sum_cnt_m3_4",
    "dp_payoutincomedata_payout_max_3_month",
    "hdb_bki_total_ip_max_limit",
    "hdb_bki_total_cnt",
    "blacklist_flag",
    "bki_total_oth_cnt",
    "dp_payoutincomedata_payout_sum_3_month",
    "hdb_relend_outstand_sum",
    "total_rur_amt_cm_avg",
    "mob_cover_days",
    "dp_payoutincomedata_payout_max_6_month",
    "label_Below_50k_share_r1",
    "turn_fdep_db_sum_v2",
    "dp_ils_accpayment_avg_6m_current",
    "transaction_category_cash_percent_amt_2m",
    "curr_rur_amt_3m_avg",
    "transaction_category_restaurants_sum_amt_m2",
    "loan_cnt",
    "turn_fdep_db_avg_v2",
    "turn_cur_db_7avg_avg_v2",
    "bki_total_ip_max_outstand",
    "amount_by_category_90d__summarur_amt__sum__cashflowca_c17531",
    "profit_income_out_rur_amt_12m",
    "avg_6m_hotels",
    "hdb_ovrd_sum",
    "dp_ils_total_seniority",
    "dp_ils_paymentssum_avg_6m_current",
    "smsInWavg6m",
    "avg_fdep_db_turn",
    "device_iphone_avg",
    "by_category__amount__sum__eoperation_type_name__plate_77b562",
    "avg_balance_rur_amt_1m_af",
    "curr_rur_amt_cm_avg_period_days_ago_v2",
    "avg_amount_cashflowcategory_oteli",
    "hdb_bki_total_ip_cnt",
    "hdb_bki_active_cc_max_outstand",
    "hdb_other_outstand_sum",
    "days_to_last_transaction",
    "hdb_bki_total_pil_max_overdue",
    "vert_pil_last_credit_step_screen_view_3m",
    "acard",
    "bki_total_il_max_limit",
    "other_credits_count",
    "tz_msk_timedelta",
    "turn_save_db_min_v2",
    "profit_income_out_rur_amt_9m",
    "dp_ils_ipkcurrentyear_currentyearpensfactor",
    "avg_amount__cashflowcategory_odezhda",
    "cntOnnRinCallAvg6m",
    "dda_rur_amt_3m_avg",
    "winback_cnt",
    "salary_median_in_gex_r1",
    "dp_payoutincomedata_payout_avg_prev_year",
    "avg_amount_daily_transactions_90d",
    "vert_has_app_ru_tinkoff_investing",
    "transaction_category_supermarket_inc_cnt_2m",
    "vert_pil_sms_success_3m",
    "min_balance_rur_amt_1m_af",
    "dp_ils_max_seniority",
    "avg_amount_cashflowcategory_set_supermarketov",
    "label_500k_to_1M_share_r1",
    "avg_amount_cashflowcategory_zarubezhnye_finansovye_operatsii",
    "bki_total_products",
    "avg_6m_all",
    "dp_ils_avg_simultanious_jobs_5y",
    "dp_ewb_dismissal_due_contract_violation_by_lb_cnt",
    "summarur_1m_purch",
    "diff_avg_cr_db_turn",
    "dp_ils_cnt_changes_1y",
    "dp_ils_employeers_cnt_last_month",
    "dp_payoutincomedata_payout_avg_6_month",
    "dp_ewb_last_organization",
    "by_category__amount__sum__eoperation_type_name__perev_e3d03b",
    "bki_active_auto_cnt",
    "turn_other_cr_avg_act_v2",
    "cntVoiceOutMob6m",
    "avg_amount_cashflowcategory_puteshestvija",
    "loanacc_rur_amt_cm_avg",
    "transaction_category_supermarket_sum_cnt_m2",
    "transaction_category_supermarket_sum_amt_d15",
    "avg_fdep_cr_turn",
    "transaction_category_restaurants_percent_cnt_2m",
    "bki_total_max_limit",
    "avg_amount_cashflowcategory_reklama_v_internete",
    "transaction_category_restaurants_percent_amt_2m",
    "turn_fdep_db_avg_act_v2",
    "dp_ils_accpayment_avg_6m",
    "turn_other_cr_sum_v2",
    "client_active_flag",
    "avg_amount_cashflowcategory_producty",
    "curr_rur_amt_cm_avg_inc_v2",
    "nonresident_flag",
    "avg_amount_cashflowcategory_kosmetika",
    "vert_has_app_ru_vtb_invest",
    "dp_ils_avg_salary_3y",
    "hdb_bki_total_auto_max_limit",
    "days_after_last_request",
    "cntRegionTripsWavg1m",
    "vert_has_app_ru_cian_main",
    "loanacc_rur_amt_curr_v2",
    "avg_3m_no_cat",
    "vert_ghost_close_dpay3_last_days",
    "vert_has_app_ru_raiffeisennews",
    "dp_ils_days_ip_share_5y",
    "avg_amount_cashflowcategory_platezhi_cherez_internet",
    "hdb_bki_total_micro_max_overdue",
    "bki_total_active_products",
    "by_category__amount__sum__eoperation_type_name__perev_9f9da8",
    "calledCtnOutGroup",
    "vert_pil_loan_application_success_3m",
    "vert_pil_fee_discount_change_3m",
    "businessTelSubs",
    "profit_income_out_rur_amt_l2m",
    "avg_3m_healthcare_services",
    "dp_ils_paymentssum_month_avg",
    "ovrd_sum",
    "hdb_bki_total_active_products",
    "hdb_bki_total_micro_cnt",
    "hdb_bki_active_pil_cnt",
    "loan_cur_amt",
    "mob_total_sessions",
    "period_last_act_ad",
    "dp_ils_days_multiple_job_share_2y",
    "hdb_bki_total_cc_max_overdue",
    "lifetimeComp",
    "hdb_bki_total_pil_last_days",
    "amount_by_category_90d__summarur_amt__sum__cashflowca_8cd199",
    "turn_save_cr_max_v2",
    "hdb_bki_active_pil_max_limit",
    "dp_ils_accpayment_avg_3m",
    "avg_6m_restaurants",
    "hdb_bki_total_pil_cnt",
    "transaction_category_fastfood_percent_cnt_2m",
    "hdb_bki_total_pil_max_del90",
    "accountsalary_out_flag",
    "cntBlockWavg6m",
    "express_rur_amt_cm_avg",
    "loanacc_rur_amt_cm_avg_inc_v2",
    "hdb_bki_last_product_days",
    "dp_ils_days_multiple_job_cnt_5y",
    "dp_ils_accpayment_month_avg",
    "cred_dda_rur_amt_3m_avg",
    "avg_3m_all",
    "hdb_other_active_max_psk",
    "hdb_bki_other_active_ip_outstanding",
    "total_sum",
    "dp_ils_uniq_companies_1y",
    "avg_6m_travel",
    "avg_6m_government_services",
    "hdb_bki_active_cc_max_overdue",
    "total_rur_amt_cm_avg_period_days_ago_v2",
    "label_Above_1M_share_r1",
    "transaction_category_supermarket_sum_cnt_d15",
    "max_balance_rur_amt_1m_af",
    "w",
    "first_salary_income"
]

# --- Чтение CSV ---
df = pd.read_csv(csv_file, sep=';')

# Проверка количества колонок
if len(df.columns) != len(target_columns):
    raise ValueError(
        f"❌ Количество колонок в CSV ({len(df.columns)}) "
        f"не совпадает с количеством целевых колонок ({len(target_columns)})"
    )

# --- Замена имён колонок по порядку ---
df.columns = target_columns

# --- Очистка CSV ---
df.replace("None", pd.NA, inplace=True)
df.to_csv(clean_csv_file, sep=';', index=False)

# --- Определение типа колонок ---
def detect_type(series):
    if pd.api.types.is_integer_dtype(series):
        return "integer"
    elif pd.api.types.is_float_dtype(series):
        return "numeric"
    else:
        try:
            pd.to_datetime(series.dropna(), errors='raise', infer_datetime_format=True)
            return "date"
        except:
            return "text"

# --- Генерация SQL ---
columns_sql = []
for col in df.columns:
    col_type = detect_type(df[col])
    not_null = "NOT NULL" if df[col].notna().all() else ""
    columns_sql.append(f'"{col}" {col_type} {not_null}'.strip())

columns_sql_str = ",\n    ".join(columns_sql)

sql_script = f"""
DROP TABLE IF EXISTS {schema}.{table_name};

CREATE TABLE {schema}.{table_name} (
    {columns_sql_str}
);

COPY {schema}.{table_name}
FROM '{clean_csv_file}'
DELIMITER ';'
CSV HEADER
NULL '';
"""

with open(sql_file, "w", encoding="utf-8") as f:
    f.write(sql_script)

print("Готово!")
print(f"✔ CSV сохранён: {clean_csv_file}")
print(f"✔ SQL создан: {sql_file}")






# import pandas as pd
# import hashlib

# # --- Параметры ---
# csv_file = "./data.csv"             # исходный CSV
# clean_csv_file = "./data_clean.csv" # очищенный CSV для COPY
# table_name = "client_data"
# schema = "public"
# sql_file = "./create_client_data.sql"

# # --- Чтение CSV и очистка данных ---
# df = pd.read_csv(csv_file, sep=';')

# # Заменяем строковые 'None' и пустые строки на NA (NULL)
# df.replace("None", pd.NA, inplace=True)

# # Сохраняем очищенный CSV
# df.to_csv(clean_csv_file, sep=';', index=False)

# # --- Определение типов колонок ---
# def detect_type(series):
#     if pd.api.types.is_integer_dtype(series):
#         return "integer"
#     elif pd.api.types.is_float_dtype(series):
#         return "numeric"
#     else:
#         try:
#             pd.to_datetime(series.dropna(), errors='raise', infer_datetime_format=True)
#             return "date"
#         except:
#             return "text"

# # --- Функция для безопасного сокращения длинных имен колонок ---
# def shorten_column_name(col, max_len=60):
#     if len(col) <= max_len:
#         return col
#     h = hashlib.md5(col.encode()).hexdigest()[:6]
#     return f"{col[:max_len-7]}_{h}"  # оставляем место для "_" + хеш

# # --- Генерация SQL ---
# columns_sql = []
# seen = set()
# for col in df.columns:
#     col_type = detect_type(df[col])
#     col_safe = shorten_column_name(col)
#     # проверка уникальности
#     while col_safe in seen:
#         col_safe = shorten_column_name(col_safe + "_dup")
#     seen.add(col_safe)
#     # проверка NOT NULL по всем строкам
#     not_null = "NOT NULL" if df[col].notna().all() else ""
#     columns_sql.append(f'"{col_safe}" {col_type} {not_null}'.strip())

# columns_sql_str = ",\n    ".join(columns_sql)

# # --- SQL-скрипт ---
# sql_script = f"""
# DROP TABLE IF EXISTS {schema}.{table_name};

# CREATE TABLE {schema}.{table_name} (
#     {columns_sql_str}
# );

# COPY {schema}.{table_name}
# FROM '{clean_csv_file}'
# DELIMITER ';'
# CSV HEADER
# NULL '';
# """

# # --- Сохраняем SQL ---
# with open(sql_file, "w", encoding="utf-8") as f:
#     f.write(sql_script)

# print(f"Очищенный CSV сохранён: {clean_csv_file}")
# print(f"Безопасный SQL-скрипт создан: {sql_file}")





# import pandas as pd
# import hashlib

# # --- Параметры ---
# csv_file = "/Users/bottleal/Desktop/data.csv"            # исходный CSV
# clean_csv_file = "/Users/bottleal/Desktop/data_clean.csv" # очищенный CSV для COPY
# table_name = "client_data"
# schema = "public"
# sql_file = "/Users/bottleal/Desktop/create_client_data_safe.sql"
# sample_rows = 100  # количество строк для определения типов

# # --- Чтение CSV и очистка данных ---
# df = pd.read_csv(csv_file, sep=';')

# # Заменяем строковые 'None' на пустые значения (NULL для PostgreSQL)
# df.replace("None", pd.NA, inplace=True)

# # Сохраняем очищенный CSV
# df.to_csv(clean_csv_file, sep=';', index=False)

# # --- Определение типов колонок ---
# df_sample = df.head(sample_rows)

# def detect_type(series):
#     if pd.api.types.is_integer_dtype(series):
#         return "integer"
#     elif pd.api.types.is_float_dtype(series):
#         return "numeric"
#     else:
#         # Попытка определить дату
#         try:
#             pd.to_datetime(series.dropna(), errors='raise', infer_datetime_format=True)
#             return "date"
#         except:
#             return "text"

# # --- Функция для безопасного сокращения длинных имен колонок ---
# def shorten_column_name(col, max_len=60):
#     if len(col) <= max_len:
#         return col
#     h = hashlib.md5(col.encode()).hexdigest()[:6]
#     return f"{col[:max_len-7]}_{h}"  # оставляем место для "_" + хеш

# # --- Генерация SQL ---
# columns_sql = []
# seen = set()
# for col in df_sample.columns:
#     col_type = detect_type(df_sample[col])
#     col_safe = shorten_column_name(col)
#     while col_safe in seen:
#         col_safe = shorten_column_name(col_safe + "_dup")
#     seen.add(col_safe)
#     not_null = "NOT NULL" if df_sample[col].notna().all() else ""
#     columns_sql.append(f'"{col_safe}" {col_type} {not_null}'.strip())

# columns_sql_str = ",\n    ".join(columns_sql)

# sql_script = f"""
# DROP TABLE IF EXISTS {schema}.{table_name};

# CREATE TABLE {schema}.{table_name} (
#     {columns_sql_str}
# );

# COPY {schema}.{table_name}
# FROM '{clean_csv_file}'
# DELIMITER ';'
# CSV HEADER
# NULL '';
# """

# # --- Сохраняем SQL ---
# with open(sql_file, "w", encoding="utf-8") as f:
#     f.write(sql_script)

# print(f"Очищенный CSV сохранён: {clean_csv_file}")
# print(f"Безопасный SQL-скрипт создан: {sql_file}")





# import pandas as pd
# import hashlib

# # Параметры
# csv_file = "/Users/bottleal/Desktop/data.csv"
# table_name = "client_data"
# schema = "public"
# sql_file = "create_client_data_safe.sql"

# # Считываем CSV (первые 100 строк для определения типов)
# df_sample = pd.read_csv(csv_file, sep=';', nrows=100)

# # Функция определения типа колонки
# def detect_type(series):
#     if pd.api.types.is_integer_dtype(series):
#         return "integer"
#     elif pd.api.types.is_float_dtype(series):
#         return "numeric"
#     else:
#         try:
#             pd.to_datetime(series, errors='raise')
#             return "date"
#         except:
#             return "text"

# # Функция для безопасного сокращения длинных имён колонок
# def shorten_column_name(col, max_len=60):
#     if len(col) <= max_len:
#         return col
#     # добавляем короткий хеш, чтобы гарантировать уникальность
#     h = hashlib.md5(col.encode()).hexdigest()[:6]
#     return f"{col[:max_len-7]}_{h}"  # -7: оставляем место для "_" + 6 символов хеша

# # Генерируем колонки для CREATE TABLE
# columns_sql = []
# seen = set()
# for col in df_sample.columns:
#     col_type = detect_type(df_sample[col])
#     col_safe = shorten_column_name(col)
#     # Проверка уникальности
#     while col_safe in seen:
#         col_safe = shorten_column_name(col_safe + "_dup")
#     seen.add(col_safe)
#     not_null = "NOT NULL" if df_sample[col].notna().all() else ""
#     columns_sql.append(f'"{col_safe}" {col_type} {not_null}'.strip())

# columns_sql_str = ",\n    ".join(columns_sql)

# # Генерация SQL-скрипта
# sql_script = f"""
# DROP TABLE IF EXISTS {schema}.{table_name};

# CREATE TABLE {schema}.{table_name} (
#     {columns_sql_str}
# );

# COPY {schema}.{table_name}
# FROM '{csv_file}'
# DELIMITER ';'
# CSV HEADER;
# """

# # Сохраняем SQL
# with open(sql_file, "w", encoding="utf-8") as f:
#     f.write(sql_script)

# print(f"Безопасный SQL-скрипт создан: {sql_file}")




# import pandas as pd

# # Параметры
# csv_file = "Users/bottleal/Desktop/data.csv"
# table_name = "client_data"
# schema = "public"
# sql_file = "create_client_data_auto_advanced.sql"

# # Считываем первые N строк для определения типов (например, 100 строк)
# df_sample = pd.read_csv(csv_file, sep=';', nrows=100)

# # Функция для определения типа колонки
# def detect_type(series):
#     # Проверка на integer
#     if pd.api.types.is_integer_dtype(series):
#         return "integer"
#     # Проверка на float
#     elif pd.api.types.is_float_dtype(series):
#         return "numeric"
#     # Попробуем проверить, можно ли преобразовать в дату
#     else:
#         try:
#             pd.to_datetime(series, errors='raise')
#             return "date"
#         except:
#             return "text"

# # Генерируем колонки для CREATE TABLE
# columns_sql = []
# for col in df_sample.columns:
#     col_type = detect_type(df_sample[col])
#     col_name = f'"{col}"'
#     not_null = "NOT NULL" if df_sample[col].notna().all() else ""
#     columns_sql.append(f"{col_name} {col_type} {not_null}".strip())

# columns_sql_str = ",\n    ".join(columns_sql)

# # Полный SQL скрипт
# sql_script = f"""
# DROP TABLE IF EXISTS {schema}.{table_name};

# CREATE TABLE {schema}.{table_name} (
#     {columns_sql_str}
# );

# COPY {schema}.{table_name}
# FROM '{csv_file}'
# DELIMITER ';'
# CSV HEADER;
# """

# # Сохраняем SQL
# with open(sql_file, "w", encoding="utf-8") as f:
#     f.write(sql_script)

# print(f"Продвинутый SQL-скрипт создан: {sql_file}")





# import pandas as pd
# from datetime import datetime

# # Параметры
# csv_file = "/Users/bottleal/Desktop/data.csv"
# table_name = "client_data"
# schema = "public"
# sql_file = "create_client_data_auto.sql"

# # Считываем первые N строк для определения типов (например, 100 строк)
# df_sample = pd.read_csv(csv_file, sep=';', nrows=100)

# # Функция для определения типа колонки
# def detect_type(series):
#     if pd.api.types.is_integer_dtype(series):
#         return "integer"
#     elif pd.api.types.is_float_dtype(series):
#         return "numeric"
#     else:
#         # Попробуем проверить, можно ли преобразовать в дату
#         try:
#             pd.to_datetime(series, errors='raise')
#             return "date"
#         except:
#             return "text"

# # Генерируем колонки для CREATE TABLE
# columns_sql = []
# for col in df_sample.columns:
#     col_type = detect_type(df_sample[col])
#     # Если имя колонки содержит пробелы или спецсимволы, обрамляем в двойные кавычки
#     col_name = f'"{col}"'
#     columns_sql.append(f"{col_name} {col_type}")

# columns_sql_str = ",\n    ".join(columns_sql)

# # Собираем полный SQL скрипт
# sql_script = f"""
# DROP TABLE IF EXISTS {schema}.{table_name};

# CREATE TABLE {schema}.{table_name} (
#     {columns_sql_str}
# );

# COPY {schema}.{table_name}
# FROM '{csv_file}'
# DELIMITER ';'
# CSV HEADER;
# """

# # Сохраняем SQL
# with open(sql_file, "w", encoding="utf-8") as f:
#     f.write(sql_script)

# print(f"SQL-скрипт создан: {sql_file}")

