from fastapi import FastAPI, Query, HTTPException
import logging
from database import get_db_connection

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI()

@app.get("/chargers")
async def get_chargers(organizationalUnitCode: str = Query(..., description="The organizational unit code to filter chargers")):
    """
    Fetch chargers based on the provided organizational unit code.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Log the query for debugging
        logger.info(f"Executing query with organizationalUnitCode: {organizationalUnitCode}")

        # Example query (replace with your actual query)
        query = "SELECT TOP 10 * FROM chargepointStatus WHERE organizationalUnitCode = ?"
        cursor.execute(query, organizationalUnitCode)
        
        # Fetch results
        rows = cursor.fetchall()

        if rows:
            chargers = [{"ID": row[0], "chargepointID": row[1], "name": row[2]} for row in rows]
        else:
            chargers = []

        cursor.close()
        conn.close()

        return {"chargers": chargers}

    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")
