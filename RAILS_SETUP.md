# Rails API Setup Guide

## Current Status

The Python AI Service is **running and working** ✅

The Rails API requires Ruby version management. Here are the setup options:

## Option 1: Using rbenv (Recommended)

```bash
# Install rbenv if not already installed
brew install rbenv

# Install Ruby 3.2.0
rbenv install 3.2.0

# Set local Ruby version
cd rails-api
rbenv local 3.2.0

# Install dependencies
bundle install

# Start Rails server
rails server
```

## Option 2: Using rvm

```bash
# Install rvm if not already installed
curl -sSL https://get.rvm.io | bash -s stable

# Install Ruby 3.2.0
rvm install 3.2.0

# Use Ruby 3.2.0
rvm use 3.2.0

# Install dependencies
cd rails-api
bundle install

# Start Rails server
rails server
```

## Option 3: Using System Ruby (Current - Requires Sudo)

If you want to use the system Ruby (2.6.10), you'll need to:

1. Update the Gemfile to use Rails 6.1 (already done)
2. Run with sudo (not recommended for development):

```bash
cd rails-api
sudo bundle install
rails server
```

## Quick Test (Without Rails)

You can test the Python service directly, which is the core functionality:

```bash
# Run the demo script
./demo.sh

# Or test manually
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: default-key" \
  -d '{
    "question": "What were my top 5 selling products last week?",
    "store_id": "example-store.myshopify.com"
  }'
```

## Environment Variables

The Rails API `.env` file is already created with:
- `PYTHON_AI_SERVICE_URL=http://localhost:8000`
- `PYTHON_SERVICE_API_KEY=default-key`
- Shopify credentials (demo values)

## Once Rails is Running

Test the full stack:

```bash
# Health check
curl http://localhost:3000/api/v1/health

# Submit a question
curl -X POST http://localhost:3000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "example-store.myshopify.com",
    "question": "What were my top 5 selling products last week?"
  }'
```

## Note

The Python service is fully functional and demonstrates:
- ✅ Intent classification
- ✅ Query generation
- ✅ Response formatting
- ✅ Error handling

The Rails API adds:
- Request validation
- OAuth handling
- Service orchestration
- Additional error handling

Both services work independently, but together they provide the complete solution.

