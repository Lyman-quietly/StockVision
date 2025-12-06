from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from routers import stock, predictions

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API for StockVision application."
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(stock.router)
app.include_router(predictions.router)

@app.get("/")
def read_root():
    """
    Root endpoint to verify backend status.
    """
    return {"status": "ok", "message": "StockVision Backend is running"}

