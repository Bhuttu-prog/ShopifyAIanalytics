#!/bin/bash

echo "=========================================="
echo "Starting Shopify AI Analytics Application"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

cd "$(dirname "$0")"

# Check if services are already running
if curl -s http://localhost:3000/api/v1/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Rails API is already running${NC}"
else
    echo -e "${YELLOW}Starting Rails API...${NC}"
    cd rails-api
    nohup /usr/bin/bundle exec rackup config.ru -p 3000 -o 0.0.0.0 > /tmp/rails.log 2>&1 &
    cd ..
    sleep 3
fi

if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Python AI Service is already running${NC}"
else
    echo -e "${YELLOW}Starting Python AI Service...${NC}"
    cd python-ai-service
    source venv/bin/activate
    nohup uvicorn main:app --host 0.0.0.0 --port 8000 > /tmp/python.log 2>&1 &
    cd ..
    sleep 3
fi

if curl -s http://localhost:8080/index.html > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Web Interface is already running${NC}"
else
    echo -e "${YELLOW}Starting Web Interface...${NC}"
    cd public
    nohup python3 -m http.server 8080 > /tmp/web_server.log 2>&1 &
    cd ..
    sleep 2
fi

echo ""
echo -e "${GREEN}=========================================="
echo "Application is Ready!"
echo "==========================================${NC}"
echo ""
echo "🌐 Open in your browser:"
echo -e "   ${BLUE}http://localhost:8080/index.html${NC}"
echo ""
echo "Services:"
echo "  ✅ Web Interface: http://localhost:8080"
echo "  ✅ Rails API: http://localhost:3000"
echo "  ✅ Python AI Service: http://localhost:8000"
echo ""
echo "To stop all services:"
echo "  ./STOP_APPLICATION.sh"
echo ""

# Try to open browser
if command -v open > /dev/null; then
    open http://localhost:8080/index.html
elif command -v xdg-open > /dev/null; then
    xdg-open http://localhost:8080/index.html
fi

