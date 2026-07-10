import os
import joblib
import numpy as np
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import forecast

# Global variable to hold the model
model = None

class NumPyLSTMModel:
    def __init__(self, weights_path):
        import h5py
        with h5py.File(weights_path, "r") as f:
            # First LSTM layer (lstm)
            self.lstm_w = f["layers/lstm/cell/vars/0"][:]
            self.lstm_u = f["layers/lstm/cell/vars/1"][:]
            self.lstm_b = f["layers/lstm/cell/vars/2"][:]
            
            # Second LSTM layer (lstm_1)
            self.lstm1_w = f["layers/lstm_1/cell/vars/0"][:]
            self.lstm1_u = f["layers/lstm_1/cell/vars/1"][:]
            self.lstm1_b = f["layers/lstm_1/cell/vars/2"][:]
            
            # First Dense layer (dense)
            self.dense_w = f["layers/dense/vars/0"][:]
            self.dense_b = f["layers/dense/vars/1"][:]
            
            # Second Dense layer (dense_1)
            self.dense1_w = f["layers/dense_1/vars/0"][:]
            self.dense1_b = f["layers/dense_1/vars/1"][:]

    def predict(self, X, verbose=0):
        batch_size, timesteps, features = X.shape
        
        # 1. First LSTM layer (return_sequences=True, 64 units)
        h_lstm = np.zeros((batch_size, timesteps, 64))
        h = np.zeros((batch_size, 64))
        c = np.zeros((batch_size, 64))
        
        w_i, w_f, w_c, w_o = np.split(self.lstm_w, 4, axis=1)
        u_i, u_f, u_c, u_o = np.split(self.lstm_u, 4, axis=1)
        b_i, b_f, b_c, b_o = np.split(self.lstm_b, 4)
        
        for t in range(timesteps):
            xt = X[:, t, :]
            
            i_gate = 1.0 / (1.0 + np.exp(-(np.dot(xt, w_i) + np.dot(h, u_i) + b_i)))
            f_gate = 1.0 / (1.0 + np.exp(-(np.dot(xt, w_f) + np.dot(h, u_f) + b_f)))
            c_cand = np.tanh(np.dot(xt, w_c) + np.dot(h, u_c) + b_c)
            c = f_gate * c + i_gate * c_cand
            o_gate = 1.0 / (1.0 + np.exp(-(np.dot(xt, w_o) + np.dot(h, u_o) + b_o)))
            h = o_gate * np.tanh(c)
            
            h_lstm[:, t, :] = h
            
        # 2. Second LSTM layer (return_sequences=False, 32 units)
        h1 = np.zeros((batch_size, 32))
        c1 = np.zeros((batch_size, 32))
        
        w1_i, w1_f, w1_c, w1_o = np.split(self.lstm1_w, 4, axis=1)
        u1_i, u1_f, u1_c, u1_o = np.split(self.lstm1_u, 4, axis=1)
        b1_i, b1_f, b1_c, b1_o = np.split(self.lstm1_b, 4)
        
        for t in range(timesteps):
            xt1 = h_lstm[:, t, :]
            
            i_gate1 = 1.0 / (1.0 + np.exp(-(np.dot(xt1, w1_i) + np.dot(h1, u1_i) + b1_i)))
            f_gate1 = 1.0 / (1.0 + np.exp(-(np.dot(xt1, w1_f) + np.dot(h1, u1_f) + b1_f)))
            c_cand1 = np.tanh(np.dot(xt1, w1_c) + np.dot(h1, u1_c) + b1_c)
            c1 = f_gate1 * c1 + i_gate1 * c_cand1
            o_gate1 = 1.0 / (1.0 + np.exp(-(np.dot(xt1, w1_o) + np.dot(h1, u1_o) + b1_o)))
            h1 = o_gate1 * np.tanh(c1)
            
        # 3. First Dense layer (relu)
        dense_out = np.dot(h1, self.dense_w) + self.dense_b
        dense_out = np.maximum(dense_out, 0)
        
        # 4. Second Dense layer (linear)
        out = np.dot(dense_out, self.dense1_w) + self.dense1_b
        return out

def load_keras_model():
    app_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(app_dir)
    workspace_dir = os.path.dirname(backend_dir)
    
    weights_search_paths = [
        os.path.join(workspace_dir, "model.weights.h5"),
        os.path.join(backend_dir, "models", "model.weights.h5"),
        os.path.join(workspace_dir, "models", "model.weights.h5"),
    ]
    
    weights_path = None
    for path in weights_search_paths:
        if os.path.exists(path):
            weights_path = path
            break
            
    if not weights_path:
        raise FileNotFoundError(
            f"Model weights file not found. \n"
            f"Weights searched paths: {weights_search_paths}"
        )
        
    return NumPyLSTMModel(weights_path)

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

@app.get("/api/debug")
def debug_model():
    app_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(app_dir)
    workspace_dir = os.path.dirname(backend_dir)
    
    config_search_paths = [
        os.path.join(workspace_dir, "config.json"),
        os.path.join(backend_dir, "models", "config.json"),
        os.path.join(workspace_dir, "models", "config.json"),
    ]
    
    weights_search_paths = [
        os.path.join(workspace_dir, "model.weights.h5"),
        os.path.join(backend_dir, "models", "model.weights.h5"),
        os.path.join(workspace_dir, "models", "model.weights.h5"),
    ]
    
    paths_status = {}
    for p in config_search_paths + weights_search_paths:
        paths_status[p] = os.path.exists(p)
        
    try:
        models_files = os.listdir(os.path.join(backend_dir, "models"))
    except Exception as e:
        models_files = str(e)
        
    try:
        backend_files = os.listdir(backend_dir)
    except Exception as e:
        backend_files = str(e)
        
    import traceback
    load_error = None
    try:
        load_keras_model()
    except Exception as e:
        load_error = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
        
    model_loaded = app.state.model is not None
    model_type = type(app.state.model).__name__ if model_loaded else "None"
    
    return {
        "model_loaded": model_loaded,
        "model_type": model_type,
        "paths_status": paths_status,
        "backend_dir_files": backend_files,
        "models_dir_files": models_files,
        "cwd": os.getcwd(),
        "env_model_path": os.getenv("MODEL_PATH"),
        "load_error": load_error
    }

app.include_router(forecast.router, prefix="/api")
