import joblib
from weatherforecast import fetch_weather_dataset

# Load trained model once
model = joblib.load("solar_model.pkl")


def predict_today(lat, lon):

    # Fetch weather forecast
    weather_df = fetch_weather_dataset(lat, lon)

    # Feature columns used by the model
    features = weather_df[
        [
            "WindSpeed",
            "Sunshine",
            "AirPressure",
            "Radiation",
            "AirTemperature",
            "RelativeAirHumidity",
            "hour",
            "month",
        ]
    ]

    # Predict solar output
    predictions = model.predict(features)

    # Add predictions to dataframe
    weather_df["PredictedSolarPower"] = predictions

    # -------- Physics sanity fixes --------

    # Solar production cannot be negative
    weather_df["PredictedSolarPower"] = weather_df["PredictedSolarPower"].clip(lower=0)

    # If radiation is extremely low, assume no solar production
    weather_df.loc[weather_df["Radiation"] < 20, "PredictedSolarPower"] = 0

    # Round values for cleaner output
    weather_df["PredictedSolarPower"] = weather_df["PredictedSolarPower"].round(2)

    # Return only what frontend needs
    result = weather_df[["Date-Hour", "PredictedSolarPower"]]

    return result