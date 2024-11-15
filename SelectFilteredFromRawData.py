import pandas as pd
from tqdm import tqdm

# Define the file path
file_path = 'debs2022-gc-trading-day-12-11-21.csv'
target_symbol = '120071.ETR'

# Initialize counters
total_rows_processed = 0
matching_rows_found = 0

# Define columns (keeping your existing columns list)
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
chunk_size = 100000
found_rows = []

# Calculate total lines for progress bar
print("Calculating total lines...")
with open(file_path) as f:
    total_lines = sum(1 for line in f) - 13

print(f"Total lines to process: {total_lines:,}")

try:
    # Create a progress bar for the chunks
    for chunk in tqdm(pd.read_csv(file_path, 
                                chunksize=chunk_size, 
                                skiprows=13,
                                names=columns,
                                low_memory=False),
                    total=total_lines // chunk_size + 1,
                    desc="Processing chunks"):
        
        # Update total rows processed
        chunk_size = chunk.shape[0]
        total_rows_processed += chunk_size
        
        # Filter rows for the target symbol
        filtered_rows = chunk[chunk['symbol'] == target_symbol]
        
        # If any rows match, append them
        if not filtered_rows.empty:
            found_rows.append(filtered_rows)
            matching_rows_found += filtered_rows.shape[0]
        
        # Calculate memory usage
        memory_usage = sum(df.memory_usage(deep=True).sum() for df in found_rows) / (1024 * 1024)
        
        # Print progress statistics every chunk
        print(f"\rProcessed: {total_rows_processed:,} rows | "
              f"Found: {matching_rows_found:,} matches | "
              f"Match rate: {(matching_rows_found/total_rows_processed)*100:.2f}% | "
              f"Memory used: {memory_usage:.2f} MB", 
              end="")

    # Final results
    if found_rows:
        result_df = pd.concat(found_rows, ignore_index=True)
        print(f"\n\nFinal Results:")
        print(f"Total rows processed: {total_rows_processed:,}")
        print(f"Total matches found: {len(result_df):,}")
        print(f"Overall match rate: {(len(result_df)/total_rows_processed)*100:.2f}%")
        
        # Save to a new CSV file
        output_file = f'{target_symbol}_data.csv'
        result_df.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")
    else:
        print(f"\n\nNo rows found for symbol {target_symbol} after processing {total_rows_processed:,} rows")

except Exception as e:
    print(f"\nError occurred: {str(e)}")
