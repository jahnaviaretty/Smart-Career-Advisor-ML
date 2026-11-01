
import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Project folder
BASE_DIR = Path(__file__).resolve().parent

# Load dataset
data_path = BASE_DIR / "database" / "career_dataset.csv"
data = pd.read_csv(data_path)

# Separate input features and target
X = data.drop("Career", axis=1)
y = data["Career"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)

print("Model training completed!")
print("Accuracy:", accuracy_score(y_test, predictions))
print("\nClassification Report:")
print(classification_report(y_test, predictions, zero_division=0))

# Save trained model
model_folder = BASE_DIR / "models"
model_folder.mkdir(exist_ok=True)

model_path = model_folder / "career_model.joblib"
joblib.dump(model, model_path)

print("\nModel saved successfully at:", model_path)
