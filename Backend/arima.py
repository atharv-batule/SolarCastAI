import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing

print("🚀 Training Time Series Models...")

# -------------------------------
# Load Data
# -------------------------------
data = pd.read_csv("./Solar Power Plant Data.csv")

data['Date-Hour(NMT)'] = pd.to_datetime(
    data['Date-Hour(NMT)'],
    format='%d.%m.%Y-%H:%M'
)

data = data.sort_values(by="Date-Hour(NMT)")

# target (kW → MW)
series = data["SystemProduction"] / 1000

# -------------------------------
# Train-Test Split (time-based)
# -------------------------------
split = int(len(series) * 0.8)

train = series[:split]
test = series[split:]

# -------------------------------
# 1️⃣ ARIMA Model
# -------------------------------
print("\n🔹 Training ARIMA...")

arima_model = ARIMA(train, order=(5,1,2))
arima_fit = arima_model.fit()

arima_pred = arima_fit.forecast(steps=len(test))

# -------------------------------
# 2️⃣ Exponential Smoothing
# -------------------------------
print("🔹 Training Exponential Smoothing...")

exp_model = ExponentialSmoothing(
    train,
    trend="add",
    seasonal="add",
    seasonal_periods=24  # daily cycle
)

exp_fit = exp_model.fit()

exp_pred = exp_fit.forecast(len(test))

# -------------------------------
# Evaluation Function
# -------------------------------
def evaluate(y_true, y_pred, name):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    print(f"\n{name} Results")
    print("----------------")
    print("MAE:", round(mae, 3))
    print("RMSE:", round(rmse, 3))
    print("R2:", round(r2, 3))

    return mae, rmse, r2

# -------------------------------
# Evaluate Models
# -------------------------------
arima_metrics = evaluate(test, arima_pred, "ARIMA")
exp_metrics = evaluate(test, exp_pred, "Exponential Smoothing")

# -------------------------------
# Compare
# -------------------------------
print("\n📊 Model Comparison")
print("--------------------")

models = ["ARIMA", "Exp Smoothing"]
results = [arima_metrics, exp_metrics]

for i, model in enumerate(models):
    print(f"{model}: MAE={results[i][0]:.3f}, RMSE={results[i][1]:.3f}, R2={results[i][2]:.3f}")

print("\n✅ Done!")