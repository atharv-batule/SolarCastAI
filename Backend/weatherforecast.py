import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

# Setup API client with caching and retries
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

openmeteo = openmeteo_requests.Client(session=retry_session)


def fetch_weather_dataset(lat, lon):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": [
            "wind_speed_10m",
            "sunshine_duration",
            "surface_pressure",
            "shortwave_radiation",
            "temperature_2m",
            "relative_humidity_2m"
        ],
        "forecast_days": 16,
        "timezone": "Asia/Kolkata"
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    hourly = response.Hourly()

    # Create dataframe
    data = {
        "Date-Hour": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ).tz_convert("Asia/Kolkata"),

        "WindSpeed": hourly.Variables(0).ValuesAsNumpy(),
        "Sunshine": hourly.Variables(1).ValuesAsNumpy() / 3600,
        "AirPressure": hourly.Variables(2).ValuesAsNumpy(),
        "Radiation": hourly.Variables(3).ValuesAsNumpy(),
        "AirTemperature": hourly.Variables(4).ValuesAsNumpy(),
        "RelativeAirHumidity": hourly.Variables(5).ValuesAsNumpy()
    }

    df = pd.DataFrame(data)

    # Extract time features for ML model
    df["hour"] = df["Date-Hour"].dt.hour
    df["month"] = df["Date-Hour"].dt.month

    # Convert datetime to readable IST string
    df["Date-Hour"] = df["Date-Hour"].dt.strftime("%Y-%m-%d %H:%M:%S IST")

    return df