# Real Estate Transactions API Documentation

## Overview

This API provides access to real estate transaction data, allowing users to query various aspects such as average revenue, transaction counts, and specific data related to smaller apartments across different cities and years.

## Endpoints

### 1. Average Revenue
- **URL**: `/average-revenue/{year}`
- **Method**: `GET`
- **URL Params**: 
  - `city=[string]` (required)
  - `year=[integer]` (required in URL)
- **Success Response**: JSON object with average revenue.
- **Error Response**: 
  - 400 Bad Request if year parameter is missing/invalid
  - 404 Not Found if no data is available
  - 500 Internal Server Error for other issues
- **Example**: `http://localhost:8000/average-revenue/2020?city=Montpellier`

### 2. Transactions
- **URL**: `/transactions`
- **Method**: `GET`
- **Query Params**: 
  - `cities=[string]` (required, comma-separated list)
  - `limit=[integer]` (optional, default is 10)
- **Success Response**: JSON object with a list of transactions.
- **Error Response**: 
  - 400 Bad Request if cities parameter is missing
  - 404 Not Found if no transactions are found
  - 500 Internal Server Error for other issues
- **Example**: `http://localhost:8000/transactions?cities=paris&limit=5`

### 3. Transaction Count
- **URL**: `/transaction-count/{year}`
- **Method**: `GET`
- **URL Params**: 
  - `city=[string]` (required)
  - `year=[integer]` (required in URL)
- **Success Response**: JSON object with transaction count.
- **Error Response**: 
  - 400 Bad Request if year is invalid
  - 404 Not Found if no data is found
  - 500 Internal Server Error for other issues
- **Example**: `http://localhost:8000/transaction-count/2023?city=Paris`

### 4. Small Apartment Transaction Count
- **URL**: `/small-apartment-transaction-count`
- **Method**: `GET`
- **Query Params**: 
  - `city=[string]` (required)
  - `year=[integer]` (required)
- **Success Response**: JSON object with small apartment transaction count.
- **Error Response**: 
  - 400 Bad Request if year is invalid
  - 404 Not Found if no data is found
  - 500 Internal Server Error for other issues
- **Example**: `http://localhost:8000/small-apartment-transaction-count?city=Marseille&year=2021`

### 5. Count Small Apartments
- **URL**: `/count-small-apartments`
- **Method**: `GET`
- **Query Params**: 
  - `city=[string]` (required)
  - `year=[integer]` (required)
- **Success Response**: JSON object with small apartment count.
- **Error Response**: 
  - 400 Bad Request if year is invalid
  - 404 Not Found if no data is found
  - 500 Internal Server Error for other issues
- **Example**: `http://localhost:8000/count-small-apartments?city=Lyon&year=2023`

### 6. Property Piece Counts
- **URL**: `/piece-counts`
- **Method**: `GET`
- **No Query Params**
- **Success Response**: JSON object with the count of properties (apartments and houses) grouped by the number of pieces (rooms).
- **Error Response**: 
  - 404 Not Found if no data is found
  - 500 Internal Server Error for database-related issues
- **Example**: `http://localhost:8000/piece-counts`

### 7. Average Price Per Square Meter
- **URL**: `/average-price-per-square-meter`
- **Method**: `GET`
- **Query Params**: 
  - `city=[string]` (required)
  - `year=[integer]` (required)
  - `building_type=[string]` (required, e.g., 'Maison', 'Appartement')
- **Success Response**: JSON object with the price, habitable surface, and average price per square meter.
- **Error Response**: 
  - 400 Bad Request if year is invalid or parameters are missing
  - 404 Not Found if no data is found
  - 500 Internal Server Error for database-related issues
- **Example**: `http://localhost:8000/average-price-per-square-meter?city=Avignon&year=2022&building_type=Maison`


## How to Run

- Ensure FastAPI and Uvicorn are installed.
- Run the server using `uvicorn main:app --reload`, assuming the script is named `main.py`.
- Access the API at `http://localhost:8000`.

## Notes

- The database sample used is `Chinook.db`.
- Comprehensive error handling is implemented.
- The API is flexible for different cities and years.
