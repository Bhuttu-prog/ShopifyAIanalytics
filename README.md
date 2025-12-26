# Shopify AI Analytics Application

An AI-powered analytics application that connects to Shopify stores, reads customer/order/inventory data, and allows users to ask natural-language questions. The system translates these questions into ShopifyQL queries, fetches data from Shopify, and returns answers in simple, business-friendly language.

## Architecture Overview

The application consists of two main services:

1. **Rails API (Backend Gateway)**: Handles authentication, validation, and routes requests to the Python AI service
2. **Python AI Service (LLM-Powered Agent)**: Processes natural language questions, generates ShopifyQL queries, and formats responses

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       │ HTTP Request
       ▼
┌─────────────────────┐
│   Rails API         │
│   (Port 3000)       │
│                     │
│  - OAuth            │
│  - Validation       │
│  - Request Logging  │
└──────┬──────────────┘
       │
       │ HTTP Request
       ▼
┌─────────────────────┐
│  Python AI Service  │
│  (Port 8000)        │
│                     │
│  - Intent Analysis  │
│  - Query Generation │
│  - Data Processing  │
│  - Response Format  │
└──────┬──────────────┘
       │
       │ Shopify API
       ▼
┌─────────────────────┐
│   Shopify Store     │
└─────────────────────┘
```

## Agentic Workflow

The Python AI service implements an agentic workflow with the following steps:

1. **Intent Understanding**: Uses LLM to classify the question type (inventory, sales, customers, products)
2. **Query Planning**: Determines which Shopify data sources are needed
3. **Query Generation**: Generates appropriate ShopifyQL queries using LLM
4. **Query Execution**: Executes queries against Shopify APIs
5. **Data Processing**: Calculates insights from raw data
6. **Response Formatting**: Converts technical metrics into business-friendly language using LLM

## Setup Instructions

### Prerequisites

- Ruby 3.2.0+
- Rails 7.1+
- Python 3.9+
- PostgreSQL (optional, for production)
- OpenAI API key
- Shopify API credentials

### Rails API Setup

1. Navigate to the Rails API directory:
```bash
cd rails-api
```

2. Install dependencies:
```bash
bundle install
```

3. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```
SHOPIFY_API_KEY=your_shopify_api_key
SHOPIFY_API_SECRET=your_shopify_api_secret
PYTHON_AI_SERVICE_URL=http://localhost:8000
PYTHON_SERVICE_API_KEY=default-key
```

4. Set up database (if using):
```bash
rails db:create
rails db:migrate
```

5. Start the Rails server:
```bash
rails server
```

The API will be available at `http://localhost:3000`

### Python AI Service Setup

1. Navigate to the Python service directory:
```bash
cd python-ai-service
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4
SHOPIFY_ACCESS_TOKEN=your_shopify_access_token
API_KEY=default-key
```

5. Start the Python service:
```bash
uvicorn main:app --reload --port 8000
```

The service will be available at `http://localhost:8000`

## API Endpoints

### Rails API Endpoints

#### POST /api/v1/questions

Submit a natural language question about your Shopify store.

**Request:**
```json
{
  "store_id": "example-store.myshopify.com",
  "question": "How much inventory should I reorder for next week?"
}
```

**Response:**
```json
{
  "answer": "Based on the last 30 days, you sell around 10 units per day. You should reorder at least 70 units to avoid stockouts next week.",
  "confidence": "medium",
  "query_used": "FROM inventory_levels WHERE...",
  "metadata": {
    "data_type": "inventory",
    "records_analyzed": 15,
    "intent": {
      "intent_type": "inventory",
      "time_period": "next week",
      "confidence": "medium"
    }
  }
}
```

#### GET /api/v1/shopify/oauth

Initiate Shopify OAuth flow.

**Request:**
```
GET /api/v1/shopify/oauth?shop=example-store.myshopify.com
```

**Response:**
```json
{
  "oauth_url": "https://example-store.myshopify.com/admin/oauth/authorize?..."
}
```

#### GET /api/v1/shopify/callback

OAuth callback endpoint (handled by Shopify).

