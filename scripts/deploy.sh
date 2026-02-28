#!/bin/bash
set -e

echo "=== Sandbox Deployment Script ==="

if [ -f .env ]; then
    echo "Loading environment variables..."
    export $(cat .env | xargs)
else
    echo "Warning: .env file not found, using .env.example"
    cp .env.example .env
fi

echo "Building Docker image..."
docker build -t sandbox-app:latest .

echo "Starting containers..."
docker-compose up -d

echo "Deployment complete!"
docker-compose ps
