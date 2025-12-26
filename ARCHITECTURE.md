# Architecture Documentation

## System Architecture

The Shopify AI Analytics Application follows a microservices architecture with clear separation of concerns between the Rails API gateway and the Python AI service.

## Component Overview

### 1. Rails API (Backend Gateway)

**Purpose**: Acts as the entry point for all client requests, handling authentication, validation, and routing.

**Responsibilities**:
- OAuth authentication with Shopify
- Request validation and sanitization
- Request logging
- Communication with Python AI service
- Response formatting
- Error handling

**Technology Stack**:
- Ruby on Rails 7.1 (API-only mode)
- PostgreSQL (optional, for production)
- HTTParty for HTTP client communication
- JWT for token handling

**Key Files**:
- `app/controllers/api/v1/questions_controller.rb`: Main endpoint for questions
- `app/controllers/api/v1/shopify_controller.rb`: OAuth handling
- `app/services/ai_service_client.rb`: Client for Python service
- `app/services/shopify_oauth_service.rb`: Shopify OAuth logic

### 2. Python AI Service (LLM-Powered Agent)

**Purpose**: Processes natural language questions, generates queries, and formats responses.

**Responsibilities**:
- Intent understanding and classification
- ShopifyQL query generation
- Shopify API communication
- Data processing and insight calculation
- Natural language response generation

**Technology Stack**:
- FastAPI for REST API
- OpenAI GPT-4 for LLM capabilities
- httpx for async HTTP requests
- Pydantic for data validation

**Key Files**:
- `app/agent.py`: Main agent orchestrator
- `app/query_generator.py`: ShopifyQL query generation
- `app/shopify_client.py`: Shopify API client
- `app/response_formatter.py`: Response formatting

## Data Flow

```
1. Client Request
   ↓
2. Rails API (Validation & Auth)
   ↓
3. Python AI Service (Intent Analysis)
   ↓
4. Query Generation (LLM)
   ↓
5. Shopify API (Data Fetching)
   ↓
6. Data Processing (Insight Calculation)
   ↓
7. Response Formatting (LLM)
   ↓
8. Rails API (Response Formatting)
   ↓
9. Client Response
```

## Agentic Workflow Details

### Step 1: Intent Understanding

The agent uses an LLM to analyze the user's question and extract:
- **Intent Type**: inventory, sales, customers, products, general
- **Time Period**: extracted time references (e.g., "last 7 days", "next month")
- **Metrics**: what metrics are being asked about
- **Product Mentions**: specific products mentioned
- **Confidence**: how confident the classification is

**Implementation**: `app/agent.py::_understand_intent()`

### Step 2: Query Planning

Based on the intent, the agent determines:
- Which Shopify data sources to query (orders, inventory, customers, products)
- What filters to apply (time period, product filters)
- What aggregations are needed
- What fields to select

**Implementation**: `app/query_generator.py::generate_query()`

### Step 3: Query Generation

The agent uses an LLM to generate ShopifyQL queries. The LLM is provided with:
- The original question
- The classified intent
- Example queries for the intent type
- ShopifyQL syntax guidelines

**Implementation**: `app/query_generator.py::generate_query()`

### Step 4: Query Execution

The generated query is executed against Shopify APIs. The system:
- Authenticates with Shopify using OAuth tokens
- Makes appropriate REST API calls (or GraphQL for ShopifyQL)
- Handles pagination for large datasets
- Manages rate limiting

**Implementation**: `app/shopify_client.py::execute_query()`

### Step 5: Data Processing

Raw Shopify data is processed to calculate insights:
- **Sales Data**: Total revenue, order count, average order value, top products
- **Inventory Data**: Available units, incoming stock, committed inventory, net available
- **Customer Data**: Total customers, repeat customers, customer segments

**Implementation**: `app/response_formatter.py::_calculate_insights()`

### Step 6: Response Formatting

The agent uses an LLM to convert technical insights into business-friendly language:
- Summarizes key findings
- Provides actionable recommendations
- Uses simple, non-technical language
- Includes specific numbers and context

