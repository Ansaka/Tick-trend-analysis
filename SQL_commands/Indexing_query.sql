CREATE INDEX idx_trading_data_symbol ON public.trading_data (symbol);
CREATE INDEX idx_trading_data_timestamp ON public.trading_data (date, "time");