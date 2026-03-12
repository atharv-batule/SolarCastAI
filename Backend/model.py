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

data = data.ffill()

# Selected features based on correlation
X = data[
[
"Radiation",
"Sunshine",
"AirTemperature",
"WindSpeed",
"hour",

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