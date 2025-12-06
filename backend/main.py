from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
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
