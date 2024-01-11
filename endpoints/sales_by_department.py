from fastapi import HTTPException
from database import get_db_connection
from database import handle_sql_error
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
    except Exception as e:
        raise handle_sql_error(e, "Database error in sales_by_department")
    finally:
        conn.close()
