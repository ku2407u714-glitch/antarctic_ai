from pathlib import Path
import csv
import math

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

ICEBERGS = [
    {"iceberg_id": "A01", "date": "2026-09-10", "latitude": -70.2, "longitude": 25.4, "speed": 0.8, "direction": "Southeast", "risk": "Medium"},
    {"iceberg_id": "B07", "date": "2026-09-10", "latitude": -68.6, "longitude": 18.1, "speed": 0.5, "direction": "East", "risk": "Low"},
    {"iceberg_id": "C12", "date": "2026-09-10", "latitude": -72.4, "longitude": 31.8, "speed": 1.1, "direction": "South", "risk": "High"},
    {"iceberg_id": "D03", "date": "2026-09-10", "latitude": -66.9, "longitude": 27.6, "speed": 0.4, "direction": "Northeast", "risk": "Low"},
    {"iceberg_id": "E18", "date": "2026-09-10", "latitude": -74.1, "longitude": 20.2, "speed": 0.7, "direction": "Southeast", "risk": "Medium"},
    {"iceberg_id": "F22", "date": "2026-09-10", "latitude": -69.4, "longitude": 35.5, "speed": 0.6, "direction": "East", "risk": "Medium"},
    {"iceberg_id": "G05", "date": "2026-09-10", "latitude": -71.3, "longitude": 14.4, "speed": 0.3, "direction": "North", "risk": "Low"},
]


def read_csv(name):
    try:
        with (DATA_DIR / name).open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))
    except (OSError, csv.Error):
        return []


def classify_risk(ice, wind, current):
    score = ice * 0.7 + wind * 0.7 + current * 8
    if score >= 90:
        return "HIGH"
    if score >= 55:
        return "MEDIUM"
    return "LOW"


def demo_prediction(values):
    temperature = values["temperature"]
    wind = values["wind_speed"]
    current = values["ocean_current"]
    ocean_temperature = values["ocean_temperature"]
    ice = max(18, min(96, 67 + (abs(temperature) - 18) * 0.9 + wind * 0.16 - ocean_temperature * 2 + current * 2.5))
    risk = classify_risk(ice, wind, current)
    iceberg_count = max(3, min(18, round(5 + wind / 8 + current * 1.5)))
    action = {"LOW": "Proceed on the recommended corridor and continue routine monitoring.", "MEDIUM": "Proceed with caution and monitor iceberg zones.", "HIGH": "Hold course changes and request a fresh operational assessment."}[risk]
    return {"sea_ice": round(ice), "risk": risk, "iceberg_count": iceberg_count, "action": action, "demo": True}


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/icebergs")
def icebergs():
    return jsonify({"icebergs": ICEBERGS, "source": "Simulated demonstration data"})


@app.get("/api/weather")
def weather():
    rows = read_csv("weather_data.csv")
    return jsonify({"weather": rows[0] if rows else {"temperature": -18, "wind_speed": 24, "wind_direction": "SW", "pressure": 986}, "source": "Simulated demonstration data"})


@app.post("/api/predict")
def predict():
    payload = request.get_json(silent=True) or {}
    try:
        values = {"temperature": float(payload.get("temperature", -18)), "wind_speed": float(payload.get("wind_speed", 24)), "ocean_current": float(payload.get("ocean_current", 1.2)), "ocean_temperature": float(payload.get("ocean_temperature", -1.5))}
    except (TypeError, ValueError):
        return jsonify({"error": "All environmental values must be numeric."}), 400
    if values["wind_speed"] < 0 or values["ocean_current"] < 0:
        return jsonify({"error": "Wind speed and ocean current cannot be negative."}), 400
    return jsonify(demo_prediction(values))


@app.post("/api/route")
def route():
    payload = request.get_json(silent=True) or {}
    start = payload.get("start", "Research Vessel")
    destination = payload.get("destination", "Research Station B")
    return jsonify({"route_name": "SAFE ROUTE A", "start": start, "destination": destination, "distance": 568, "time": 42, "fuel": 1240, "risk": "LOW", "ice_exposure": 18, "safety_score": 94, "fuel_efficiency": 87, "message": "Recommended route avoids high-risk sea-ice and predicted iceberg zones.", "demo": True})


if __name__ == "__main__":
    app.run(debug=True)
