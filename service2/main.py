import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import fastapi
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Microservice 2", description="Second FastAPI service using Python 3.9 and FastAPI 0.68.0", version="2.0.0"
)

# Configuration
SERVICE_NAME = os.getenv("SERVICE_NAME", "service2")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "2.0.0")
SHARED_DATA_PATH = Path("/app/shared_data")

# Ensure shared data directory exists
SHARED_DATA_PATH.mkdir(exist_ok=True)


class ServiceSettings(BaseModel):
    service_name: str
    service_version: str
    python_version: str
    fastapi_version: str
    timestamp: str
    message: str


class AddSettingsRequest(BaseModel):
    filename: str
    message: str


def get_service_settings(message: str = "") -> Dict[str, Any]:
    """Get current service settings"""
    return {
        "service_name": SERVICE_NAME,
        "service_version": SERVICE_VERSION,
        "python_version": sys.version.split(" ")[0],
        "fastapi_version": fastapi.__version__,
        "timestamp": datetime.now().isoformat(),
        "message": message,
    }


async def save_to_json_file(filename: str, data: Dict[str, Any]) -> None:
    """Save data to a JSON file in the shared directory"""
    file_path = SHARED_DATA_PATH / filename

    # Load existing data if file exists
    existing_data = []
    if file_path.exists():
        try:
            with open(file_path, "r") as f:
                existing_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            existing_data = []

    # Append new data
    existing_data.append(data)

    # Save back to file
    with open(file_path, "w") as f:
        json.dump(existing_data, f, indent=2)


@app.get("/")
async def root():
    """Root endpoint"""
    return get_service_settings("Welcome to Service 2!")


@app.post("/add-settings")
async def add_settings(request: AddSettingsRequest):
    """
    Endpoint called by service1 to add service2 settings to the JSON file
    """
    try:
        # Create settings for this service
        service2_settings = get_service_settings(request.message)

        # Save service2 settings to the same JSON file
        await save_to_json_file(request.filename, service2_settings)

        return {
            "success": True,
            "message": f"Settings added successfully by {SERVICE_NAME}",
            "filename": request.filename,
            "settings": service2_settings,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
