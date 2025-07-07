#!/bin/bash

# Test script for the microservices demo
# This script tests the communication between the two services

echo "=== Microservices Communication Test ==="
echo

# Check if services are running
echo "1. Checking if services are running..."
echo "Service 1 status:"
curl -s http://localhost:8001/health | jq .
echo "Service 2 status:"
curl -s http://localhost:8002/health | jq .
echo

# Test the main workflow
echo "2. Testing main workflow (Service 1 -> Service 2)..."
echo "Creating data via Service 1..."
curl -s -X POST "http://localhost:8001/create-data" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "test_communication.json",
    "message": "Hello from the test script!"
  }' | jq .
echo

# List files
echo "3. Listing files in shared storage..."
curl -s http://localhost:8001/files | jq .
echo

# Get file content
echo "4. Reading the created file..."
curl -s http://localhost:8001/files/test_communication.json | jq .
echo

# Test Service 2 standalone
echo "5. Testing Service 2 standalone..."
curl -s -X POST "http://localhost:8002/create-standalone" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "service2_standalone.json",
    "message": "Service 2 standalone test"
  }' | jq .
echo

# List files again
echo "6. Final file list..."
curl -s http://localhost:8002/files | jq .
echo

echo "=== Test completed ==="
