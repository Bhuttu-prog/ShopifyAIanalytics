# API Examples and Sample Requests

This document provides detailed examples of API requests and responses for the Shopify AI Analytics Application.

## Example 1: Inventory Reorder Question

### Request
```bash
curl -X POST http://localhost:3000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "example-store.myshopify.com",
    "question": "How much inventory should I reorder for next week?"
  }'
```

### Response
```json
{
  "answer": "Based on the last 30 days, you sell around 10 units per day on average. To ensure you have enough stock for next week, you should reorder at least 70 units to avoid stockouts.",
  "confidence": "medium",
  "query_used": "FROM inventory_levels WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) SELECT available, incoming, committed",
  "metadata": {
    "data_type": "inventory",
    "records_analyzed": 15,
    "intent": {
      "intent_type": "inventory",
      "time_period": "next week",
      "metrics": ["units"],
      "product_mentioned": null,
      "confidence": "medium"
    }
  }
}
```

## Example 2: Top Selling Products

### Request
```bash
curl -X POST http://localhost:3000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "example-store.myshopify.com",
    "question": "What were my top 5 selling products last week?"
  }'
```

### Response
```json
{
  "answer": "Based on the last 7 days, your top 5 selling products were: Coffee Beans Premium (45 units), Vintage Mug Set (32 units), Artisan Tea Collection (28 units), Espresso Machine (15 units), and Coffee Grinder (12 units).",
  "confidence": "high",
  "query_used": "FROM orders WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) GROUP BY product_title SELECT product_title, SUM(quantity) as total_sold ORDER BY total_sold DESC LIMIT 5",
  "metadata": {
    "data_type": "sales",
    "records_analyzed": 45,
    "intent": {
      "intent_type": "sales",
      "time_period": "last week",
      "metrics": ["quantity", "products"],
      "product_mentioned": null,
      "confidence": "high"
    }
  }
}
```

## Example 3: Stockout Prediction

### Request
```bash
curl -X POST http://localhost:3000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "example-store.myshopify.com",
    "question": "Which products are likely to go out of stock in 7 days?"
  }'
```

### Response
```json
{
  "answer": "Based on current inventory levels and recent sales velocity, the following products are at risk of going out of stock within 7 days: Coffee Beans Premium (currently 8 units, selling 2 per day), Vintage Mug Set (12 units, selling 1.5 per day), and Artisan Tea Collection (10 units, selling 1.8 per day). I recommend reordering these products immediately.",
  "confidence": "medium",
  "query_used": "FROM inventory_levels JOIN orders ON inventory_levels.product_id = orders.product_id WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) SELECT product_title, available, AVG(daily_sales) as avg_daily_sales",
  "metadata": {
    "data_type": "inventory",
    "records_analyzed": 20,
    "intent": {
      "intent_type": "inventory",
      "time_period": "7 days",
      "metrics": ["stock", "availability"],
      "product_mentioned": null,
      "confidence": "medium"
    }
  }
}
```

## Example 4: Repeat Customers

### Request
```bash
curl -X POST http://localhost:3000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "example-store.myshopify.com",
    "question": "Which customers placed repeat orders in the last 90 days?"
  }'
```

### Response
```json
{
  "answer": "In the last 90 days, you have 23 customers who placed repeat orders. The top repeat customers include: john.doe@example.com (5 orders), jane.smith@example.com (4 orders), and mike.johnson@example.com (3 orders). These customers represent your most loyal customer base.",
  "confidence": "high",
  "query_used": "FROM orders WHERE created_at >= DATE_SUB(NOW(), INTERVAL 90 DAY) GROUP BY customer_email HAVING COUNT(*) > 1 SELECT customer_email, COUNT(*) as order_count ORDER BY order_count DESC",
  "metadata": {
    "data_type": "customers",
    "records_analyzed": 23,
    "intent": {
      "intent_type": "customers",
      "time_period": "last 90 days",
      "metrics": ["orders", "repeat"],
      "product_mentioned": null,
      "confidence": "high"
    }
  }
}
```

## Example 5: Product-Specific Inventory

