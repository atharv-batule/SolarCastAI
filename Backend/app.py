from flask import Flask, jsonify
import pandas as pd
from predict import predict_today
from weatherforecast import fetch_weather_dataset

app = Flask(__name__)

@app.route("/solar-forecast", methods=["GET"])
def solar_forecast():

    df = predict_today(15.2833, 73.9833)
    result = df.to_dict(orient="records")

    return jsonify(result)


@app.route("/analytics", methods=["GET"])
def analytics():

    lat = 15.2833
    lon = 73.9833

    weather_df = fetch_weather_dataset(lat, lon)
    pred_df = predict_today(lat, lon)

    df = pd.merge(weather_df, pred_df, on="Date-Hour")

    correlation = float(df["Radiation"].corr(df["PredictedSolarPower"]))
    avg_radiation = float(df["Radiation"].mean())
    avg_production = float(df["PredictedSolarPower"].mean())

    scatter_points = df[["Radiation","PredictedSolarPower"]].astype(float).to_dict(orient="records")

    response = {
        "correlation_radiation_production": correlation,
        "average_radiation": avg_radiation,
        "average_production": avg_production,
        "points": scatter_points
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)