# Real Estate Transactions API Documentation

***

# Table of Contents
1. [Overview](#overview)
2. [Endpoints](#endpoints)
   - [1. Average Revenue](#1-average-revenue)
   - [2. Transactions](#2-transactions)
   - [3. Transaction Count](#3-transaction-count)
   - [4. Small Apartment Transaction Count](#4-small-apartment-transaction-count)
   - [5. Count Small Apartments](#5-count-small-apartments)
   - [6. Property Piece Counts](#6-property-piece-counts)
   - [7. Average Price Per Square Meter](#7-average-price-per-square-meter)
   - [8. Sales by Department](#8-sales-by-department)
   - [9. Transactions in High-Income Cities](#9-transactions-in-high-income-cities)
3. [How to Run](#how-to-run)
4. [Notes](#notes)

***

## Overview

This API provides access to real estate transaction data, allowing users to query various aspects such as average revenue, transaction counts, and specific data related to smaller apartments across different cities and years.

***

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

### 8. Sales by Department
- **URL**: `/sales-by-department`
- **Method**: `GET`
- **No Query Params**
- **Success Response**: JSON object listing each department with its corresponding number of sales, ordered by the number of sales in descending order.
- **Error Response**: 
  - 404 Not Found if no data is found
  - 500 Internal Server Error for database-related issues
- **Example**: `http://localhost:8000/sales-by-department`

### 9. Transactions in High-Income Cities
- **URL**: `/transactions-in-high-income-cities`
- **Method**: `GET`
- **Query Params**: 
  - `city=[string]` (optional)
  - `minimum_income=[integer]` (optional, default is 10000)
- **Success Response**: JSON object listing each city with its corresponding number of real estate transactions in 2022, where the average fiscal revenue in 2018 was above the specified minimum income.
- **Error Response**: 
  - 404 Not Found if no data is found
  - 500 Internal Server Error for database-related issues
- **Example**: `http://localhost:8000/transactions-in-high-income-cities?city=Paris&minimum_income=15000`

***

## How to Run

- Ensure FastAPI and Uvicorn are installed.
- Run the server using `uvicorn main:app --reload`, assuming the script is named `main.py`.
- Access the API at `http://localhost:8000`.

***

## Notes

- The database sample used is `Chinook.db`.
- Comprehensive error handling is implemented.
- The API is flexible for different cities and years.
