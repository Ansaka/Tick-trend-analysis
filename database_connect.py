import asyncio
import sys
import os
from dotenv import load_dotenv
from google.cloud.sql.connector import Connector
from google.oauth2 import service_account
import pg8000.native as pg8000
import json

# Set different event loop policy for Windows
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load environment variables first
load_dotenv()

# Get the Google service account key from the environment variable
google_service_account_key = os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY")

# Set the credentials environment variable directly
if google_service_account_key:
    service_account_info = json.loads(google_service_account_key)
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_service_account_key

# Initialize the Cloud SQL Python Connector
connector = Connector(credentials=credentials)

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
