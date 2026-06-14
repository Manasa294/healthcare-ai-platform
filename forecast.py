from prophet import Prophet
import pandas as pd

# Sample monthly no-show counts
data = pd.DataFrame({

    "ds": [
        "2025-01-31",
        "2025-02-28",
        "2025-03-31",
        "2025-04-30",
        "2025-05-31",
        "2025-06-30"
    ],

    "y": [
        20,
        25,
        30,
        35,
        40,
        45
    ]

})

# Create model
model = Prophet()

# Train model
model.fit(data)

# Forecast next 6 months
future = model.make_future_dataframe(
    periods=6,
    freq="ME"   # Monthly End (new Pandas format)
)

# Generate predictions
forecast = model.predict(future)

# Show results
print("\nForecasted No-Shows:\n")

print(
    forecast[
        ["ds", "yhat"]
    ].tail(6)
)