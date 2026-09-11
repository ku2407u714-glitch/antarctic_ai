from pathlib import Path
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "sea_ice_model.joblib"
FEATURES = ["temperature", "wind_speed", "ocean_temperature", "current_speed"]


def predict_sea_ice(values):
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Train the demo model first with python ml/train_sea_ice.py")
    model = joblib.load(MODEL_PATH)
    frame = pd.DataFrame([values], columns=FEATURES)
    return float(model.predict(frame)[0])


if __name__ == "__main__":
    print(predict_sea_ice({"temperature": -18, "wind_speed": 24, "ocean_temperature": -1.5, "current_speed": 1.2}))
