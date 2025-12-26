from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

from app.agent import AnalyticsAgent
from app.shopify_client import ShopifyClient

load_dotenv()

app = FastAPI(title="Shopify Analytics AI Service", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class AnalyzeRequest(BaseModel):
    question: str
    store_id: str

class AnalyzeResponse(BaseModel):
    answer: str
    confidence: str
    query_used: Optional[str] = None
    metadata: Optional[dict] = None

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Shopify Analytics AI Service"}

@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
async def analyze_question(
    request: AnalyzeRequest,
    x_api_key: Optional[str] = Header(None)
):
    """
    Main endpoint that receives natural language questions and returns AI-powered insights
    """
    # Simple API key validation (can be enhanced)
    expected_key = os.getenv("API_KEY", "default-key")
    if x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    try:
        agent = AnalyticsAgent()
        result = await agent.process_question(request.question, request.store_id)
        
        return AnalyzeResponse(
            answer=result["answer"],
            confidence=result["confidence"],
            query_used=result.get("query_used"),
            metadata=result.get("metadata", {})
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

