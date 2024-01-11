import sqlite3
from fastapi import HTTPException
import logging

def get_db_connection():
    try:
        conn = sqlite3.connect('Chinook.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

logging.basicConfig(level=logging.ERROR, filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

def handle_sql_error(e: Exception, detail_message: str, status_code: int = 500):
    logging.error(f"SQL Error: {str(e)}")
    # Check if the exception is an instance of sqlite3.Error
    if isinstance(e, sqlite3.Error):
        # Return an HTTPException with the provided details
        return HTTPException(status_code=status_code, detail=f"{detail_message}: {str(e)}")
    else:
        # Handle non-sqlite3 errors differently if needed
        return HTTPException(status_code=status_code, detail=f"{detail_message}: Unexpected error")
