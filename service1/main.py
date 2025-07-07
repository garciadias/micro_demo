import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Microservice 1",
    description="First FastAPI service using Python 3.11 and FastAPI 0.104.1",
    version="1.0.0"
)

# Configuration
SERVICE_NAME = os.getenv("SERVICE_NAME", "service1")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")
OTHER_SERVICE_URL = os.getenv("OTHER_SERVICE_URL", "http://service2:8002")
SHARED_DATA_PATH = Path("/app/shared_data")

# Ensure shared data directory exists
SHARED_DATA_PATH.mkdir(exist_ok=True)


# Define Pydantic models for data interfaces
class ServiceSettings(BaseModel):
    service_name: str
    service_version: str
    python_version: str
    fastapi_version: str
    timestamp: str
    message: str


class CreateDataRequest(BaseModel):
    filename: str
    message: str


def get_service_settings(message: str = "") -> Dict[str, Any]:
    """Get current service settings"""
    return {
        "service_name": SERVICE_NAME,
        "service_version": SERVICE_VERSION,
        "python_version": "3.11",
        "fastapi_version": "0.104.1",
        "timestamp": datetime.now().isoformat(),
        "message": message
    }


async def save_to_json_file(filename: str, data: Dict[str, Any]) -> None:
    """Save data to a JSON file in the shared directory"""
    file_path = SHARED_DATA_PATH / filename

    # Load existing data if file exists
    existing_data = []
    if file_path.exists():
        try:
            with open(file_path, 'r') as f:
                existing_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            existing_data = []

    # Append new data
    existing_data.append(data)

    # Save back to file
    with open(file_path, 'w') as f:
        json.dump(existing_data, f, indent=2)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "status": "running",
        "python_version": "3.11",
        "fastapi_version": "0.104.1"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": SERVICE_NAME}


@app.get("/settings")
async def get_settings():
    """Get service settings"""
    return get_service_settings()


@app.post("/create-data")
async def create_data(request: CreateDataRequest):
    """
    Main endpoint that creates JSON data and calls the second service
    """
    try:
        # Create settings for this service
        service1_settings = get_service_settings(request.message)

        # Save service1 settings to JSON file
        await save_to_json_file(request.filename, service1_settings)

        # Call service2 to add its settings to the same file
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{OTHER_SERVICE_URL}/add-settings",
                    json={
                        "filename": request.filename,
                        "message": f"Called from {SERVICE_NAME}"
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                service2_response = response.json()
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=503,
                    detail=f"Failed to communicate with service2: {str(e)}"
                )
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"Service2 returned error: {e.response.text}"
                )

        # Read the final file content
        file_path = SHARED_DATA_PATH / request.filename
        with open(file_path, 'r') as f:
            final_content = json.load(f)

        return {
            "success": True,
            "message": f"Data created successfully by {SERVICE_NAME}",
            "filename": request.filename,
            "service1_settings": service1_settings,
            "service2_response": service2_response,
            "final_file_content": final_content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/files")
async def list_files():
    """List all JSON files in the shared directory"""
    try:
        json_files = [f.name for f in SHARED_DATA_PATH.glob("*.json")]
        return {"files": json_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")


@app.get("/files/{filename}")
async def get_file_content(filename: str):
    """Get content of a specific JSON file"""
    try:
        file_path = SHARED_DATA_PATH / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        with open(file_path, 'r') as f:
            content = json.load(f)

        return {"filename": filename, "content": content}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
