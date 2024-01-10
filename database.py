import sqlite3
from fastapi import HTTPException

def get_db_connection():
    try:
        conn = sqlite3.connect('Chinook.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
