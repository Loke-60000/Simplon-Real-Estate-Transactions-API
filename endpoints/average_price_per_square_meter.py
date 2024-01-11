from fastapi import HTTPException
from database import get_db_connection
from database import handle_sql_error
from fuzzywuzzy import fuzz

async def average_price_per_square_meter(city: str, year: str, building_type: str):
    # Define the valid building types available in the database
    valid_building_types = ['APPARTEMENT', 'MAISON']
    
    if not year.isdigit() or len(year) != 4:
        raise HTTPException(status_code=400, detail="Year must be a valid 4-digit number")

    # Find the most similar building type from the valid ones
    most_similar_building_type = max(valid_building_types, key=lambda x: fuzz.ratio(building_type.upper(), x))

    year_pattern = f"{year}%"
    city_name = city.upper()
    
    conn = get_db_connection()
    try:
        result = conn.execute("SELECT prix, surface_habitable, AVG(ROUND(prix/surface_habitable)) as prix2 FROM transactions_sample ts WHERE UPPER(ville) = ? AND date_transaction LIKE ? AND UPPER(type_batiment) = ?", (city_name, year_pattern, most_similar_building_type)).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail=f"No data found for city {city}, year {year}, and building type {building_type}")
        
        if result['prix'] is None or result['surface_habitable'] is None or result['prix2'] is None:
            raise HTTPException(status_code=404, detail=f"No data found for city {city}, year {year}, and building type {building_type}")

        return {"prix": result['prix'], "surface_habitable": result['surface_habitable'], "average_price_per_square_meter": result['prix2']}
    except Exception as e:
        raise handle_sql_error(e, "Database error in average_price_per_square_meter")
    finally:
        conn.close()
