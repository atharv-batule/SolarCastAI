from flask import Blueprint, Flask, jsonify;
from solar_forecast import get_solar_forecast;
from predict import predict_today;
from weatherforecast import fetch_weather_dataset;


solar_bp = Blueprint("solar", __name__)
@solar_bp.route("/solar-forecast", methods=["GET"])
def solar_forecast():
    return get_solar_forecast(15.2833, 73.9833);
    