#!/bin/bash

echo "Stopping Shopify AI Analytics Application..."
echo ""

# Stop web server
pkill -f "http.server 8080" && echo "✅ Stopped web interface"

# Stop Rails API
pkill -f "rackup config.ru" && echo "✅ Stopped Rails API"

# Stop Python service
pkill -f "uvicorn main:app" && echo "✅ Stopped Python AI Service"

echo ""
echo "All services stopped."

