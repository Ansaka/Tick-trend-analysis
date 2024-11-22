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
    print(f"Debug: symbol={symbol}, date={date}")  # Add debug logging
    
    query = """
    SELECT symbol, date + time as datetime, last 
    FROM trading_data_5min_filled
    WHERE symbol = :symbol AND date = :date
    ORDER BY date + time;
    """
    
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text(query), 
                {"symbol": symbol, "date": date}
            )
            data = [
                {
                    "datetime": row[1].isoformat() if row[1] else None, 
                    "price": float(row[2]) if row[2] else None
                } 
                for row in result
            ]
            print(f"Debug: Found {len(data)} records")  # Add debug logging
            return data
    except Exception as e:
        print(f"Error: {str(e)}")  # Add error logging
        return {"error": str(e)}
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)