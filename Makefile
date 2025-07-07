.PHONY: build up down restart logs test clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  make build    - Build the Docker images"
	@echo "  make up       - Start the services"
	@echo "  make down     - Stop the services"
	@echo "  make restart  - Restart the services"
	@echo "  make logs     - Show logs from all services"
	@echo "  make logs1    - Show logs from service1"
	@echo "  make logs2    - Show logs from service2"
	@echo "  make test     - Run the test script"
	@echo "  make clean    - Stop services and remove containers/volumes"
	@echo "  make rebuild  - Clean build and restart"

# Build the images
build:
	docker compose build

# Start the services
up:
	docker compose up -d

# Stop the services
down:
	docker compose down

# Restart the services
restart: down up

# Show logs
logs:
	docker compose logs -f

logs1:
	docker compose logs -f service1

logs2:
	docker compose logs -f service2

# Run tests
test:
	@echo "Waiting for services to start..."
	@sleep 5
	./test_services.sh

# Clean up everything
clean:
	docker compose down -v --remove-orphans
	docker system prune -f

# Rebuild everything
rebuild: clean build up

# Quick start (build and run)
start: build up
	@echo "Services are starting..."
	@echo "Service 1: http://localhost:8001"
	@echo "Service 2: http://localhost:8002"
	@echo "Run 'make test' to test the services"

debug:
	@echo "Debugging mode will create both services but will not start the fastapi service."
	docker compose -f docker compose.debug.yml build
	docker compose -f docker compose.debug.yml up -d