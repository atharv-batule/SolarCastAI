from flask import Blueprint,Flask, app, jsonify
import pandas as pd
from predict import predict_today
from weatherforecast import fetch_weather_dataset
from Controller.analytics import analytics


analytics_bp = Blueprint("analytics", __name__, url_prefix="/api")

@analytics_bp.route("/analytics", methods=["GET"])
def get_analytics():
    lat = 15.2833
    lon = 73.9833
    return analytics(lat, lon)