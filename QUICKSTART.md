# Quick Start Guide

Get the Shopify AI Analytics Application running in 5 minutes.

## Prerequisites Check

```bash
# Check Ruby version (need 3.2.0+)
ruby -v

# Check Python version (need 3.9+)
python3 --version

# Check if PostgreSQL is installed (optional)
psql --version
```

## Step 1: Run Setup Script

```bash
./setup.sh
```

This will:
- Install Ruby dependencies
- Create Python virtual environment
- Install Python dependencies
- Create .env files from examples

## Step 2: Configure Environment Variables

### Rails API Configuration

Edit `rails-api/.env`:

```bash
SHOPIFY_API_KEY=your_shopify_api_key_here
SHOPIFY_API_SECRET=your_shopify_api_secret_here
PYTHON_AI_SERVICE_URL=http://localhost:8000
PYTHON_SERVICE_API_KEY=default-key
```

### Python Service Configuration

Edit `python-ai-service/.env`:

```bash
OPENAI_API_KEY=sk-your_openai_api_key_here
OPENAI_MODEL=gpt-4
SHOPIFY_ACCESS_TOKEN=your_shopify_access_token_here
API_KEY=default-key
```

## Step 3: Start Services

### Terminal 1: Start Rails API

```bash
cd rails-api
rails server
```

You should see:
```
=> Booting Puma
=> Rails 7.1.0 application starting in development
=> Run `bin/rails server --help` for more startup options
Puma starting in single mode...
* Listening on http://127.0.0.1:3000
```

### Terminal 2: Start Python AI Service

```bash
cd python-ai-service
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Step 4: Test the Application

### Test Health Endpoints

```bash
# Test Rails API
curl http://localhost:3000/api/v1/health

# Test Python Service
curl http://localhost:8000/health
```

### Test Question Endpoint

```bash
curl -X POST http://localhost:3000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "example-store.myshopify.com",
    "question": "What were my top 5 selling products last week?"
  }'
```

## Troubleshooting

### Rails API Issues

**Problem**: `bundle install` fails
- **Solution**: Make sure Ruby 3.2.0+ is installed. Use `rbenv` or `rvm` to manage Ruby versions.

**Problem**: Port 3000 already in use
- **Solution**: Kill the process using port 3000 or change `PORT` in `.env`

**Problem**: Database connection error
- **Solution**: PostgreSQL is optional. If you see database errors, you can skip database setup for basic functionality.

### Python Service Issues

**Problem**: `pip install` fails
- **Solution**: Make sure virtual environment is activated: `source venv/bin/activate`

**Problem**: OpenAI API errors
- **Solution**: Verify your `OPENAI_API_KEY` is correct and has credits

**Problem**: Import errors
- **Solution**: Make sure you're in the virtual environment and all dependencies are installed

### Connection Issues

**Problem**: Rails can't connect to Python service
- **Solution**: 
  1. Verify Python service is running on port 8000
  2. Check `PYTHON_AI_SERVICE_URL` in `rails-api/.env`
  3. Check `API_KEY` matches in both services

## Next Steps

1. **Authenticate with Shopify**: Use the OAuth endpoint to get an access token
2. **Update Shopify Token**: Add the token to `python-ai-service/.env` as `SHOPIFY_ACCESS_TOKEN`
3. **Try Different Questions**: See `EXAMPLES.md` for more question examples
4. **Read Documentation**: Check `README.md` and `ARCHITECTURE.md` for details

## Getting Shopify Credentials

1. Go to https://partners.shopify.com
2. Create a new app
3. Get your API Key and API Secret
4. Set OAuth redirect URL to: `http://localhost:3000/api/v1/shopify/callback`
5. Request scopes: `read_orders`, `read_products`, `read_inventory`

## Getting OpenAI API Key

1. Go to https://platform.openai.com
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and add to `python-ai-service/.env`

## Development Tips

- **Hot Reload**: Both services support hot reload in development
- **Logs**: Check Rails logs in `rails-api/log/development.log`
- **Python Logs**: Check terminal output for Python service logs
- **API Testing**: Use Postman, curl, or the examples in `EXAMPLES.md`

## Production Deployment

For production deployment:

1. Set `RAILS_ENV=production` in Rails
2. Use a production-grade server (e.g., Gunicorn for Python)
3. Set up reverse proxy (Nginx)
4. Use environment variables for all secrets
5. Enable HTTPS
6. Set up monitoring and logging
7. Use a production database (PostgreSQL)

See `ARCHITECTURE.md` for more deployment details.

