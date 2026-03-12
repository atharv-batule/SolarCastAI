import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

def main():
    print("🚀 Starting Solar Power Forecasting Model...\n")

    # 1️⃣ Load the Dataset
    print("Loading dataset...")
    try:
        data = pd.read_csv("c:\\Users\\athar\\Downloads\\Solar Power Plant Data.csv")
    except FileNotFoundError:
        print("❌ Error: 'solar_data.csv' not found. Please ensure it's in the same directory.")
        return

    # 2️⃣ Convert the Time Column
    print("Processing datetime column...")
    data['Date-Hour(NMT)'] = pd.to_datetime(
        data['Date-Hour(NMT)'],
        format='%d.%m.%Y-%H:%M'
    )

    # 3️⃣ Feature Engineering (Extract Time Features)
    data['hour'] = data['Date-Hour(NMT)'].dt.hour
    data['day'] = data['Date-Hour(NMT)'].dt.day
    data['month'] = data['Date-Hour(NMT)'].dt.month

    # Remove the original datetime column
    data = data.drop(columns=['Date-Hour(NMT)'])

    # 4️⃣ Handle Missing Values (Updated Pandas Syntax)
    print("Cleaning missing values...")
    data = data.ffill()

    # 5️⃣ Define Features and Target
    X = data[['WindSpeed',
              'Sunshine',
              'AirPressure',
              'Radiation',
              'AirTemperature',
              'RelativeAirHumidity',
              'hour',
              'month']]
    y = data['SystemProduction']

    # 6️⃣ Train/Test Split
    print("Splitting data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 7️⃣ Train the Model (Random Forest)
    print("Training the Random Forest model (this might take a few seconds)...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 8️⃣ Make Predictions
    print("Making predictions...")
    predictions = model.predict(X_test)

    # 9️⃣ Evaluate Model Performance
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print("\n✅ --- Model Evaluation ---")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"R-squared (R2) Score: {r2:.4f}")
    print("--------------------------\n")

    # 🔟 Example Prediction
    print("Testing a sample prediction...")
    sample = [[
        5,      # WindSpeed
        8,      # Sunshine
        1012,   # AirPressure
        600,    # Radiation
        30,     # AirTemperature
        60,     # Humidity
        12,     # Hour
        6       # Month
    ]]
    
    # Needs a DataFrame to match feature names and suppress sklearn warnings
    sample_df = pd.DataFrame(sample, columns=X.columns)
    sample_prediction = model.predict(sample_df)
    print(f"Predicted Solar Power for sample: {sample_prediction[0]:.2f}\n")

    # --- Visualizations ---
    print("📊 Generating Visualizations... (Close each window to see the next one)")

    # Viz 1: Actual vs Predicted
    plt.figure(figsize=(10, 5))
    plt.plot(y_test.values[:100], label="Actual")
    plt.plot(predictions[:100], label="Predicted", alpha=0.7)
    plt.legend()
    plt.title("Solar Power Forecasting: Actual vs Predicted (First 100 Samples)")
    plt.xlabel("Samples")
    plt.ylabel("System Production")
    plt.tight_layout()
    plt.show()

    # Viz 2: Feature Importance
    importance = model.feature_importances_
    plt.figure(figsize=(10, 5))
    plt.bar(X.columns, importance, color='orange')
    plt.title("Weather Impact on Solar Production (Feature Importance)")
    plt.xticks(rotation=45)
    plt.ylabel("Importance Score")
    plt.tight_layout()
    plt.show()

    # Viz 3: Average Solar Production by Hour
    peak_hours = data.groupby('hour')['SystemProduction'].mean()
    plt.figure(figsize=(10, 5))
    peak_hours.plot(color='green', marker='o')
    plt.title("Average Solar Production by Hour of Day")
    plt.xlabel("Hour of Day (0-23)")
    plt.ylabel("Average Production")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

    print("🎉 Run complete!")

if __name__ == "__main__":
    main()