**Implementation**: `app/response_formatter.py::_generate_answer()`

## Error Handling Strategy

### Rails API Error Handling

1. **Validation Errors**: Return 400 Bad Request with error details
2. **Authentication Errors**: Return 401 Unauthorized
3. **Service Errors**: Return 503 Service Unavailable when Python service is down
4. **Internal Errors**: Return 500 with generic message, log details

### Python Service Error Handling

1. **LLM Errors**: Fallback to template-based responses
2. **Shopify API Errors**: Return error details in response
3. **Query Generation Errors**: Use fallback queries
4. **Data Processing Errors**: Return partial results with error indication

## Security Architecture

### Authentication Flow

1. **Shopify OAuth**:
   - User initiates OAuth via Rails API
   - Redirects to Shopify authorization page
   - Shopify redirects back with authorization code
   - Rails exchanges code for access token
   - Token stored securely (in production, use encrypted storage)

2. **Service-to-Service Authentication**:
   - API key authentication between Rails and Python
   - Headers: `X-API-Key`
   - Configurable via environment variables

### Data Security

- All sensitive credentials in environment variables
- No hardcoded API keys or tokens
- HTTPS in production (configured via reverse proxy)
- HMAC verification for Shopify webhooks

## Scalability Considerations

### Current Architecture

- **Stateless Services**: Both Rails and Python services are stateless
- **Horizontal Scaling**: Can run multiple instances behind load balancer
- **Database**: Optional PostgreSQL for request logging/caching

### Future Enhancements

- **Caching Layer**: Redis for Shopify API responses
- **Message Queue**: RabbitMQ/Kafka for async processing
- **Database**: Store conversation history and user preferences
- **CDN**: For static assets (if UI is added)

## Deployment Architecture

### Development

```
Rails API (localhost:3000) ←→ Python Service (localhost:8000) ←→ Shopify API
```

### Production (Recommended)

```
Load Balancer
    ↓
Rails API (Multiple Instances)
    ↓
Python Service (Multiple Instances)
    ↓
Shopify API
```

### Environment Variables

**Rails API**:
- `SHOPIFY_API_KEY`
- `SHOPIFY_API_SECRET`
- `PYTHON_AI_SERVICE_URL`
- `PYTHON_SERVICE_API_KEY`
- `DATABASE_URL` (production)

**Python Service**:
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `SHOPIFY_ACCESS_TOKEN`
- `API_KEY`

## API Design Principles

1. **RESTful**: Follow REST conventions where applicable
2. **Versioning**: API versioned via `/api/v1/` prefix
3. **Consistent Responses**: Standardized response format
4. **Error Codes**: Meaningful HTTP status codes
5. **Documentation**: OpenAPI/Swagger documentation (can be added)

## Monitoring and Logging

### Logging Strategy

- **Rails**: Log all requests, errors, and service calls
- **Python**: Log intent classifications, queries generated, API calls
- **Structured Logging**: JSON format for easy parsing
- **Log Levels**: DEBUG (development), INFO (production), ERROR (all)

### Metrics to Track

- Request latency
- LLM API call latency
- Shopify API call latency
- Error rates
- Intent classification accuracy
- Query generation success rate

## Testing Strategy

### Unit Tests

- **Rails**: Controller tests, service tests
- **Python**: Agent tests, query generator tests, formatter tests

### Integration Tests

- End-to-end request flow
- Shopify API mocking
- LLM response mocking

### Manual Testing

- Sample questions from assignment
- Error scenarios
- Edge cases

## Future Architecture Enhancements

1. **GraphQL API**: For Shopify Analytics API (more efficient than REST)
2. **WebSocket Support**: For real-time updates
3. **Caching Layer**: Redis for frequently asked questions
4. **Conversation Memory**: Store context for follow-up questions
5. **Query Validation**: Validate ShopifyQL syntax before execution
6. **Dashboard UI**: React/Vue frontend for visualization
7. **Scheduled Reports**: Background jobs for regular insights

