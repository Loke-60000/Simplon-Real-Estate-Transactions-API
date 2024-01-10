from fastapi import HTTPException
from database import get_db_connection
import sqlite3

async def average_price_per_square_meter(city: str, year: str, building_type: str):
    if not year.isdigit() or len(year) != 4:
        raise HTTPException(status_code=400, detail="Year must be a valid 4-digit number")

    year_pattern = f"{year}%"
    city_name = city.upper()
    building_type_upper = building_type.upper()

    conn = get_db_connection()
    try:
        result = conn.execute("SELECT prix, surface_habitable, AVG(ROUND(prix/surface_habitable)) as prix_per_sqm FROM transactions_sample ts WHERE UPPER(ville) = ? AND date_transaction LIKE ? AND UPPER(type_batiment) = ?", (city_name, year_pattern, building_type_upper)).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail=f"No data found for city {city}, year {year}, and building type {building_type}")
        
        # Check if the retrieved values are null
        if result['prix'] is None or result['surface_habitable'] is None or result['prix_per_sqm'] is None:
            raise HTTPException(status_code=404, detail=f"No data found for city {city}, year {year}, and building type {building_type}")

        return {"prix": result['prix'], "surface_habitable": result['surface_habitable'], "average_price_per_square_meter": result['prix_per_sqm']}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()