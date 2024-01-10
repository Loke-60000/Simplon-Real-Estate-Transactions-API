from fastapi import HTTPException
from database import get_db_connection
import sqlite3

async def transactions_in_high_income_cities():
    query = """
    SELECT tr.ville, COUNT(*) as transaction_count
    FROM transactions_sample tr
    INNER JOIN foyers_fiscaux ff ON tr.ville = UPPER(ff.ville)
    WHERE ff.revenu_fiscal_moyen > 10000 
    AND ff.date = 2018 
    AND tr.date_transaction LIKE '2022%'
    GROUP BY tr.ville;
    """
    
    conn = get_db_connection()
    try:
        result = conn.execute(query).fetchall()
        if not result:
            raise HTTPException(status_code=404, detail="No data found")
        return {"transactions_in_high_income_cities": [dict(row) for row in result]}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()
