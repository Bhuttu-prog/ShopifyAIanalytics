# Python AI Service

FastAPI service that processes natural language questions and generates Shopify analytics insights.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Update `.env` with your credentials:
- `OPENAI_API_KEY`: Your OpenAI API key
- `SHOPIFY_ACCESS_TOKEN`: Shopify access token (obtained via OAuth)
- `API_KEY`: API key for service authentication

4. Run the service:
```bash
uvicorn main:app --reload --port 8000
```

## API Endpoints

### POST /api/v1/analyze

Processes a natural language question and returns insights.

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
  "answer": "Based on the last 7 days, your top 5 selling products were...",
  "confidence": "high",
  "query_used": "FROM orders...",
  "metadata": {
    "data_type": "sales",
    "records_analyzed": 45,
    "intent": {...}
  }
}
```

## Architecture

The service uses an agentic workflow:

1. **Intent Understanding**: Classifies the question type
2. **Query Generation**: Creates ShopifyQL queries
3. **Data Execution**: Fetches data from Shopify APIs
4. **Response Formatting**: Converts data into business-friendly language

