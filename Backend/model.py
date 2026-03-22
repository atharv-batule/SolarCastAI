import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

print("🚀 Training Solar Power Model...")

data = pd.read_csv("./Solar Power Plant Data.csv")

data['Date-Hour(NMT)'] = pd.to_datetime(
    data['Date-Hour(NMT)'],
    format='%d.%m.%Y-%H:%M'
)

data['hour'] = data['Date-Hour(NMT)'].dt.hour
data['month'] = data['Date-Hour(NMT)'].dt.month

#
data["lag_1"] = data["SystemProduction"].shift(1)
data["lag_2"] = data["SystemProduction"].shift(2)
data["lag_3"] = data["SystemProduction"].shift(3)

data["lag_24"] = data["SystemProduction"].shift(24)
data["lag_48"] = data["SystemProduction"].shift(48)

data["rolling_mean_6"] = data["SystemProduction"].rolling(6).mean()
data["rolling_std_6"] = data["SystemProduction"].rolling(6).std()


data = data.ffill()
data = data.dropna()



# Selected features based on correlation
X = data[
[
"Radiation",
"Sunshine",
"AirTemperature",
"WindSpeed",
"hour",
"AirPressure",
"month",
"RelativeAirHumidity",
 # lag features
    "lag_1",
    "lag_2",
    "lag_3",
    "lag_24",
    "lag_48",

    # rolling features
    "rolling_mean_6",
    "rolling_std_6"
]
]

# target (kW → MW)
y = data["SystemProduction"] / 1000

split = int(len(X)*0.8)

X_train = X[:split]
X_test = X[split:]

y_train = y[:split]
y_test = y[split:]

model = RandomForestRegressor(
    n_estimators=300,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\nModel Evaluation")
print("----------------")
print("MAE:", round(mae,3))
print("RMSE:", round(rmse,3))
print("R2:", round(r2,3))

joblib.dump(model, "solar_model.pkl")

print("\n✅ Model saved")