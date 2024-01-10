from fastapi import HTTPException
from database import get_db_connection

async def average_revenue(city: str, year: str = None):
    if year is None:
        raise HTTPException(status_code=400, detail="Year parameter is required")
    if not year.isdigit() or len(year) != 4:
        raise HTTPException(status_code=400, detail="Year must be a valid 4-digit number")

    year_int = int(year)
    conn = get_db_connection()
    try:
        city_upper = f"%{city.upper()}%"
        result = conn.execute("SELECT revenu_fiscal_moyen FROM foyers_fiscaux WHERE UPPER(ville) LIKE ? and date = ?", (city_upper, year_int)).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail=f"No data found for city {city} in year {year}")
        return {"revenu_fiscal_moyen": result['revenu_fiscal_moyen']}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()
