from fastapi import HTTPException
from database import get_db_connection
import sqlite3

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
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()
