from fastapi import HTTPException
from database import get_db_connection
import sqlite3

async def count_small_apartments(city: str, year: str):
    if not year.isdigit() or len(year) != 4:
        raise HTTPException(status_code=400, detail="Year must be a valid 4-digit number")
    
    year_pattern = f"{year}%"
    city_pattern = f"%{city.upper()}%"

    conn = get_db_connection()
    try:
        result = conn.execute("SELECT COUNT(*) FROM transactions_sample WHERE ville LIKE ? AND date_transaction LIKE ? AND n_pieces < 2", (city_pattern, year_pattern)).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail=f"No data found for city {city} in year {year}")
        return {"small_apartment_count": result[0]}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()
