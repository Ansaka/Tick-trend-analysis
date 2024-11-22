CREATE TABLE trading_data (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20),
    sectype VarChar(3),
    date DATE,
    time TIME(3),
    last NUMERIC
);