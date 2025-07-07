# Microservices Demo

For a more detailed introduction to microservices, check out:

- This seminal article: [Microservices](https://martinfowler.com/articles/microservices.html).
- This microsoft guide: [Microservices Architecture](https://docs.microsoft.com/en-us/azure/architecture/microservices/).
- This comprehensive book: [Microservice APIs : Using Python, Flask, FastAPI, OpenAPI and More](https://books.google.co.uk/books/about/Microservice_APIs.html?id=5s-azgEACAAJ&redir_esc=y).
- Counter example: [Kraken Monolith](https://blog.europython.eu/kraken-technologies-how-we-organize-our-very-large-pythonmonolith/)

This project demonstrates two FastAPI services that communicate with each other and share data through a common mounted folder.

## Architecture

- **Service 1**: Python 3.11 + FastAPI 0.104.1 (Port 8001)
- **Service 2**: Python 3.9 + FastAPI 0.68.0 (Port 8002)
- **Shared Storage**: Common folder mounted in both containers
- **Communication**: HTTP requests between services

## Features

- Two independent FastAPI services with different Python and FastAPI versions
- Inter-service communication via HTTP
- Shared JSON file storage
- Docker Compose orchestration
- Health checks and status endpoints

## Quick Start

1. Build and start the services:

```bash
docker-compose up --build
```

2. Test the main workflow:

```bash
curl -X POST "http://localhost:8001/create-data" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "test_communication.json",
    "message": "Hello from the API test!"
  }'
```

## API Endpoints

### Service 1 (Port 8001)

- `GET /` - Service information
- `GET /health` - Health check
- `GET /settings` - Get service settings
- `POST /create-data` - **Main endpoint**: Creates JSON data and calls Service 2
- `GET /files` - List all JSON files
- `GET /files/{filename}` - Get specific file content

### Service 2 (Port 8002)

- `GET /` - Service information
- `GET /health` - Health check
- `GET /settings` - Get service settings
- `POST /add-settings` - Called by Service 1 to add settings
- `POST /create-standalone` - Create data independently
- `GET /files` - List all JSON files
- `GET /files/{filename}` - Get specific file content

## Workflow

1. Client calls `POST /create-data` on Service 1
2. Service 1 saves its settings to a JSON file
3. Service 1 calls Service 2's `/add-settings` endpoint
4. Service 2 appends its settings to the same JSON file
5. Service 1 returns the complete result

## Example Response

```json
{
  "success": true,
  "message": "Data created successfully by service1",
  "filename": "test_communication.json",
  "service1_settings": {
    "service_name": "service1",
    "service_version": "1.0.0",
    "python_version": "3.11",
    "fastapi_version": "0.104.1",
    "timestamp": "2025-07-06T10:30:00.123456",
    "message": "Hello from the API test!"
  },
  "service2_response": {
    "success": true,
    "message": "Settings added successfully by service2",
    "filename": "test_communication.json",
    "settings": {
      "service_name": "service2",
      "service_version": "2.0.0",
      "python_version": "3.9",
      "fastapi_version": "0.68.0",
      "timestamp": "2025-07-06T10:30:00.456789",
      "message": "Called from service1"
    }
  },
  "final_file_content": [
    {
      "service_name": "service1",
      "service_version": "1.0.0",
      "python_version": "3.11",
      "fastapi_version": "0.104.1",
      "timestamp": "2025-07-06T10:30:00.123456",
      "message": "Hello from the API test!"
    },
    {
      "service_name": "service2",
      "service_version": "2.0.0",
      "python_version": "3.9",
      "fastapi_version": "0.68.0",
      "timestamp": "2025-07-06T10:30:00.456789",
      "message": "Called from service1"
    }
  ]
}
```

## Testing Individual Services

### Service 1 Only

```bash
curl http://localhost:8001/
curl http://localhost:8001/health
curl http://localhost:8001/settings
```

### Service 2 Only

```bash
curl http://localhost:8002/
curl http://localhost:8002/health
curl http://localhost:8002/settings

# Create standalone data
curl -X POST "http://localhost:8002/create-standalone" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "service2_only.json",
    "message": "Service 2 standalone test"
  }'
```

### View Files

```bash
curl http://localhost:8001/files
curl http://localhost:8001/files/test_communication.json
```

## Docker Compose Configuration

- Both services share the `./shared_data` folder
- Services communicate through the `microservices-network`
- Service 1 depends on Service 2 to ensure proper startup order
- Environment variables configure service behavior

## Development

To run locally without Docker:

1. Set up virtual environments for each service
2. Install requirements: `pip install -r requirements.txt`
3. Run services: `uvicorn main:app --port 8001` and `uvicorn main:app --port 8002`
4. Update `OTHER_SERVICE_URL` environment variable for local development

## Debug Setup Instructions

This setup allows you to debug both microservices using VS Code with Docker.

### Prerequisites

1. **VS Code Extensions**: Install the Python Debugger extension (`ms-python.debugpy`)

## How to Debug

### 1. Start the Debug Environment

```bash
# Start both services in debug mode
docker compose -f docker-compose.debug.yml up --build
```

The services will start and wait for a debugger to attach. You'll see messages like:

- Service1: "Waiting for client to attach..."
- Service2: "Waiting for client to attach..."

### 2. Attach VS Code Debugger

1. **Open the Debug View** in VS Code (Ctrl+Shift+D)
2. **Select a debug configuration**:
   - "Debug Service1 (Docker)" - to debug only service1
   - "Debug Service2 (Docker)" - to debug only service2  
   - "Debug Both Services" - to debug both services simultaneously
3. **Click the green play button** or press F5

### 3. Set Breakpoints

- Open the Python files in VS Code (`service1/main.py`, `service2/main.py`)
- Click in the gutter next to line numbers to set breakpoints
- The debugger will pause execution when breakpoints are hit

### 4. Test the Services

Once debuggers are attached, the services will start running. You can test them:

```bash
# Test service1
curl http://localhost:8001/health

# Test service2  
curl http://localhost:8002/health

# Test communication between services
curl -X POST http://localhost:8001/create-data \
  -H "Content-Type: application/json" \
  -d '{"filename": "test.json", "message": "Debug test"}'
```

## Debug Features

- **Live code editing**: Changes to Python files are automatically reloaded
- **Breakpoints**: Set breakpoints in any Python file
- **Variable inspection**: Examine variables, call stack, and execution state
- **Step debugging**: Step through code line by line
- **Hot reload**: Code changes are reflected without rebuilding containers

## Port Mappings

| Service | Application Port | Debug Port |
|---------|------------------|------------|
| Service1| 8001            | 5678       |
| Service2| 8002            | 5679       |

## Stopping the Debug Environment

```bash
# Stop all services
docker compose -f docker-compose.debug.yml down
```

## Troubleshooting

- **"Connection refused"**: Ensure the containers are running and ports are not blocked
- **"Debugger not stopping at breakpoints"**: Check that path mappings in `.vscode/launch.json` are correct
- **"Services not starting"**: Check Docker logs with `docker compose -f docker-compose.debug.yml logs`
