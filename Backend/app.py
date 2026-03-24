from flask import Flask, jsonify
import pandas as pd
from predict import predict_today
from weatherforecast import fetch_weather_dataset
from routes.solar_forecast import solar_bp
from routes.analytics import analytics_bp
app = Flask(__name__)
app.register_blueprint(solar_bp)
app.register_blueprint(analytics_bp)

if __name__ == "__main__":
    app.run(debug=True)