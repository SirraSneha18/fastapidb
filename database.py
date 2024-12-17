import pyodbc
import logging
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging to output to stdout (which Azure captures)
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_db_connection():
    # Fetch environment variables
    server = 'mydatabase-server.database.windows.net'  # Azure SQL server name
    database ='MyDatabase'
    username ='sneha123 '# Username
    password ='sneha@18'  # Password
    driver = '{ODBC Driver 18 for SQL Server}' # Driver for SQL Server

    # Log environment variables for debugging (do not log sensitive data like passwords in production)
    logger.debug(f"DB_SERVER: {server}, DB_DATABASE: {database}, DB_USERNAME: {username}, DB_DRIVER: {driver}")
    
    if not server or not database or not username or not password or not driver:
        logger.error("Missing one or more required environment variables.")
        raise ValueError("Missing one or more required environment variables.")
    
    # Remove curly braces around the driver if present
    driver = driver.strip('{}')

    # Create the connection string
    connection_string = f'DRIVER={{{driver}}};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'

    try:
        # Log the attempt to connect
        logger.info("Attempting to connect to the database...")

        # Establish the connection
        conn = pyodbc.connect(connection_string)

        # Log success
        logger.info("Successfully connected to the database.")

        return conn
    except pyodbc.Error as e:
        # Log any connection error
        logger.error(f"Failed to connect to the database: {e}")
        raise Exception("Database connection failed") from e
