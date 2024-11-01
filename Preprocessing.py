import pandas as pd
from sqlalchemy import create_engine

# Step 1: Set up the database connection
db_user = 'my_user'
db_password = 'my_password'
db_host = 'localhost'  # or your database host
db_port = '5432'       # default PostgreSQL port
db_name = 'GoldenCross'

columns = [
    "symbol",
    "sectype",
    "date",
    "time",
    "Ask",
    "Ask volume",
    "Bid",
    "Bid volume",
    "Ask time",
    "Day's high ask",
    "Close",
    "Currency",
    "Day's high ask time",
    "Day's high",
    "ISIN",
    "Auction price",
    "Day's low ask",
    "Day's low",
    "Day's low ask time",
    "Open",
    "last",
    "last_last",
    "Last volume",
    "Trading time",
    "Total volume",
    "Mid price",
    "Trading date",
    "Profit",
    "Current price",
    "Related indices",
    "Day high bid time",
    "Day low bid time",
    "Open Time",
    "Last trade time",
    "Close Time",
    "Day high Time",
    "Day low Time",
    "Bid time",
    "Auction Time",
    "temp"
]


# Create a database engine
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Step 2: Define a function to read and process CSV files
def load_data_to_db(file_path):
    try:
        # Read the CSV file
        df = pd.read_csv('debs2022-gc-trading-day-12-11-21.csv', header=None, skiprows=13, low_memory=False)
        
        # Manually set column names
        df.columns = columns
        print(df.head()) 

        # Print the initial columns for debugging
        print(f"Columns in DataFrame before stripping: {df.columns.tolist()}")

        # Select relevant columns
        df_formatted = df[["symbol", 'sectype', 'date', 'time', 'last']]
        df_formatted = df_formatted[df_formatted['last'].notna()]
        print(df_formatted.head())

        # Print the columns after renaming
        print(f"Columns in DataFrame after renaming: {df_formatted.columns.tolist()}")

        # Convert date format from DD-MM-YYYY to YYYY-MM-DD
        df_formatted['date'] = pd.to_datetime(df_formatted['date'], format='%d-%m-%Y', errors='coerce').dt.strftime('%Y-%m-%d')

        # Convert time format to HH:MM:SS
        df_formatted['time'] = pd.to_datetime(df_formatted['time'], format='%H:%M:%S.%f', errors='coerce').dt.strftime('%H:%M:%S.%f')

        # Validate DataFrame (e.g., check for empty DataFrame)
        if df_formatted.empty:
            print(f"No data found in {file_path}. Skipping this file.")
            return
        
        # Check for required columns before insertion
        required_columns = ['symbol', 'sectype', 'date', 'time', 'last']  # Update this to match the new column names
        if not all(col in df_formatted.columns for col in required_columns):
            print(f"Missing required columns in {file_path}. Skipping this file.")
            return

        # Insert data into PostgreSQL
        df_formatted.to_sql('trading_data', con=engine, if_exists='append', index=False)
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
