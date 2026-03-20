
from email.policy import default

from weatherforecast import fetch_weather_dataset
from predict import predict_today
import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)


def get_solar_forecast(lat, lon):
    # Get solar predictions
    df = predict_today(lat, lon)

    # Fix datetime format
    df["Date-Hour"] = pd.to_datetime(
        df["Date-Hour"].astype(str).str.replace(" IST", "", regex=False)
    )

    # Forecast data (UNCHANGED)
    forecast = df.to_dict(orient="records")

    # -------- Generate simple insights --------
    peak_row = df.loc[df["PredictedSolarPower"].idxmax()]
    peak_time = peak_row["Date-Hour"].strftime("%H:%M")
    peak_value = round(float(peak_row["PredictedSolarPower"]), 2)

    avg_power = round(float(df["PredictedSolarPower"].mean()), 2)

    insights = [
        {
            "title": "Peak Solar Production",
            "description": "Solar output will reach its highest level during the day.",
            "detail": f"Peak production of about {peak_value} units is expected around {peak_time}.",
            "icon": "sun"
        },
        {
            "title": "Morning Generation Ramp",
            "description": "Solar production begins after sunrise.",
            "detail": "Energy generation starts increasing after 07:00 as solar radiation increases.",
            "icon": "sunrise"
        },
        {
            "title": "Evening Decline",
            "description": "Solar output drops after sunset.",
            "detail": "Production gradually decreases after 17:00 and reaches zero by evening.",
            "icon": "sunset"
        },
        {
            "title": "Average Daily Production",
            "description": "Average solar generation level for the forecast period.",
            "detail": f"The average predicted production is about {avg_power} units.",
            "icon": "chart"
        }
    ]

    response = {
        "forecast": forecast,
        "insights": insights
    }

    return jsonify(response)

