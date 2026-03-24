from predict import predict_today
import pandas as pd
from flask import jsonify


def get_solar_forecast(lat, lon):

    # -------------------------------
    # STEP 1: Load historical solar data
    # -------------------------------
    history_df = pd.read_csv("Solar Power Plant Data.csv")

    # Clean column names
    history_df.columns = history_df.columns.str.strip().str.replace(" ", "")

    # Fix datetime for history (NO timezone needed here)
    if "Date-Hour" in history_df.columns:
        history_df["Date-Hour"] = pd.to_datetime(
            history_df["Date-Hour"].astype(str).str.replace(" IST", "", regex=False),
            errors="coerce"
        )
        history_df = history_df.sort_values("Date-Hour")

    # Keep recent rows (for lag features)
    history_df = history_df.tail(100)

    # -------------------------------
    # STEP 2: Predict
    # -------------------------------
    df = predict_today(lat, lon, history_df)

    # -------------------------------
    # STEP 3: Convert to IST + STRING (IMPORTANT)
    # -------------------------------
    df["Date-Hour"] = (
        pd.to_datetime(df["Date-Hour"], errors="coerce")
        .dt.tz_localize("UTC")
        .dt.tz_convert("Asia/Kolkata")
        .dt.strftime("%Y-%m-%d %H:%M:%S")
    )

    forecast = df.to_dict(orient="records")

    # -------------------------------
    # Insights (use datetime BEFORE string conversion)
    # -------------------------------
    df_temp = pd.to_datetime(df["Date-Hour"], errors="coerce")

    peak_idx = df["PredictedSolarPower"].idxmax()
    peak_time = df_temp.iloc[peak_idx].strftime("%H:%M")
    peak_value = round(float(df["PredictedSolarPower"].max()), 2)

    avg_power = round(float(df["PredictedSolarPower"].mean()), 2)

    insights = [
        {
            "title": "Peak Solar Production",
            "description": "Solar output will reach its highest level during the day.",
            "detail": f"Peak production of about {peak_value} units is expected around {peak_time}.",
            "icon": "sun"
        },
        {
            "title": "Average Daily Production",
            "description": "Average solar generation level for the forecast period.",
            "detail": f"The average predicted production is about {avg_power} units.",
            "icon": "chart"
        }
    ]

    return jsonify({
        "forecast": forecast,
        "insights": insights
    })