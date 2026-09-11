from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
data = pd.read_csv(ROOT / "data" / "sea_ice_data.csv")
features = ["temperature", "wind_speed", "ocean_temperature", "current_speed"]
X_train, X_test, y_train, y_test = train_test_split(data[features], data["ice_concentration"], test_size=0.3, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print(f"MAE: {mean_absolute_error(y_test, predictions):.2f}")
print(f"R2: {r2_score(y_test, predictions):.2f}")
joblib.dump(model, ROOT / "models" / "sea_ice_model.joblib")
print("Saved demo model to models/sea_ice_model.joblib")
