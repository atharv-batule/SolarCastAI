import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

print("🚀 Training Solar Power Model...")

# Load dataset
data = pd.read_csv(r"c:\Users\athar\Downloads\Solar Power Plant Data.csv")

# Convert datetime
data['Date-Hour(NMT)'] = pd.to_datetime(
    data['Date-Hour(NMT)'],
    format='%d.%m.%Y-%H:%M'
)

# Feature engineering
data['hour'] = data['Date-Hour(NMT)'].dt.hour
data['month'] = data['Date-Hour(NMT)'].dt.month

# Remove datetime
data = data.drop(columns=['Date-Hour(NMT)'])

# Handle missing values
data = data.ffill()

# Features
X = data[['WindSpeed',
          'Sunshine',
          'AirPressure',
          'Radiation',
          'AirTemperature',
          'RelativeAirHumidity',
          'hour',
          'month']]

# Target
y = data['SystemProduction']

# Train split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "solar_model.pkl")

print("✅ Model trained and saved as solar_model.pkl")