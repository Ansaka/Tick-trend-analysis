from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from datetime import datetime
import json
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
load_dotenv()

# Get environment variables
db_user = os.getenv('DB_USER')
db_password = quote_plus(os.getenv('DB_PASSWORD'))
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

@app.get("/api/stock-data/{symbol}")
async def get_stock_data(symbol: str, date: str = None):
    query = """
    WITH time_windows AS (
        SELECT 
            symbol,
            date,
            date_trunc('hour', time) + 
                INTERVAL '5 minutes' * FLOOR(EXTRACT(MINUTE FROM time) / 5) as window_start,
            LAST_VALUE(last) OVER (
                PARTITION BY 
                    symbol, 
                    date, 
                    date_trunc('hour', time) + INTERVAL '5 minutes' * FLOOR(EXTRACT(MINUTE FROM time) / 5)
                ORDER BY time
                RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            ) as last_price
        FROM trading_data
        WHERE symbol = :symbol
        AND date = :date
    )
    SELECT 
        window_start as time,
        last_price as price
    FROM time_windows
    GROUP BY window_start, last_price
    ORDER BY window_start;
    """
    
    with engine.connect() as connection:
        result = connection.execute(
            text(query), 
            {"symbol": symbol, "date": date or datetime.now().strftime('%Y-%m-%d')}
        )
        data = [{"time": str(row[0]), "price": float(row[1])} for row in result]
        return data
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)