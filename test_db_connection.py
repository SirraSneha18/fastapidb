import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database connection details from environment variables
server = os.getenv("DB_SERVER")
database = os.getenv("DB_DATABASE")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
driver = os.getenv("DB_DRIVER", '{ODBC Driver 17 for SQL Server}')

# Formulate the connection string with port 1433 and increased timeout
connection_string = f"DRIVER={driver};SERVER={server},{os.getenv('DB_PORT')};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=yes;Timeout=60"

try:
    # Attempt to connect
    conn = pyodbc.connect(connection_string)
    print("Successfully connected to the database!")
    conn.close()
except Exception as e:
    print(f"Failed to connect to the database: {e}")
