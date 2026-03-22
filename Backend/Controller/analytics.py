from flask import Flask, jsonify
import pandas as pd
from predict import predict_today
from weatherforecast import fetch_weather_dataset

def analytics(lat,lon):

    # lat = 15.2833
    # lon = 73.9833

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