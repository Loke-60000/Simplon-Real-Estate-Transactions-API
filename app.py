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



# Main function to run the app (not required)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

'''
http://localhost:8000/average-revenue/2020?city=Montpellier
http://localhost:8000/transactions?cities=paris&limit=5
http://localhost:8000/transaction-count/2023?city=Paris
http://localhost:8000/small-apartment-transaction-count?city=Marseille&year=2021
http://localhost:8000/count-small-apartments?city=Lyon&year=2023
'''
