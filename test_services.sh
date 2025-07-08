#!/bin/bash

# Test script for the microservices demo
# This script tests the communication between the two services

echo "=== Microservices Communication Test ==="
echo

# Check if services are running
echo "1. Checking if services are running..."
echo "Service 1 status:"
curl -s http://localhost:8001/ | jq .
echo "Service 2 status:"
curl -s http://localhost:8002/ | jq .
echo

# Test the main workflow
echo "2. Testing main workflow (Service 1 -> Service 2)..."
echo "Creating data via Service 1..."
curl -s -X POST "http://localhost:8001/create-data" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "test_communication.json",
    "message": "Hello from Service 1!#"
  }' | jq .
echo
