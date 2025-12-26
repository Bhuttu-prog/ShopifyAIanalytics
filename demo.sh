#!/bin/bash

echo "=========================================="
echo "Shopify AI Analytics Application Demo"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Testing Python AI Service...${NC}"
echo ""

# Test 1: Health Check
echo -e "${YELLOW}1. Health Check:${NC}"
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""
echo ""

# Test 2: Top Products Question
echo -e "${YELLOW}2. Question: 'What were my top 5 selling products last week?'${NC}"
curl -s -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: default-key" \
  -d '{
    "question": "What were my top 5 selling products last week?",
    "store_id": "example-store.myshopify.com"
  }' | python3 -m json.tool
echo ""
echo ""

# Test 3: Inventory Question
echo -e "${YELLOW}3. Question: 'How much inventory should I reorder for next week?'${NC}"
curl -s -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: default-key" \
  -d '{
    "question": "How much inventory should I reorder for next week?",
    "store_id": "example-store.myshopify.com"
  }' | python3 -m json.tool
echo ""
echo ""

# Test 4: Customer Question
echo -e "${YELLOW}4. Question: 'Which customers placed repeat orders in the last 90 days?'${NC}"
curl -s -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: default-key" \
  -d '{
    "question": "Which customers placed repeat orders in the last 90 days?",
    "store_id": "example-store.myshopify.com"
  }' | python3 -m json.tool
echo ""
echo ""

echo -e "${GREEN}=========================================="
echo "Demo Complete!"
echo "==========================================${NC}"
echo ""
echo "Note: The service is running in demo mode without:"
echo "  - OpenAI API key (using rule-based classification)"
echo "  - Shopify access token (using mock data)"
echo ""
echo "To enable full functionality:"
echo "  1. Add OPENAI_API_KEY to python-ai-service/.env"
echo "  2. Add SHOPIFY_ACCESS_TOKEN to python-ai-service/.env"
echo "  3. Restart the Python service"

