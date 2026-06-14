import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier

import joblib


df = pd.read_csv(
    "dataset/appointments.csv"
)

X = df[
    [
        "Age",
        "Previous_No_Shows",
        "SMS_Received"
    ]
]

y = df["No_Show"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    random_state=42
)

model.fit(
    X_train,
    y_train
)

joblib.dump(
    model,
    "ml/no_show_model.pkl"
)

print("Model Saved")