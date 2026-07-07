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
    
    # Dummy feature extraction for the dummy model we created
    # The dummy model just takes a single feature (like an index or day counter)
    # If using a real model like Prophet, we'd pass the dataframe.
    # Here we just use an increasing index starting from len(df) + 1
    future_X = np.array([[len(df) + i] for i in range(1, horizon + 1)])
    
    # Generate predictions
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
