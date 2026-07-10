import pandas as pd
import numpy as np
from datetime import timedelta

def process_and_forecast(df: pd.DataFrame, horizon: int, model):
    """
    Process the historical sales data and forecast the future.
    Optimized for Sales Forecasting context.
    """
    # 1. Preprocessing
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
    
    # Sort and remove duplicates
    df = df.sort_values('Date').drop_duplicates(subset=['Date'])
    
    # Impute missing sales values with forward fill, then backward fill
    df['Sales'] = df['Sales'].ffill().bfill()
    
    if len(df) == 0:
        raise ValueError("Dataset is empty after cleaning.")

    historical_records = df.to_dict(orient='records')
    
    # KPIs for historical data
    total_historical_revenue = df['Sales'].sum()
    avg_daily_sales = df['Sales'].mean()
    
    # Calculate simple MoM growth if we have enough data (approx 30 days)
    if len(df) >= 30:
        last_30_days = df.iloc[-30:]['Sales'].sum()
        prev_30_days = df.iloc[-60:-30]['Sales'].sum() if len(df) >= 60 else None
        if prev_30_days and prev_30_days > 0:
            historical_growth_rate = ((last_30_days - prev_30_days) / prev_30_days) * 100
        else:
            historical_growth_rate = 0.0
    else:
        historical_growth_rate = 0.0
        
    # 2. Forecasting
    last_date = df['Date'].max()
    future_dates = [last_date + timedelta(days=i) for i in range(1, horizon + 1)]
    
    # Check if the model is a Keras model or scikit-learn fallback
    is_keras = False
    try:
        if hasattr(model, 'input_shape') or type(model).__name__ in ('Sequential', 'Functional', 'Model'):
            is_keras = True
    except Exception:
        pass

    if is_keras:
        # We need min and max sales to scale/inverse-scale the main sequence and outputs
        min_sales = float(df['Sales'].min())
        max_sales = float(df['Sales'].max())
        sales_range = max_sales - min_sales
        if sales_range == 0.0:
            sales_range = 1.0

        # Define the 34 features
        feature_cols = [f'Feature_{i}' for i in range(1, 35)]
        
        # Check if all 34 features exist in the uploaded df; if not, auto-generate them
        missing_features = [col for col in feature_cols if col not in df.columns]
        if len(missing_features) > 0:
            print(f"Warning: Missing feature columns {missing_features}. Generating scaled lag features from Sales.")
            # Scale sales first to [0, 1] so that generated lags are also in [0, 1]
            df['Sales_scaled'] = (df['Sales'] - min_sales) / sales_range
            for i, col in enumerate(feature_cols):
                if col not in df.columns:
                    # Shift scaled sales to create lag features
                    df[col] = df['Sales_scaled'].shift(i).bfill().fillna(0.0)
                    
        if len(df) < 28:
            raise ValueError(f"Dataset has only {len(df)} rows, but the LSTM model requires at least 28 rows of history.")
            
        # Extract features matrix of shape (len(df), 34)
        features_matrix = df[feature_cols].values.astype(np.float32)
        
        # Scale each feature column independently to [0, 1] for input stability
        min_vals = features_matrix.min(axis=0)
        max_vals = features_matrix.max(axis=0)
        denom = max_vals - min_vals
        denom[denom == 0.0] = 1.0
        features_matrix_scaled = (features_matrix - min_vals) / denom
        
        # Take the last 28 rows of the scaled features to form the initial sequence of shape (1, 28, 34)
        last_sequence = features_matrix_scaled[-28:]
        current_seq = np.expand_dims(last_sequence, axis=0).astype(np.float32)
        
        predictions_scaled = []
        for step in range(horizon):
            pred = model.predict(current_seq, verbose=0)
            pred_value = float(pred[0, 0])
            predictions_scaled.append(pred_value)
            
            # Rolling forecast sequence update in the scaled space
            next_features = np.zeros(34, dtype=np.float32)
            next_features[0] = pred_value # Set scaled prediction as first feature
            next_features[1:] = current_seq[0, -1, 0:33] # Shift previous lags
            
            next_features_seq = np.expand_dims(np.expand_dims(next_features, axis=0), axis=0)
            current_seq = np.concatenate([current_seq[:, 1:, :], next_features_seq], axis=1)
            
        # Inverse-scale the scaled predictions back to the original Sales range
        predictions = np.array(predictions_scaled) * sales_range + min_sales
    else:
        # Fallback dummy feature extraction for the dummy model we created
        future_X = np.array([[len(df) + i] for i in range(1, horizon + 1)])
        predictions = model.predict(future_X)
    
    # Ensure no negative sales
    predictions = np.maximum(predictions, 0)
    
    forecast_results = []
    for d, p in zip(future_dates, predictions):
        forecast_results.append({
            "Date": d.strftime("%Y-%m-%d"),
            "Sales": round(float(p), 2)
        })
        
    # 3. KPI Summaries
    projected_revenue = sum([f['Sales'] for f in forecast_results])
    expected_avg_daily = projected_revenue / horizon
    
    summary = {
        "forecast_days": horizon,
        "total_historical_revenue": round(float(total_historical_revenue), 2),
        "historical_avg_daily_sales": round(float(avg_daily_sales), 2),
        "historical_monthly_growth_rate_pct": round(float(historical_growth_rate), 2),
        "projected_revenue": round(float(projected_revenue), 2),
        "projected_avg_daily_sales": round(float(expected_avg_daily), 2)
    }

    # Format historical dates as strings for JSON
    formatted_historical = []
    for r in historical_records:
        formatted_historical.append({
            "Date": r["Date"].strftime("%Y-%m-%d"),
            "Sales": round(float(r["Sales"]), 2)
        })

    return {
        "historical": formatted_historical,
        "forecast": forecast_results,
        "summary": summary
    }
