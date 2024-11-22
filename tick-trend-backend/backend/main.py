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
async def get_stock_data(symbol: str, start_date: str = None, end_date: str = None):
    print(f"Debug: symbol={symbol}, start_date={start_date}, end_date={end_date}")
    
    query = """
    SELECT symbol, date + time as datetime, last 
    FROM trading_data_5min_filled
    WHERE symbol = :symbol 
    AND date BETWEEN :start_date AND :end_date
    ORDER BY date + time;
    """
    
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text(query), 
                {
                    "symbol": symbol,
                    "start_date": start_date,
                    "end_date": end_date
                }
            )
            data = [
                {
                    "datetime": row[1].isoformat() if row[1] else None, 
                    "price": float(row[2]) if row[2] else None
                } 
                for row in result
            ]
            print(f"Debug: Found {len(data)} records")
            return data
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}
    

@app.get("/api/symbols")
async def get_symbols(search: str = ""):
    query = """
    SELECT DISTINCT symbol 
    FROM trading_symbols
    WHERE symbol ILIKE :search
    ORDER BY symbol
    LIMIT 50;
    """
    
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text(query),
                {"search": f"%{search}%"}
            )
            symbols = [row[0] for row in result]
            return symbols
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)