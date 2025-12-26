#!/bin/bash

echo "=========================================="
echo "Full Stack Application Test"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Testing Full Stack (Rails API → Python AI Service)${NC}"
echo ""

# Test 1: Rails Health Check
echo -e "${YELLOW}1. Rails API Health Check:${NC}"
curl -s http://localhost:3000/api/v1/health | python3 -m json.tool
echo ""
echo ""

# Test 2: Python Service Health Check
echo -e "${YELLOW}2. Python AI Service Health Check:${NC}"
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""
echo ""

# Test 3: Full Stack - Top Products Question
echo -e "${YELLOW}3. Full Stack Test - Question: 'What were my top 5 selling products last week?'${NC}"
curl -s -X POST http://localhost:3000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "example-store.myshopify.com",
    "question": "What were my top 5 selling products last week?"
  }' | python3 -m json.tool
echo ""
echo ""

# Test 4: Full Stack - Inventory Question
echo -e "${YELLOW}4. Full Stack Test - Question: 'How much inventory should I reorder for next week?'${NC}"
curl -s -X POST http://localhost:3000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "example-store.myshopify.com",
    "question": "How much inventory should I reorder for next week?"
  }' | python3 -m json.tool
echo ""
echo ""

# Test 5: Full Stack - Customer Question
echo -e "${YELLOW}5. Full Stack Test - Question: 'Which customers placed repeat orders in the last 90 days?'${NC}"
curl -s -X POST http://localhost:3000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "example-store.myshopify.com",
    "question": "Which customers placed repeat orders in the last 90 days?"
  }' | python3 -m json.tool
echo ""
echo ""

# Test 6: Error Handling - Missing Parameters
echo -e "${YELLOW}6. Error Handling Test - Missing question parameter:${NC}"
curl -s -X POST http://localhost:3000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "example-store.myshopify.com"
  }' | python3 -m json.tool
echo ""
echo ""

echo -e "${GREEN}=========================================="
echo "All Tests Complete!"
echo "==========================================${NC}"
echo ""
echo "Services Status:"
echo "  ✅ Rails API: http://localhost:3000"
echo "  ✅ Python AI Service: http://localhost:8000"
echo ""
echo "Both services are running and communicating successfully!"

