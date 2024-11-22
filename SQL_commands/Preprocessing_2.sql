-- Preprocess by creating a temporary table with minimal data
CREATE TEMP TABLE temp_trading_data AS
SELECT 
    symbol,
    date + "time" AS timestamp,
    last
FROM public.trading_data;

-- Index the temporary table for faster lookups
CREATE INDEX idx_temp_trading_data ON temp_trading_data (symbol, timestamp);

-- Now generate the 5-minute intervals and join with the temp data
CREATE TABLE public.trading_data_5min_filled AS
WITH symbols AS (
    SELECT DISTINCT symbol FROM public.trading_data
),
all_intervals AS (
    SELECT generate_series(
        (SELECT MIN(date) FROM public.trading_data) + time '00:00',
        (SELECT MAX(date) FROM public.trading_data) + time '23:55',
        interval '5 minutes'
    ) AS interval_start
),
all_combinations AS (
    SELECT 
        s.symbol, 
        ai.interval_start::timestamp AS interval_start
    FROM symbols s
    CROSS JOIN all_intervals ai
)
-- Use a LEFT JOIN and a simpler method to carry forward prices
SELECT 
    ac.symbol,
    ac.interval_start::date AS date,
    ac.interval_start::time AS time,
    (SELECT td.last 
     FROM temp_trading_data td 
     WHERE td.symbol = ac.symbol 
       AND td.timestamp <= ac.interval_start
     ORDER BY td.timestamp DESC
     LIMIT 1) AS last
FROM all_combinations ac
ORDER BY ac.symbol, ac.interval_start;
