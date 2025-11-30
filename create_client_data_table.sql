-- Создание таблицы client_data для 78,000 клиентов с 200+ колонками
-- На основе предоставленных данных о колонках

CREATE TABLE IF NOT EXISTS client_data (
    id SERIAL PRIMARY KEY,

    -- Базовые данные клиента
    age INTEGER,
    gender VARCHAR(10),
    adminarea VARCHAR(100),
    city_smart_name VARCHAR(100),

    -- Финансовые показатели
    incomeValue DECIMAL(12,2),
    incomeValueCategory INTEGER,
    uniV5 DECIMAL(5,4),

    -- BKI данные
    bki_active_auto_cnt DECIMAL(5,2),
    bki_total_active_products DECIMAL(5,2),
    bki_total_auto_cnt DECIMAL(5,2),
    bki_total_il_max_limit DECIMAL(12,2),
    bki_total_max_limit DECIMAL(12,2),
    bki_total_oth_cnt DECIMAL(5,2),
    bki_total_products DECIMAL(5,2),
    blacklist_flag INTEGER,

    -- Телеком данные
    businessTelSubs INTEGER,
    cntBlockWavg6m DECIMAL(8,4),
    cntRegionTripsWavg1m DECIMAL(8,4),
    cntVoiceOutMob6m DECIMAL(10,4),
    days_after_last_request INTEGER,
    smsInWavg6m DECIMAL(10,4),

    -- Балансы и обороты
    cred_dda_rur_amt_3m_avg DECIMAL(12,2),
    curr_rur_amt_3m_avg DECIMAL(12,2),
    curr_rur_amt_cm_avg DECIMAL(12,2),
    curr_rur_amt_cm_avg_inc_v2 DECIMAL(12,2),
    curr_rur_amt_cm_avg_period_days_ago_v2 DECIMAL(12,2),
    curr_rur_amt_cm_avg_v2 DECIMAL(12,2),
    curbal_usd_amt_cm_avg DECIMAL(12,2),
    dda_rur_amt_3m_avg DECIMAL(12,2),
    dda_rur_amt_curr_v2 DECIMAL(12,2),
    diff_avg_cr_db_turn DECIMAL(12,2),
    express_rur_amt_cm_avg DECIMAL(12,2),
    loanacc_rur_amt_cm_avg DECIMAL(12,2),
    loanacc_rur_amt_cm_avg_inc_v2 DECIMAL(12,2),
    loanacc_rur_amt_curr_v2 DECIMAL(12,2),
    total_rur_amt_cm_avg DECIMAL(12,2),
    total_rur_amt_cm_avg_period_days_ago_v2 DECIMAL(12,2),

    -- Обороты
    avg_credit_turn_rur DECIMAL(12,2),
    avg_cur_cr_turn DECIMAL(12,2),
    avg_cur_db_turn DECIMAL(12,2),
    avg_debet_turn_rur DECIMAL(12,2),
    avg_fdep_cr_turn DECIMAL(12,2),
    avg_fdep_db_turn DECIMAL(12,2),
    turn_cur_cr_7avg_avg_v2 DECIMAL(12,2),
    turn_cur_cr_avg_act_v2 DECIMAL(12,2),
    turn_cur_cr_avg_v2 DECIMAL(12,2),
    turn_cur_cr_max_v2 DECIMAL(12,2),
    turn_cur_cr_min_v2 DECIMAL(12,2),
    turn_cur_cr_sum_v2 DECIMAL(12,2),
    turn_cur_db_7avg_avg_v2 DECIMAL(12,2),
    turn_cur_db_avg_act_v2 DECIMAL(12,2),
    turn_cur_db_avg_v2 DECIMAL(12,2),
    turn_cur_db_max_v2 DECIMAL(12,2),
    turn_cur_db_min_v2 DECIMAL(12,2),
    turn_cur_db_sum_v2 DECIMAL(12,2),
    turn_other_cr_avg_act_v2 DECIMAL(12,2),
    turn_other_cr_sum_v2 DECIMAL(12,2),
    turn_other_db_max_v2 DECIMAL(12,2),

    -- Операционный доход
    profit_income_out_rur_amt_12m DECIMAL(12,2),
    profit_income_out_rur_amt_9m DECIMAL(12,2),
    profit_income_out_rur_amt_l2m DECIMAL(12,2),

    -- Транзакции и расходы
    avg_3m_all DECIMAL(12,2),
    avg_3m_healthcare_services DECIMAL(12,2),
    avg_3m_money_transactions DECIMAL(12,2),
    avg_3m_no_cat DECIMAL(12,2),
    avg_6m_all DECIMAL(12,2),
    avg_6m_clothing DECIMAL(12,2),
    avg_6m_government_services DECIMAL(12,2),
    avg_6m_hotels DECIMAL(12,2),
    avg_6m_money_transactions DECIMAL(12,2),
    avg_6m_restaurants DECIMAL(12,2),
    avg_6m_travel DECIMAL(12,2),
    avg_amount_daily_transactions_90d DECIMAL(10,2),
    summarur_1m_purch DECIMAL(10,2),

    -- Категории трат по месяцам
    avg_by_category__amount__sum__cashflowcategory_name__elektronnye_dengi DECIMAL(12,2),
    avg_by_category__amount__sum__cashflowcategory_name__gipermarkety DECIMAL(12,2),
    avg_by_category__amount__sum__cashflowcategory_name__kafe DECIMAL(12,2),
    avg_by_category__amount__sum__cashflowcategory_name__produkty DECIMAL(12,2),
    avg_by_category__amount__sum__cashflowcategory_name__supermarkety DECIMAL(12,2),
    avg_by_category__amount__sum__cashflowcategory_name__vydacha_nalichnyh_v_bankomate DECIMAL(12,2),

    -- Переводы
    by_category__amount__sum__eoperation_type_name__perevod_po_nomeru_telefona DECIMAL(12,2),

    -- Транзакции в категориях
    transaction_category_supermarket_inc_cnt_2m DECIMAL(5,2),
    transaction_category_supermarket_percent_cnt_2m DECIMAL(5,2),
    transaction_category_supermarket_sum_cnt_m2 INTEGER,
    transaction_category_supermarket_sum_cnt_m3_4 INTEGER,

    -- Мобильное приложение
    device_iphone_avg DECIMAL(3,2),
    mob_cnt_days INTEGER,
    mob_cover_days DECIMAL(5,4),
    mob_total_sessions INTEGER,

    -- Риски и просрочки
    total_sum DECIMAL(12,2),
    ovrd_sum DECIMAL(12,2),

    -- Статусы и флаги
    accountsalary_out_flag INTEGER,
    client_active_flag INTEGER,
    nonresident_flag INTEGER,

    -- Продукты других банков
    other_credits_count INTEGER,
    pil INTEGER,

    -- BKI детальная информация
    hdb_bki_active_cc_max_limit DECIMAL(12,2),
    hdb_bki_active_cc_max_outstand DECIMAL(12,2),
    hdb_bki_active_cc_max_overdue DECIMAL(12,2),
    hdb_bki_active_pil_cnt DECIMAL(5,2),
    hdb_bki_active_pil_max_limit DECIMAL(12,2),
    hdb_bki_last_product_days DECIMAL(8,2),
    hdb_bki_total_active_products DECIMAL(5,2),
    hdb_bki_total_cc_max_limit DECIMAL(12,2),
    hdb_bki_total_cc_max_overdue DECIMAL(12,2),
    hdb_bki_total_cnt DECIMAL(8,2),
    hdb_bki_total_ip_cnt DECIMAL(5,2),
    hdb_bki_total_max_limit DECIMAL(12,2),
    hdb_bki_total_max_overdue_sum DECIMAL(12,2),
    hdb_bki_total_micro_cnt DECIMAL(5,2),
    hdb_bki_total_pil_cnt DECIMAL(5,2),
    hdb_bki_total_pil_last_days DECIMAL(8,2),
    hdb_bki_total_pil_max_del90 DECIMAL(5,2),
    hdb_bki_total_pil_max_limit DECIMAL(12,2),
    hdb_bki_total_pil_max_overdue DECIMAL(12,2),
    hdb_bki_total_products DECIMAL(5,2),

    -- Риски других банков
    hdb_other_active_max_psk DECIMAL(8,2),
    hdb_other_outstand_sum DECIMAL(12,2),
    hdb_outstand_sum DECIMAL(12,2),
    hdb_ovrd_sum DECIMAL(12,2),
    hdb_relend_active_max_psk DECIMAL(8,2),
    hdb_relend_outstand_sum DECIMAL(12,2),

    -- Региональные данные
    per_capita_income_rur_amt DECIMAL(10,2),
    tz_msk_timedelta INTEGER,

    -- Время жизни и история
    lifetimeComp INTEGER,
    winback_cnt INTEGER,

    -- Приложения конкурентов
    vert_has_app_ru_cian_main INTEGER,
    vert_has_app_ru_raiffeisennews INTEGER,
    vert_has_app_ru_tinkoff_investing INTEGER,
    vert_has_app_ru_vtb_invest INTEGER,

    -- События в приложении
    vert_pil_fee_discount_change_3m INTEGER,
    vert_pil_last_credit_step_screen_view_3m INTEGER,
    vert_pil_loan_application_success_3m INTEGER,
    vert_pil_sms_success_3m INTEGER,

    -- Продукты Альфа-Банка
    acard INTEGER,

    -- Системные поля
    vert_ghost_close_dpay3_last_days INTEGER,
    dt TIMESTAMP,

    -- Индексы для производительности
    days_to_last_transaction INTEGER,

    -- Создание индексов
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание индексов для быстрого поиска
CREATE INDEX IF NOT EXISTS idx_client_data_id ON client_data(id);
CREATE INDEX IF NOT EXISTS idx_client_data_age ON client_data(age);
CREATE INDEX IF NOT EXISTS idx_client_data_region ON client_data(adminarea);
CREATE INDEX IF NOT EXISTS idx_client_data_income ON client_data(incomeValue);
CREATE INDEX IF NOT EXISTS idx_client_data_bki_active ON client_data(bki_total_active_products);
CREATE INDEX IF NOT EXISTS idx_client_data_mobile_sessions ON client_data(mob_total_sessions);
CREATE INDEX IF NOT EXISTS idx_client_data_credit_score ON client_data(uniV5);

-- Комментарий к таблице
COMMENT ON TABLE client_data IS 'Таблица с данными клиентов Альфа-Банка (78k клиентов, 200+ колонок)';
COMMENT ON COLUMN client_data.uniV5 IS 'Кредитный скоринг V5 (0-1 шкала)';
COMMENT ON COLUMN client_data.bki_total_active_products IS 'Количество активных кредитных продуктов по BKI';
