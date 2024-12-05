from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from datetime import datetime
import json
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
from google.cloud.sql.connector import Connector
from google.oauth2 import service_account
import pg8000.native

app = FastAPI()

# Load environment variables
load_dotenv()

frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the Google service account key path from the environment variable
google_service_account_key_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY_PATH")

# Load the JSON data from the file
if google_service_account_key_path:
    with open(google_service_account_key_path, 'r') as file:
        service_account_info = json.load(file)
else:
    raise ValueError("Variable for credentials is not set")

# Set the credentials environment variable directly
if service_account_info:
    credentials = service_account.Credentials.from_service_account_info(service_account_info)

# Initialize the Cloud SQL Python Connector
connector = Connector(credentials=credentials)

# Get database connection parameters
instance_connection_name = os.getenv("INSTANCE")
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Get backend parameters
host = os.getenv('HOST', '127.0.0.1')
port = int(os.getenv('PORT', 8000))

def getconn():
    return connector.connect(
        instance_connection_name,
        "pg8000",
        user=db_user,
        password=db_password,
        db=db_name,
    )

# Create SQLAlchemy engine using the connection pool
engine = create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

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
            
            # Drop leading None price data points
            first_valid_index = next((i for i, point in enumerate(data) if point['price'] is not None), len(data))
            data = data[first_valid_index:] 

            print(f"Debug: Found {len(data)} records")
            
            # EMA Calculation Variables
            j_values = [38, 100]  # Smoothing factors
            ema_values = {j: 0 for j in j_values}  # Initialize EMA^j_s,w0
            
            # To track previous EMAs for crossover detection
            previous_ema_38 = 0
            previous_ema_100 = 0
            
            # Calculate EMA and detect signals
            signals = []
            ema_rows = []
            
            for i, row in enumerate(data):
                close_price = row["price"]
                ema_row = {"datetime": row["datetime"], "price": close_price}
                
                # Calculate EMAs
                for j in j_values:
                    smoothing_factor = 2 / (1 + j)
                    ema_previous = ema_values[j]  # Get previous EMA

                    # Check for None values
                    if close_price is None or ema_previous is None:
                        continue  # Skip this iteration if any value is None

                    ema_current = (close_price * smoothing_factor) + (ema_previous * (1 - smoothing_factor))
                    ema_values[j] = ema_current  # Update EMA
                    
                    # Store EMA in the result
                    ema_row[f"ema_{j}"] = ema_current
                
                # Append the EMA row to the list
                ema_rows.append(ema_row)

                # Detect crossovers (buy/sell signals)
                current_ema_38 = ema_row.get("ema_38", 0)
                current_ema_100 = ema_row.get("ema_100", 0)
                
                if i > 0:  # Skip crossover detection for the first row
                    # Bullish breakout (Buy signal)
                    if current_ema_38 > current_ema_100 and previous_ema_38 <= previous_ema_100:
                        signals.append({
                            "datetime": ema_row["datetime"],
                            "signal": "BUY",
                            "price": close_price
                        })
                    
                    # Bearish breakout (Sell signal)
                    if current_ema_38 < current_ema_100 and previous_ema_38 >= previous_ema_100:
                        signals.append({
                            "datetime": ema_row["datetime"],
                            "signal": "SELL",
                            "price": close_price
                        })
                
                # Update previous EMA values for next iteration
                previous_ema_38 = current_ema_38
                previous_ema_100 = current_ema_100
            
            return {"data": data, "signals": signals, "ema_rows": ema_rows}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}
    

@app.get("/api/symbols")
async def get_symbols(search: str = ""):
    query = """
    SELECT symbol 
    FROM trading_symbols
    WHERE symbol ILIKE :search
    LIMIT 30;
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
    uvicorn.run(app, host=host, port=port)