from fastapi import FastAPI, HTTPException, Query
import sqlite3
import uvicorn

app = FastAPI()

# Database Connection
def get_db_connection():
    try:
        conn = sqlite3.connect('Chinook.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
        
conn = get_db_connection()

@app.get("/average-revenue/{year}")
async def average_revenue(city: str, year: str = None):
    if year is None:
        raise HTTPException(status_code=400, detail="Year parameter is required")
    if not year.isdigit() or len(year) != 4:
        raise HTTPException(status_code=400, detail="Year must be a valid 4-digit number")

    year_int = int(year)
    try:
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
    except HTTPException as e:
        raise e
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/transactions")
async def get_transactions(cities: str = Query(None, description="Comma-separated list of cities, use % for wildcard"), limit: int = 10):
    if cities is None:
        raise HTTPException(status_code=400, detail="Cities parameter is required")

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
    finally:
        conn.close()

@app.get("/transaction-count/{year}")
async def transaction_count(city: str, year: str):
    if not year.isdigit() or len(year) != 4:
        raise HTTPException(status_code=400, detail="Year must be a valid 4-digit number")

    year_pattern = f"{year}%"
    city_pattern = f"%{city.upper()}%"

    try:
        try:
            result = conn.execute("SELECT COUNT(id_transaction) FROM transactions_sample WHERE UPPER(ville) LIKE ? AND date_transaction LIKE ?", (city_pattern, year_pattern)).fetchone()
            if result is None:
                raise HTTPException(status_code=404, detail=f"No data found for city {city} in year {year}")
            return {"transaction_count": result[0]}
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        finally:
            conn.close()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/count-small-apartments")
async def count_small_apartments(city: str, year: str):
    if not year.isdigit() or len(year) != 4:
        raise HTTPException(status_code=400, detail="Year must be a valid 4-digit number")
    year_pattern = f"{year}%"
    city_pattern = f"%{city.upper()}%"
    try:
        result = conn.execute("SELECT COUNT(*) FROM transactions_sample WHERE ville LIKE ? AND date_transaction LIKE ? AND n_pieces < 2", (city_pattern, year_pattern)).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail=f"No data found for city {city} in year {year}")
        return {"small_apartment_count": result[0]}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/piece-counts")
async def piece_counts():
    query = """
    SELECT n_pieces, COUNT(*) as count
    FROM transactions_sample
    WHERE type_batiment LIKE 'Appartement' OR type_batiment LIKE 'Maison'
    GROUP BY n_pieces
    ORDER BY n_pieces;
    """
    try:
        result = conn.execute(query).fetchall()
        if not result:
            raise HTTPException(status_code=404, detail="No data found")
        return {"piece_counts": [dict(row) for row in result]}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/average-price-per-square-meter")
async def average_price_per_square_meter(city: str, year: str, building_type: str):
    if not year.isdigit() or len(year) != 4:
        raise HTTPException(status_code=400, detail="Year must be a valid 4-digit number")

    year_pattern = f"{year}%"
    city_name = city.upper()
    building_type_upper = building_type.upper()

    try:
        result = conn.execute("SELECT prix, surface_habitable, AVG(ROUND(prix/surface_habitable)) as prix_per_sqm FROM transactions_sample ts WHERE UPPER(ville) = ? AND date_transaction LIKE ? AND UPPER(type_batiment) = ?", (city_name, year_pattern, building_type_upper)).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail=f"No data found for city {city}, year {year}, and building type {building_type}")
        return {"prix": result['prix'], "surface_habitable": result['surface_habitable'], "average_price_per_square_meter": result['prix_per_sqm']}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/sales-by-department")
async def sales_by_department():
    query = """
    SELECT departement, COUNT(*) as ventes
    FROM transactions_sample
    GROUP BY departement
    ORDER BY ventes DESC;
    """
    try:
        result = conn.execute(query).fetchall()
        if not result:
            raise HTTPException(status_code=404, detail="No data found")
        return {"sales_by_department": [dict(row) for row in result]}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/transactions-in-high-income-cities")
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
    try:
        result = conn.execute(query).fetchall()
        if not result:
            raise HTTPException(status_code=404, detail="No data found")
        return {"transactions_in_high_income_cities": [dict(row) for row in result]}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Main function to run the app (not required)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
