import joblib
import pandas as pd
import numpy as np
from weatherforecast import fetch_weather_dataset


# -------------------------------
# Load model
# -------------------------------
model = joblib.load("solar_model.pkl")


# -------------------------------
# Feature list (MUST match training)
# -------------------------------
FEATURE_COLS = [
    "Radiation",
    "Sunshine",
    "AirTemperature",
    "WindSpeed",
    "hour",
    "AirPressure",
    "month",
    "RelativeAirHumidity",
    "lag_1",
    "lag_2",
    "lag_3",
    "lag_24",
    "lag_48",
    "rolling_mean_6",
    "rolling_std_6"
]


# -------------------------------
# Prediction (Recursive)
# -------------------------------
def predict_today(lat, lon, history_df):
    """
    history_df must contain:
    - SystemProduction column
    - Date-Hour column
    """

    # -------------------------------
    # CLEAN HISTORY DATA ✅
    # -------------------------------
    history_df.columns = history_df.columns.str.strip().str.replace(" ", "")

    if "SystemProduction" not in history_df.columns:
        raise ValueError(f"❌ 'SystemProduction' column missing. Found: {history_df.columns}")

    # Fix datetime if needed
    if "Date-Hour" in history_df.columns:
        history_df["Date-Hour"] = pd.to_datetime(
            history_df["Date-Hour"].astype(str).str.replace(" IST", "", regex=False),
            errors="coerce"
        )
        history_df = history_df.sort_values("Date-Hour")

    # Keep last 100 rows (for lag safety)
    history_df = history_df.tail(100)

    # Convert to MW (same as training)
    history_power = list(history_df["SystemProduction"] / 1000)

    # Safety check
    if len(history_power) < 50:
        raise ValueError("❌ Not enough history data (need at least 50 rows)")

    # -------------------------------
    # FETCH WEATHER FORECAST
    # -------------------------------
    forecast_df = fetch_weather_dataset(lat, lon)

    forecast_df["Date-Hour"] = pd.to_datetime(
        forecast_df["Date-Hour"].astype(str).str.replace(" IST", "", regex=False),
        errors="coerce"
    )

    forecast_df["hour"] = forecast_df["Date-Hour"].dt.hour
    forecast_df["month"] = forecast_df["Date-Hour"].dt.month

    predictions = []

    # -------------------------------
    # RECURSIVE PREDICTION LOOP
    # -------------------------------
    for i in range(len(forecast_df)):

        row = forecast_df.iloc[i].copy()

        # Lag features
        row["lag_1"] = history_power[-1]
        row["lag_2"] = history_power[-2]
        row["lag_3"] = history_power[-3]
        row["lag_24"] = history_power[-24]
        row["lag_48"] = history_power[-48]

        # Rolling features
        last_6 = history_power[-6:]
        row["rolling_mean_6"] = np.mean(last_6)
        row["rolling_std_6"] = np.std(last_6)

        # Prepare input
        X = pd.DataFrame([row])[FEATURE_COLS]

        # Predict
        pred = model.predict(X)[0]

        # Physics constraint
        if row["Radiation"] < 20:
            pred = 0

        pred = max(pred, 0)

        # Store prediction
        pred = round(pred, 2)
        predictions.append(pred)

        # Update history (recursive)
        history_power.append(pred)

    # -------------------------------
    # OUTPUT
    # -------------------------------
    forecast_df["PredictedSolarPower"] = predictions

    return forecast_df[["Date-Hour", "PredictedSolarPower"]]