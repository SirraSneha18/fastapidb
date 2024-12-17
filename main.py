from fastapi import FastAPI, Query, HTTPException
import pyodbc
from database import get_db_connection
import traceback
import logging


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

def get_user_organizational_unit_code() -> str:
    # This is the hardcoded default organizational unit code
    return "0000-0010"

@app.get("/chargers")
async def get_chargers(organizationalUnitCode: str = Query(..., description="The organizational unit code to filter chargers")):
    """
    Fetch chargers based on the provided organizational unit code.
    """
    try:
        if not organizationalUnitCode:
            raise HTTPException(status_code=400, detail="No organizationalUnitCode provided.")

        # Log the received organizational unit code
        logger.info(f"Received organizationalUnitCode: {organizationalUnitCode}")

        # Establish the connection to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Log the query being executed
        logger.info(f"Executing query for organizationalUnitCode: {organizationalUnitCode}")

        # Query chargers based on the organizational unit code
        cursor.execute("""
            SELECT * 
            FROM [dbo].[chargepointStatus1]
            WHERE organizationalUnitCode = ?
        """, organizationalUnitCode)

        # Fetch all rows from the query result
        rows = cursor.fetchall()

        # Log the number of results found
        logger.info(f"Query returned {len(rows)} results for organizationalUnitCode: {organizationalUnitCode}")

        # If no rows are returned, raise a 404 exception
        if not rows:
            logger.warning(f"No chargers found for the provided organizational unit code: {organizationalUnitCode}")
            return {"detail": "No chargers found for the provided organizational unit code."}

        # Format the result
        chargers = [{
            "ID": row[0],
            "chargepointID": row[1],
            "name": row[2],
            "connector": row[3],
            "location": row[4],
            "status": row[5],
            "statusError": row[6],
            "statusTime": row[7],
            "networkStatus": row[8],
            "networkStatusTime": row[9],
            "mailContactOffline": row[10],
            "mailContactStatus": row[11],
            "mailContactOfflineLate": row[12],
            "organizationalUnitCode": row[13],
            "organizationalUnitName": row[14],
        } for row in rows]

        # Log the result
        logger.info(f"Returning {len(chargers)} chargers for organizationalUnitCode: {organizationalUnitCode}")

        # Close the cursor and the connection
        cursor.close()
        conn.close()

        return {"chargers": chargers}

    except HTTPException as http_err:
        # Log HTTP-specific errors
        logger.error(f"HTTP error occurred: {http_err.detail}")
        return {"detail": http_err.detail}

    except Exception as e:
        # Log the exception for debugging
        logger.error(f"Error: {e}")
        logger.error(traceback.format_exc())
        return {"detail": "Internal Server Error", "error": str(e)}
