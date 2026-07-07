import os
import joblib
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import forecast

# Global variable to hold the model
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model_path = os.getenv("MODEL_PATH", "/app/models/forecast_model.pkl")
    
    # Check local path for development if not in Docker
    if not os.path.exists(model_path):
        model_path = os.path.join(os.path.dirname(__file__), "../../models/forecast_model.pkl")
        
    try:
        model = joblib.load(model_path)
        print(f"Loaded pretrained model from {model_path}")
        # Attach the model to the app state so routes can access it
        app.state.model = model
    except Exception as e:
        print(f"Warning: Could not load model from {model_path}: {e}")
        app.state.model = None

    yield
    # Clean up on shutdown
    model = None

app = FastAPI(
    title="Stateless Sales Forecasting API",
    description="Loads a pretrained model to perform sales forecasting.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(forecast.router, prefix="/api")
