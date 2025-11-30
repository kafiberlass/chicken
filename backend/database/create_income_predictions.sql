
DROP TABLE IF EXISTS public.income_predictions;

CREATE TABLE public.income_predictions (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    predicted_income NUMERIC NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

COPY public.income_predictions (client_id, predicted_income)
FROM 'backend/database/predictions_clean.csv'
CSV HEADER
NULL '';
