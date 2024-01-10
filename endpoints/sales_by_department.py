from fastapi import HTTPException
from database import get_db_connection
import sqlite3

async def sales_by_department():
    query = """
    SELECT departement, COUNT(*) as ventes
    FROM transactions_sample
    GROUP BY departement
    ORDER BY ventes DESC;
    """
    
    conn = get_db_connection()
    try:
        result = conn.execute(query).fetchall()
        if not result:
            raise HTTPException(status_code=404, detail="No data found")
        return {"sales_by_department": [dict(row) for row in result]}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()
