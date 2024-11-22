import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm
from datetime import datetime
import glob
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database credentials from environment variables
db_user = os.getenv('DB_USER')
db_password = quote_plus(os.getenv('DB_PASSWORD'))
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

columns = [
    "symbol", "sectype", "date", "time", "Ask", "Ask volume", "Bid", "Bid volume", 
    "Ask time", "Day's high ask", "Close", "Currency", "Day's high ask time", 
    "Day's high", "ISIN", "Auction price", "Day's low ask", "Day's low", 
    "Day's low ask time", "Open", "Nominal value", "last", "Last volume", "Trading time", 
    "Total volume", "Mid price", "Trading date", "Profit", "Current price", 
    "Related indices", "Day high bid time", "Day low bid time", "Open Time", 
    "Last trade time", "Close Time", "Day high Time", "Day low Time", "Bid time", 
    "Auction Time", "temp"
]

# Create a database engine
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Step 2: Define a function to read and process CSV files in chunks
def load_data_to_db(file_path, total_files, current_file, chunk_size=100000):
    try:
        # Initialize total row counter
        total_rows = 0

        # Calculate approximate total lines for the progress bar
        with open(file_path) as f:
            total_lines = sum(1 for line in f) - 13  # Adjust for skipped rows
        
        # Extract date from filename for progress reporting
        date_str = file_path.split('-')[-1].replace('.csv', '')
        
        # Read CSV in chunks with a progress bar
        chunk_iterator = pd.read_csv(file_path, header=None, skiprows=13, 
                                   low_memory=False, chunksize=chunk_size)
        
        progress_bar = tqdm(chunk_iterator,
                          total=total_lines // chunk_size + 1,
                          desc=f"Processing file {current_file}/{total_files} ({date_str})")
        
        for chunk in progress_bar:
            # Manually set column names for the current chunk
            chunk.columns = columns
            
            # Select and filter relevant columns
            df_formatted = chunk[["symbol", 'sectype', 'date', 'time', 'last']].dropna(subset=['last'])
            
            # Convert date format from DD-MM-YYYY to YYYY-MM-DD
            df_formatted['date'] = pd.to_datetime(df_formatted['date'], format='%d-%m-%Y', errors='coerce').dt.strftime('%Y-%m-%d')

            # Convert time format to HH:MM:SS
            df_formatted['time'] = pd.to_datetime(df_formatted['time'], format='%H:%M:%S.%f', errors='coerce').dt.strftime('%H:%M:%S.%f')

            # Insert the current chunk into the database
            df_formatted.to_sql('trading_data', con=engine, if_exists='append', index=False)

            # Update total rows processed
            total_rows += len(df_formatted)
            
            # Update progress bar description with detailed information
            progress_bar.set_postfix({'Rows': total_rows})

        print(f"\nCompleted {file_path}: Processed {total_rows:,} rows")
        return total_rows

    except Exception as e:
        print(f"\nError loading data from {file_path}: {e}")
        return 0

# Step 3: Load all CSV files
for i in range(1):  # Adjust range as necessary
    print(f"Loading data from data{i}.csv...")
    file_path = f'debs2022-gc-trading-day-12-11-21.csv'
    load_data_to_db(file_path)

# Step 4: Close the engine
engine.dispose()
