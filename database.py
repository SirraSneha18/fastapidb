import os
import pyodbc
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    # Retrieve connection details from environment variables
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_DATABASE")
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    driver = os.getenv("DB_DRIVER")

    # Create a connection string
    connection_string = f'DRIVER={driver};SERVER={server},{os.getenv("DB_PORT")};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=yes;Timeout=60'

    try:
        # Log the attempt to connect
        logger.info("Attempting to connect to the database...")

        # Establish the connection
        conn = pyodbc.connect(connection_string)

        # Log success
        logger.info("Successfully connected to the database.")
        return conn
    except Exception as e:
        # Log any connection error
        logger.error(f"Failed to connect to the database: {e}")
        raise
