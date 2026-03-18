from flask import Flask, jsonify;
from solar_forecast import get_solar_forecast;
from predict import predict_today;
from weatherforecast import fetch_weather_dataset;

app = Flask(__name__)

@app.route("/solar-forecast", methods=["GET"])
def solar_forecast():
    return get_solar_forecast(15.2833, 73.9833);
    