import os
import joblib
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import forecast

# Global variable to hold the model
model = None

def load_keras_model():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    models_dir = os.path.join(root_dir, "models")
    
    config_path = os.path.join(root_dir, "config.json")
    if not os.path.exists(config_path):
        config_path = os.path.join(models_dir, "config.json")
        
    weights_path = os.path.join(root_dir, "model.weights.h5")
    if not os.path.exists(weights_path):
        weights_path = os.path.join(models_dir, "model.weights.h5")
        
    if not os.path.exists(config_path) or not os.path.exists(weights_path):
        raise FileNotFoundError(f"Model files not found. Config: {config_path}, Weights: {weights_path}")
        
    import keras
    import json
    
    with open(config_path, "r") as f:
        model_config = json.load(f)
        
    model = keras.models.model_from_json(json.dumps(model_config))
    model.load_weights(weights_path)
    return model

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    
    try:
        # Try loading Keras LSTM model
        model = load_keras_model()
        print("Loaded pretrained Keras LSTM model successfully!")
        app.state.model = model
    except Exception as e:
        print(f"Warning: Could not load Keras LSTM model: {e}")
        print("Attempting to load fallback joblib model...")
        try:
            model_path = os.getenv("MODEL_PATH", "/app/models/forecast_model.pkl")
            if not os.path.exists(model_path):
                model_path = os.path.join(os.path.dirname(__file__), "../../models/forecast_model.pkl")
            if os.path.exists(model_path):
                model = joblib.load(model_path)
                print(f"Loaded fallback pretrained model from {model_path}")
                app.state.model = model
            else:
                app.state.model = None
        except Exception as ex:
            print(f"Error loading fallback model: {ex}")
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