### Request
```bash
curl -X POST http://localhost:3000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "example-store.myshopify.com",
    "question": "How many units of Coffee Beans Premium will I need next month?"
  }'
```

### Response
```json
{
  "answer": "Based on your sales history, Coffee Beans Premium sells approximately 60 units per month. With your current inventory of 8 units and no incoming stock, you should order at least 60 units to cover next month's projected demand.",
  "confidence": "high",
  "query_used": "FROM orders WHERE product_title = 'Coffee Beans Premium' AND created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) SELECT SUM(quantity) as total_sold, AVG(quantity) as avg_daily_sales",
  "metadata": {
    "data_type": "inventory",
    "records_analyzed": 12,
    "intent": {
      "intent_type": "inventory",
      "time_period": "next month",
      "metrics": ["units"],
      "product_mentioned": "Coffee Beans Premium",
      "confidence": "high"
    }
  }
}
```

## Example 6: Error Handling - Missing Parameters

### Request
```bash
curl -X POST http://localhost:3000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "example-store.myshopify.com"
  }'
```

### Response
```json
{
  "error": "validation_error",
  "message": "Question parameter is required"
}
```

## Example 7: Error Handling - Service Unavailable

### Request
```bash
curl -X POST http://localhost:3000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "example-store.myshopify.com",
    "question": "What were my sales last month?"
  }'
```

### Response (when Python service is down)
```json
{
  "error": "service_unavailable",
  "message": "AI service is currently unavailable"
}
```

## Example 8: Shopify OAuth Flow

### Step 1: Initiate OAuth
```bash
curl "http://localhost:3000/api/v1/shopify/oauth?shop=example-store.myshopify.com"
```

### Response
```json
{
  "oauth_url": "https://example-store.myshopify.com/admin/oauth/authorize?client_id=YOUR_API_KEY&scope=read_orders,read_products,read_inventory&redirect_uri=http://localhost:3000/api/v1/shopify/callback"
}
```

### Step 2: User redirects to OAuth URL and authorizes

### Step 3: Shopify redirects to callback
```
GET /api/v1/shopify/callback?code=AUTH_CODE&shop=example-store.myshopify.com
```

### Response
```json
{
  "message": "Authentication successful",
  "store_id": "example-store.myshopify.com",
  "access_token": "shpat_xxxxxxxxxxxxx"
}
```

## Example 9: Health Check

### Request
```bash
curl http://localhost:3000/api/v1/health
```

### Response
```json
{
  "status": "ok",
  "service": "Shopify Analytics API"
}
```

## Example 10: Python Service Direct Call

### Request
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: default-key" \
  -d '{
    "question": "What was my total revenue last month?",
    "store_id": "example-store.myshopify.com"
  }'
```

### Response
```json
{
  "answer": "Your total revenue for the last month was $12,450.00 from 89 orders, with an average order value of $139.89. This represents strong performance compared to previous periods.",
  "confidence": "high",
  "query_used": "FROM orders WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) SELECT SUM(total_price) as total_revenue, COUNT(*) as order_count, AVG(total_price) as avg_order_value",
  "metadata": {
    "data_type": "sales",
    "records_analyzed": 89,
    "intent": {
      "intent_type": "sales",
      "time_period": "last month",
      "metrics": ["revenue"],
      "product_mentioned": null,
      "confidence": "high"
    }
  }
}
```

## Testing with Different Tools

### Using Postman

1. Create a new POST request to `http://localhost:3000/api/v1/questions`
2. Set headers: `Content-Type: application/json`
3. Body (raw JSON):
```json
{
  "store_id": "your-store.myshopify.com",
  "question": "Your question here"
}
```

### Using Python requests

```python
import requests

url = "http://localhost:3000/api/v1/questions"
payload = {
    "store_id": "example-store.myshopify.com",
    "question": "What were my top 5 selling products last week?"
}

response = requests.post(url, json=payload)
print(response.json())
```

### Using JavaScript fetch

```javascript
fetch('http://localhost:3000/api/v1/questions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    store_id: 'example-store.myshopify.com',
    question: 'What were my top 5 selling products last week?'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

