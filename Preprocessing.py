import pandas as pd
from sqlalchemy import create_engine

# Step 1: Set up the database connection
db_user = 'my_user'
db_password = 'my_password'
db_host = 'localhost'  # or your database host
db_port = '5432'       # default PostgreSQL port
db_name = 'GoldenCross'

# Create a database engine
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Step 2: Define a function to read and process CSV files
def load_data_to_db(file_path):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path, skiprows=0, delimiter=',', low_memory=False)

        # Print the initial columns for debugging
        print(f"Columns in DataFrame before stripping: {df.columns.tolist()}")

        # Strip whitespace from all column names
        df.columns = df.columns.str.strip()

        # Print the columns after stripping whitespace
        print(f"Columns in DataFrame after stripping: {df.columns.tolist()}")

        # Rename columns to match PostgreSQL schema (lowercase)
        df.rename(columns={
            'ID': 'id',
            'SecType': 'sectype',
            'Date': 'date',
            'Time': 'time',
            'Ask': 'ask',
            'Ask volume': 'ask_volume',
            'Bid': 'bid',
            'Bid volume': 'bid_volume',
            'Ask time': 'ask_time',
            "Day's high ask": "days_high_ask",
            'Close': 'close',
            'Currency': 'currency',
            "Day's high ask time": "days_high_ask_time",
            "Day's high": 'days_high',
            'ISIN': 'isin',
            'Auction price': 'auction_price',
            "Day's low ask": "days_low_ask",
            "Day's low": 'days_low',
            "Day's low ask time": "days_low_ask_time",
            'Open': 'open',
            'Nominal value': 'nominal_value',
            'Last': 'last',
            'Last volume': 'last_volume',
            'Trading time': 'trading_time',
            'Total volume': 'total_volume',
            'Mid price': 'mid_price',
            'Trading date': 'trading_date',
            'Profit': 'profit',
            'Current price': 'current_price',
            'Related indices': 'related_indices',
            'Day high bid time': 'day_high_bid_time',
            'Day low bid time': 'day_low_bid_time',
            'Open Time': 'open_time',
            'Last trade time': 'last_trade_time',
            'Close Time': 'close_time',
            'Day high Time': 'day_high_time',
            'Day low Time': 'day_low_time',
            'Bid time': 'bid_time',
            'Auction Time': 'auction_time'
        }, inplace=True)

        # Print the columns after renaming
        print(f"Columns in DataFrame after renaming: {df.columns.tolist()}")

        # Validate DataFrame (e.g., check for empty DataFrame)
        if df.empty:
            print(f"No data found in {file_path}. Skipping this file.")
            return
        
        # Check for required columns before insertion
        required_columns = ['id', 'sectype', 'date', 'time', 'ask']
        if not all(col in df.columns for col in required_columns):
            print(f"Missing required columns in {file_path}. Skipping this file.")
            return

        # Insert data into PostgreSQL
        df.to_sql('trading_data', con=engine, if_exists='append', index=False)
        print(f"Data from {file_path} loaded successfully.")

    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")

# Step 3: Load all CSV files
for i in range(1, 2):  # Adjust range as necessary
    print(f"Loading data from data{i}.csv...")
    file_path = f'data{i}.csv'
    load_data_to_db(file_path)

# Step 4: Close the engine
engine.dispose()
