from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Request
import pandas as pd
import io
from app.services.forecaster import process_and_forecast

router = APIRouter()

@router.post("/forecast")
async def create_forecast(
    request: Request,
    file: UploadFile = File(...),
    horizon: int = Form(30)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")
        
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV: {e}")
        
    # Check if 'Date' and 'Sales' columns exist
    if 'Date' not in df.columns or 'Sales' not in df.columns:
        raise HTTPException(status_code=400, detail="CSV must contain 'Date' and 'Sales' columns.")
        
    model = request.app.state.model
    if model is None:
        raise HTTPException(status_code=503, detail="Forecast model is not loaded.")
        
    try:
        result = process_and_forecast(df, horizon, model)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecasting error: {e}")
