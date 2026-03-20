from flask import Flask, jsonify
import pandas as pd
from predict import predict_today
from weatherforecast import fetch_weather_dataset

app = Flask(__name__)


@app.route("/solar-forecast", methods=["GET"])
def solar_forecast():

    lat = 15.2833
    lon = 73.9833

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
    forecast_df = df.copy()
    forecast_df["Date-Hour"] = forecast_df["Date-Hour"].dt.strftime("%Y-%m-%d %H:%M:%S")
    forecast = forecast_df.to_dict(orient="records")

    response = {
        "forecast": forecast,
        "insights": insights
    }

    return jsonify(response)


@app.route("/analytics", methods=["GET"])
def analytics():

    lat = 15.2833
    lon = 73.9833

    weather_df = fetch_weather_dataset(lat, lon)
    pred_df = predict_today(lat, lon)

    df = pd.merge(weather_df, pred_df, on="Date-Hour")

    df["Date-Hour"] = pd.to_datetime(
        df["Date-Hour"].astype(str).str.replace(" IST", "", regex=False)
    )

    df["date"] = df["Date-Hour"].dt.strftime("%Y-%m-%d")
    df["hour"] = df["Date-Hour"].dt.hour

    radiation_vs_production = df[["Radiation","PredictedSolarPower"]] \
        .astype(float) \
        .to_dict(orient="records")

    temperature_vs_production = df[["AirTemperature","PredictedSolarPower"]] \
        .astype(float) \
        .to_dict(orient="records")

    daily_trend = (
        df.groupby("date")["PredictedSolarPower"]
        .sum()
        .round(2)
        .reset_index()
        .to_dict(orient="records")
    )

    heatmap_df = (
        df.groupby(["date","hour"])["PredictedSolarPower"]
        .mean()
        .reset_index()
    )

    heatmap = heatmap_df.to_dict(orient="records")

    correlation = float(df["Radiation"].corr(df["PredictedSolarPower"]))
    avg_radiation = float(df["Radiation"].mean())
    avg_production = float(df["PredictedSolarPower"].mean())

    response = {
        "average_production": avg_production,
        "average_radiation": avg_radiation,
        "correlation_radiation_production": correlation,
        "radiation_vs_production": radiation_vs_production,
        "temperature_vs_production": temperature_vs_production,
        "solar_production_trends": daily_trend,
        "heatmap": heatmap
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)