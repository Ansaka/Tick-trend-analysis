from dotenv import load_dotenv
from google.cloud.sql.connector import Connector
import pg8000.native as pg8000
import os

# Initialize the Cloud SQL Python Connector
connector = Connector()

load_dotenv()

# Read the environment variables
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("AUTH_JSON")
instance = os.getenv("INSTANCE")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Function to create a connection
def get_connection():
    return connector.connect(
        instance,
        "pg8000",
        user=username,
        password=password,
        db=db_name
    )

# Test the database connection with a query
if __name__ == "__main__":
    try:
        # Get the connection
        connection = get_connection()
        cursor = connection.cursor()

        # Execute a simple query
        cursor.execute("SELECT version();")

        # Fetch and print the result
        version = cursor.fetchone()
        print("PostgreSQL version:", version)

        # Close the connection
        cursor.close()
        connection.close()
        print("Database connection test successful!")
    except Exception as e:
        print("Error connecting to the database:", e)
    finally:
        connector.close()
