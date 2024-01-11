from fastapi import HTTPException
from database import get_db_connection
import sqlite3
from database import handle_sql_error

async def transactions_in_high_income_cities(city: str = None, year: str = "2018", minimum_income: int = 10000):
    # Validate the year
    try:
        year = int(year)
        if year < 1000 or year > 9999:
            raise ValueError("Year must be a four-digit number.")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid year format. Year must be a four-digit number.")

    year_pattern = f"{year}%"

    query = """
    SELECT tr.ville, COUNT(*) as transaction_count
    FROM transactions_sample tr
    INNER JOIN foyers_fiscaux ff ON UPPER(tr.ville) LIKE UPPER(ff.ville)
    WHERE ff.revenu_fiscal_moyen > ?
    AND ff.date = ?
    AND tr.date_transaction LIKE '2022%'
    """

    if city:
        city_pattern = f"%{city.upper()}%"
        query += " AND UPPER(tr.ville) LIKE ? "
        query_params = (minimum_income, year, city_pattern)
    else:
        query_params = (minimum_income, year)

    query += " GROUP BY tr.ville;"

    conn = get_db_connection()
    try:
        result = conn.execute(query, query_params).fetchall()
        if not result:
            raise HTTPException(status_code=404, detail="No data found")
        return {"transactions_in_high_income_cities": [dict(row) for row in result]}
    except Exception as e:
        raise handle_sql_error(e, "Database error in transactions_in_high_income_cities")
    finally:
        conn.close()
