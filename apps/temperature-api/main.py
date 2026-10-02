"""temperature-api: заглушка датчиков температуры для монолита smart_home.

Эндпоинты:
  GET /temperature?location=<комната>&sensorId=<id>  — по локации (или ID в query)
  GET /temperature/{sensor_id}                       — по ID датчика (так монолит
                                                       читает показания в Get All Sensors)
  GET /health                                        — проверка работоспособности

На каждый запрос возвращается случайное значение температуры.
"""

import os
import random
from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="temperature-api")

LOCATION_BY_SENSOR_ID = {
    "1": "Living Room",
    "2": "Bedroom",
    "3": "Kitchen",
}
SENSOR_ID_BY_LOCATION = {loc: sid for sid, loc in LOCATION_BY_SENSOR_ID.items()}


def resolve(location: str, sensor_id: str) -> tuple[str, str]:
    """Дополняет пустую локацию по ID датчика и пустой ID — по локации."""
    if not location:
        location = LOCATION_BY_SENSOR_ID.get(sensor_id, "Unknown")
    if not sensor_id:
        sensor_id = SENSOR_ID_BY_LOCATION.get(location, "0")
    return location, sensor_id


def reading(location: str, sensor_id: str) -> dict:
    """Случайное показание в формате, который ожидает монолит (TemperatureResponse)."""
    location, sensor_id = resolve(location, sensor_id)
    return {
        "value": round(random.uniform(15.0, 30.0), 1),
        "unit": "°C",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "location": location,
        "status": "active",
        "sensor_id": sensor_id,
        "sensor_type": "temperature",
        "description": f"Temperature sensor in {location}",
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/temperature")
def temperature_by_location(location: str = "", sensorId: str = "") -> dict:
    return reading(location, sensorId)


@app.get("/temperature/{sensor_id}")
def temperature_by_sensor_id(sensor_id: str) -> dict:
    return reading("", sensor_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8081")))
