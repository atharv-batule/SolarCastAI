import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib  # Used to save the model

# --- 1. DATA PREPARATION ---
# Generating synthetic data so the code works 'out of the box'
# Replace this block with: df = pd.read_csv('your_weather_file.csv')
data_size = 1000
np.random.seed(42)
df = pd.DataFrame({
    'WindSpeed': np.random.uniform(0, 30, data_size),
    'Sunshine': np.random.uniform(0, 12, data_size),
    'AirPressure': np.random.uniform(980, 1030, data_size),
    'Radiation': np.random.uniform(0, 1000, data_size),
    'AirTemperature': np.random.uniform(-5, 40, data_size),
    'RelativeAirHumidity': np.random.uniform(20, 100, data_size),
    'Hour': np.tile(np.arange(24), data_size // 24 + 1)[:data_size],
    'DayOfYear': np.repeat(np.arange(1, 366), 24)[:data_size]
})

# Define attributes
features = [
    'WindSpeed', 'Sunshine', 'AirPressure', 'Radiation', 
    'AirTemperature', 'RelativeAirHumidity', 'Hour', 'DayOfYear'
]

# Create 'Next Day' Targets (Shift by 24 hours)
prediction_lag = 24 
df_targets = df[features].shift(-prediction_lag)
df_targets.columns = [f"Next_{col}" for col in features]

# Clean up: Merge features and targets, drop NaN rows created by shifting
processed_data = pd.concat([df[features], df_targets], axis=1).dropna()

X = processed_data[features]
y = processed_data[[f"Next_{col}" for col in features]]

# --- 2. MODEL TRAINING ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Multi-output Random Forest
model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Save the model for later use in your Backend
joblib.dump(model, 'weather_model.pkl')
print("Model trained and saved as 'weather_model.pkl'")

# --- 3. READY-MADE EXAMPLE (PREDICTION) ---

def predict_tomorrow(api_data):
    """
    Takes a dictionary of current weather and returns predicted weather for 24h later.
    """
    # Convert input to DataFrame
    input_df = pd.DataFrame([api_data])
    
    # Ensure columns are in the correct order
    input_df = input_df[features]
    
    # Predict
    prediction = model.predict(input_df)
    
    # Format the output nicely
    result_columns = [f"Next_{col}" for col in features]
    return dict(zip(result_columns, prediction[0]))

# Example: Data you might get from an API right now
current_weather_sample = {
    'WindSpeed': 15.2,
    'Sunshine': 5.5,
    'AirPressure': 1015.0,
    'Radiation': 600.0,
    'AirTemperature': 28.5,
    'RelativeAirHumidity': 45.0,
    'Hour': 12,        # 12:00 PM
    'DayOfYear': 150   # Late May
}

tomorrow_forecast = predict_tomorrow(current_weather_sample)

print("\n--- PREDICTION FOR TOMORROW AT THIS TIME ---")
for key, value in tomorrow_forecast.items():
    print(f"{key}: {value:.2f}")