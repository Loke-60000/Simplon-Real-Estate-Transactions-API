from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException
import uvicorn

from endpoints.average_revenue import average_revenue
from endpoints.transactions import get_transactions
from endpoints.transaction_count import transaction_count
from endpoints.count_small_apartments import count_small_apartments
from endpoints.piece_counts import piece_counts
from endpoints.average_price_per_square_meter import average_price_per_square_meter
from endpoints.sales_by_department import sales_by_department
from endpoints.transactions_in_high_income_cities import transactions_in_high_income_cities

app = FastAPI(title="Real Estate Transactions API")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    try:
        with open("static/index.html", 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="index.html not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

app.get("/average-revenue/{year}")(average_revenue)
app.get("/transactions")(get_transactions)
app.get("/transaction-count/{year}")(transaction_count)
app.get("/count-small-apartments")(count_small_apartments)
app.get("/piece-counts")(piece_counts)
app.get("/average-price-per-square-meter")(average_price_per_square_meter)
app.get("/sales-by-department")(sales_by_department)
app.get("/transactions-in-high-income-cities")(transactions_in_high_income_cities)

# Main function to run the app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)