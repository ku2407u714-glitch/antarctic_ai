from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="POLARIS API", version="0.1.0", description="Synthetic polar decision-support prototype")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_methods=["*"], allow_headers=["*"])

ICEBERGS = [
    {"iceberg_id": "IB-1042", "latitude": -64.32, "longitude": 12.42, "speed": 0.42, "direction": "NE", "risk": "TL2", "confidence": 87},
    {"iceberg_id": "IB-1188", "latitude": -68.6, "longitude": 18.1, "speed": 0.50, "direction": "E", "risk": "TL1", "confidence": 91},
    {"iceberg_id": "IB-1216", "latitude": -72.4, "longitude": 31.8, "speed": 1.10, "direction": "S", "risk": "TL3", "confidence": 79},
    {"iceberg_id": "IB-1274", "latitude": -66.9, "longitude": 27.6, "speed": 0.40, "direction": "NE", "risk": "TL1", "confidence": 94},
]

class Environment(BaseModel):
    temperature: float = -18
    wind_speed: float = Field(24, ge=0)
    ocean_current: float = Field(1.2, ge=0)
    ocean_temperature: float = -1.5

class RouteRequest(BaseModel):
    start: str = "Research Vessel"
    destination: str = "Research Station B"
    risk_tolerance: str = "MEDIUM"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def prediction(values: Environment) -> dict[str, Any]:
    ice = max(18, min(96, 67 + (abs(values.temperature) - 18) * 0.9 + values.wind_speed * 0.16 - values.ocean_temperature * 2 + values.ocean_current * 2.5))
    score = ice * 0.7 + values.wind_speed * 0.7 + values.ocean_current * 8
    risk = "HIGH" if score >= 90 else "MEDIUM" if score >= 55 else "LOW"
    action = {"LOW": "Proceed on the recommended corridor and continue routine monitoring.", "MEDIUM": "Proceed with caution and monitor iceberg zones.", "HIGH": "Hold course changes and request a fresh operational assessment."}[risk]
    return {"sea_ice": round(ice), "risk": risk, "iceberg_count": max(3, min(18, round(5 + values.wind_speed / 8 + values.ocean_current * 1.5))), "action": action, "updated_at": now(), "data_status": "SYNTHETIC / SIMULATION DATA"}

@app.get("/api/health")
def health():
    return {"status": "online", "mode": "synthetic", "updated_at": now()}

@app.get("/api/sea-ice")
def sea_ice():
    return {"current": 68, "historical_average": 61, "anomaly": 7, "trend": "rising", "forecast": [68, 71, 75, 78, 80], "data_status": "SYNTHETIC / SIMULATION DATA"}

@app.get("/api/weather")
def weather():
    return {"temperature": -18, "wind_speed": 24, "wind_direction": "SW", "pressure": 986, "precipitation": 0.4, "wave_height": 1.8, "storm_risk": 34, "data_status": "SYNTHETIC / SIMULATION DATA"}

@app.get("/api/ocean")
def ocean():
    return {"current_speed": 1.2, "current_direction": "ESE", "sea_surface_temperature": -1.5, "data_status": "SYNTHETIC / SIMULATION DATA"}

@app.get("/api/icebergs")
def icebergs():
    return {"icebergs": ICEBERGS, "data_status": "SYNTHETIC / SIMULATION DATA", "updated_at": now()}

@app.get("/api/icebergs/{iceberg_id}")
def iceberg_detail(iceberg_id: str):
    item = next((item for item in ICEBERGS if item["iceberg_id"] == iceberg_id), None)
    if not item:
        raise HTTPException(404, "Iceberg not found")
    return item

@app.get("/api/icebergs/{iceberg_id}/trajectory")
def trajectory(iceberg_id: str):
    item = next((item for item in ICEBERGS if item["iceberg_id"] == iceberg_id), None)
    if not item:
        raise HTTPException(404, "Iceberg not found")
    return {"iceberg_id": iceberg_id, "points": [{"hours": hours, "latitude": item["latitude"] - hours * 0.012, "longitude": item["longitude"] + hours * 0.025, "probability": max(0.2, 0.92 - hours / 200)} for hours in (0, 24, 48, 72, 96, 120)], "model": "Transparent vector prototype", "data_status": "SYNTHETIC / SIMULATION DATA"}

@app.get("/api/vessels")
def vessels():
    return {"vessels": [{"vessel_id": "POLAR-EXPLORER", "name": "POLAR EXPLORER", "latitude": -70.2, "longitude": 25.4, "speed": 12.4, "heading": 146, "fuel": 68, "ais": "SIMULATED"}], "updated_at": now()}

@app.post("/api/predict")
def predict(values: Environment):
    return prediction(values)

@app.get("/api/risk")
def risk():
    return {"score": 72, "level": "HIGH", "breakdown": {"sea_ice": 29, "iceberg": 20, "weather": 13, "vessel": 10}, "explanation": ["lower ice concentration on safety-first route", "avoids TL3 iceberg zone", "safer for vessel draught", "acceptable fuel increase"]}

@app.get("/api/routes")
def routes():
    return {"routes": [{"name": "DIRECT", "eta": "14 days", "distance": 520, "fuel": 1110, "risk": "HIGH", "recommendation": "Not advised"}, {"name": "MODERATE DEVIATION", "eta": "16.5 days", "distance": 556, "fuel": 1280, "risk": "MEDIUM", "recommendation": "Acceptable"}, {"name": "SAFETY-FIRST", "eta": "19 days", "distance": 610, "fuel": 1420, "risk": "LOW", "recommendation": "Recommended"}, {"name": "DYNAMIC AI", "eta": "Variable", "distance": 568, "fuel": 1240, "risk": "ADAPTIVE", "recommendation": "AI optimized"}]}

@app.post("/api/routes/optimize")
def optimize(values: RouteRequest):
    return {"recommended_route": "SAFETY-FIRST" if values.risk_tolerance == "LOW" else "DYNAMIC AI", "old_risk": 76, "new_risk": 28, "eta": "17.2 days", "explanation": ["avoids TL3 iceberg zone", "lower cumulative ice exposure", "weather conditions are more favorable"]}

@app.post("/api/routes/reroute")
def reroute():
    return {"status": "ready_for_operator_approval", "old_risk": 76, "new_risk": 28, "time_to_intersection": "9 hours"}

@app.get("/api/alerts")
def alerts():
    return {"alerts": [{"severity": "RED", "type": "ICEBERG INTERSECTION", "timestamp": now(), "description": "Predicted intersection with vessel route in 9 hours.", "recommended_action": "Reroute 32 km east."}, {"severity": "AMBER", "type": "SEA ICE", "timestamp": now(), "description": "Ice concentration increasing 18 km ahead.", "recommended_action": "Reduce operational speed."}]}

@app.post("/api/simulation/start")
def simulation_start():
    return {"simulation_id": "SIM-2026-09-11-001", "status": "running", "data_status": "SYNTHETIC / SIMULATION DATA"}

@app.post("/api/simulation/step")
def simulation_step():
    return {"step": 1, "vessel_moved": True, "risk": 72, "alert_triggered": True, "updated_at": now()}

@app.get("/api/analytics")
def analytics():
    return {"sea_ice_trend": [58, 61, 64, 68, 71], "iceberg_count": [4, 6, 5, 7, 7], "average_risk": [42, 48, 55, 66, 72], "route_fuel": [1110, 1280, 1420, 1240], "data_status": "SYNTHETIC / SIMULATION DATA"}
