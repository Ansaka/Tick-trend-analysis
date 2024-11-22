import asyncio
import sys
import os
from dotenv import load_dotenv
from google.cloud.sql.connector import Connector
import pg8000.native as pg8000

# Set different event loop policy for Windows
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load environment variables first
load_dotenv()

# Get the absolute path to the credentials file
current_dir = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(current_dir, os.getenv("AUTH_JSON").lstrip('./'))

# Verify the file exists
if not os.path.exists(credentials_path):
    raise FileNotFoundError(f"Credentials file not found at: {credentials_path}")

# Set the credentials environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Initialize the Cloud SQL Python Connector
connector = Connector()

# Read the environment variables
instance = os.getenv("INSTANCE")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

async def main():
    connection = None
    try:
        # Get the connection
        connection = connector.connect(
            instance,
            "pg8000",
            user=username,
            password=password,
            db=db_name
        )
        cursor = connection.cursor()

        # Execute a simple query
        cursor.execute("SELECT version();")

        # Fetch and print the result
        version = cursor.fetchone()
        print("PostgreSQL version:", version)

        # Close the cursor
        cursor.close()
        print("Database connection test successful!")
    except Exception as e:
        print("Error connecting to the database:", e)
    finally:
        if connection:
            try:
                connection.close()
            except Exception as e:
                print(f"Error closing connection: {e}")
        connector.close()

if __name__ == "__main__":
    asyncio.run(main())