#### GET /api/v1/health

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "service": "Shopify Analytics API"
}
```

### Python AI Service Endpoints

#### POST /api/v1/analyze

Process a question and return AI-generated insights.

**Headers:**
```
X-API-Key: default-key
Content-Type: application/json
```

**Request:**
```json
{
  "question": "What were my top 5 selling products last week?",
  "store_id": "example-store.myshopify.com"
}
```

**Response:**
```json
{
  "answer": "Based on the last 7 days, your top 5 selling products were Product A (45 units), Product B (32 units)...",
  "confidence": "high",
  "query_used": "FROM orders WHERE created_at >= '2024-01-01'...",
  "metadata": {
    "data_type": "sales",
    "records_analyzed": 45,
    "intent": {...}
  }
}
```

## Example Questions

The system can handle various types of questions:

- **Inventory**: "How many units of Product X will I need next month?"
- **Inventory**: "Which products are likely to go out of stock in 7 days?"
- **Sales**: "What were my top 5 selling products last week?"
- **Sales**: "How much revenue did I make last month?"
- **Inventory**: "How much inventory should I reorder based on last 30 days sales?"
- **Customers**: "Which customers placed repeat orders in the last 90 days?"

## Agent Design

### Intent Classification

The agent classifies questions into categories:
- `inventory`: Questions about stock levels, reordering, availability
- `sales`: Questions about revenue, orders, product performance
- `customers`: Questions about customer behavior, repeat purchases
- `products`: Questions about product information
- `general`: Other analytics questions

### Query Generation

The agent generates ShopifyQL queries based on:
- Question intent
- Time period mentioned
- Specific products mentioned
- Metrics requested

### Response Formatting

The agent converts raw Shopify data into:
- Simple, business-friendly language
- Actionable insights
- Recommendations when appropriate
- Confidence levels (high, medium, low)

## Error Handling

The system includes comprehensive error handling:

- **Validation Errors**: Missing required parameters
- **Authentication Errors**: Invalid API keys or Shopify tokens
- **Service Errors**: Python service unavailable
- **Data Errors**: Empty or invalid Shopify responses
- **LLM Errors**: Fallback responses when LLM fails

## Security Considerations

- API key authentication between Rails and Python services
- Shopify OAuth for secure store access
- HMAC verification for Shopify webhooks (implemented in `ShopifyOAuthService`)
- Environment variables for sensitive credentials
- CORS configuration for API access

## Testing

### Test Rails API

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

### Test Python Service

```bash
# Health check
curl http://localhost:8000/health

# Analyze a question
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: default-key" \
  -d '{
    "question": "What were my top 5 selling products last week?",
    "store_id": "example-store.myshopify.com"
  }'
```

## Project Structure

```
CafeNostalgia/
├── rails-api/
│   ├── app/
│   │   ├── controllers/
│   │   │   └── api/v1/
│   │   │       ├── questions_controller.rb
│   │   │       ├── shopify_controller.rb
│   │   │       └── health_controller.rb
│   │   └── services/
│   │       ├── ai_service_client.rb
│   │       └── shopify_oauth_service.rb
│   ├── config/
│   └── Gemfile
├── python-ai-service/
│   ├── app/
│   │   ├── agent.py
│   │   ├── query_generator.py
│   │   ├── shopify_client.py
│   │   └── response_formatter.py
│   ├── main.py
│   └── requirements.txt
└── README.md
```

## Future Enhancements (Bonus Features)

- [ ] Caching Shopify responses for improved performance
- [ ] Conversation memory for follow-up questions
- [ ] Query validation layer for ShopifyQL syntax
- [ ] Metrics dashboard UI
- [ ] Retry & fallback logic in agent
- [ ] Support for Shopify GraphQL Analytics API
- [ ] Real-time inventory projections
- [ ] Email/Slack notifications for insights

## Troubleshooting

### Rails API Issues

- **Port already in use**: Change `PORT` in `.env` or kill the process using port 3000
- **Database connection errors**: Ensure PostgreSQL is running and credentials are correct
- **Python service connection errors**: Verify `PYTHON_AI_SERVICE_URL` is correct and service is running

### Python Service Issues

- **OpenAI API errors**: Verify `OPENAI_API_KEY` is set and valid
- **Shopify API errors**: Ensure `SHOPIFY_ACCESS_TOKEN` is valid and has required scopes
- **Import errors**: Ensure virtual environment is activated and dependencies are installed

## License

This project is created for the Shopify AI Analytics Assignment.

## Author

Built according to the specifications in the assignment document.

