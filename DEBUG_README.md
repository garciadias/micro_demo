# Debug Setup Instructions

This setup allows you to debug both microservices using VS Code with Docker.

## Prerequisites

1. **VS Code Extensions**: Install the Python Debugger extension (`ms-python.debugpy`)
2. **Docker**: Ensure Docker and Docker Compose are installed

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
