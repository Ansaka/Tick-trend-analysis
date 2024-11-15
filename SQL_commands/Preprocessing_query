-- Create a new table and populate it with the results of the query
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
),
trading_data_with_timestamps AS (
    SELECT 
        symbol,
        date + "time" AS timestamp,  -- Combine date and time into a timestamp
        last
    FROM public.trading_data
)
SELECT 
    ac.symbol,
    ac.interval_start::date AS date,
    ac.interval_start::time AS time,
    COALESCE(
        td.last, 
        LAG(td.last) OVER (PARTITION BY ac.symbol ORDER BY ac.interval_start)
    ) AS last
FROM all_combinations ac
LEFT JOIN trading_data_with_timestamps td 
ON ac.symbol = td.symbol AND ac.interval_start = td.timestamp
ORDER BY ac.symbol, ac.interval_start;
