from fastapi import HTTPException, Query
from database import get_db_connection
from database import handle_sql_error

async def get_transactions(cities: str = Query(None, description="Comma-separated list of cities, use % for wildcard"), limit: int = 10):
    if cities is None:
        raise HTTPException(status_code=400, detail="Cities parameter is required")

    conn = get_db_connection()
    city_list = [f"%{city.upper()}%" for city in cities.split(',')]
    placeholders = ','.join(['?'] * len(city_list))
    try:
        for city in city_list:
            city_check = conn.execute("SELECT COUNT(*) FROM transactions_sample WHERE UPPER(ville) LIKE ?", (city,)).fetchone()
            if city_check[0] == 0:
                raise HTTPException(status_code=404, detail=f"City {city.strip('%').capitalize()} not found in database")
        
        query = f"""
            SELECT ville, id_transaction, date_transaction, prix
            FROM transactions_sample ts
            WHERE UPPER(ville) LIKE ({placeholders})
            ORDER BY ville ASC
            LIMIT ?
        """
        result = conn.execute(query, city_list + [limit]).fetchall()
        if not result:
            raise HTTPException(status_code=404, detail="No transactions found")
        return {"transactions": [dict(row) for row in result]}
    except Exception as e:
        raise handle_sql_error(e, "Database error in transactions")
    finally:
        conn.close()
