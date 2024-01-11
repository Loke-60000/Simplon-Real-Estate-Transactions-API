from fastapi import HTTPException
from database import get_db_connection
import sqlite3
from database import handle_sql_error

async def piece_counts():
    query = """
    SELECT n_pieces, COUNT(*) as count
    FROM transactions_sample
    WHERE type_batiment LIKE 'Appartement' OR type_batiment LIKE 'Maison'
    GROUP BY n_pieces
    ORDER BY n_pieces;
    """
    
    conn = get_db_connection()
    try:
        result = conn.execute(query).fetchall()
        if not result:
            raise HTTPException(status_code=404, detail="No data found")
        return {"piece_counts": [dict(row) for row in result]}
    except Exception as e:
        raise handle_sql_error(e, "Database error in piece_counts")
    finally:
        conn.close()
