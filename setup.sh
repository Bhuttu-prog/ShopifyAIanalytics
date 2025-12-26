#!/bin/bash

echo "Setting up Shopify AI Analytics Application..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Ruby is installed
if ! command -v ruby &> /dev/null; then
    echo -e "${YELLOW}Ruby is not installed. Please install Ruby 3.2.0+ first.${NC}"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python 3 is not installed. Please install Python 3.9+ first.${NC}"
    exit 1
fi

echo -e "${GREEN}Setting up Rails API...${NC}"
cd rails-api

# Install Ruby dependencies
if [ -f "Gemfile" ]; then
    echo "Installing Ruby gems..."
    bundle install
else
    echo -e "${YELLOW}Gemfile not found in rails-api directory${NC}"
fi

# Set up environment file
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo -e "${YELLOW}Please update rails-api/.env with your credentials${NC}"
fi

cd ..

echo ""
echo -e "${GREEN}Setting up Python AI Service...${NC}"
cd python-ai-service

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Set up environment file
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo -e "${YELLOW}Please update python-ai-service/.env with your credentials${NC}"
fi

deactivate
cd ..

echo ""
echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Update rails-api/.env with your Shopify API credentials"
echo "2. Update python-ai-service/.env with your OpenAI API key"
echo "3. Start Rails API: cd rails-api && rails server"
echo "4. Start Python service: cd python-ai-service && source venv/bin/activate && uvicorn main:app --reload"
echo ""
echo "See README.md for detailed instructions."

