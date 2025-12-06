from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="StockVision API", description="Backend for StockVision Desktop Application")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for local desktop app usage
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers import stock, predictions

app.include_router(stock.router)
app.include_router(predictions.router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "StockVision Backend is running"}
