"""
AI Agent that processes natural language questions and generates ShopifyQL queries
"""
import os
from typing import Dict, Any
from openai import OpenAI
from app.shopify_client import ShopifyClient
from app.query_generator import QueryGenerator
from app.response_formatter import ResponseFormatter

class AnalyticsAgent:
    """
    Main agent orchestrating the workflow:
    1. Understand intent
    2. Plan data requirements
    3. Generate ShopifyQL
    4. Execute query
    5. Format response
    """
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY", "")
        self.llm_client = OpenAI(api_key=api_key) if api_key else None
        self.shopify_client = ShopifyClient()
        self.query_generator = QueryGenerator(self.llm_client) if self.llm_client else None
        self.response_formatter = ResponseFormatter(self.llm_client) if self.llm_client else None
    
    async def process_question(self, question: str, store_id: str) -> Dict[str, Any]:
        """
        Main processing pipeline for user questions
        """
        try:
            # Step 1: Understand intent and classify question
            if self.llm_client:
                intent = await self._understand_intent(question)
            else:
                # Fallback intent without LLM
                intent = self._simple_intent_classification(question)
            
            # Step 2: Generate ShopifyQL query
            if self.query_generator:
                query = await self.query_generator.generate_query(question, intent)
            else:
                query = "FROM orders SELECT * LIMIT 10"
            
            # Step 3: Execute query against Shopify
            data = await self.shopify_client.execute_query(store_id, query, intent)
            
            # Step 4: Format response in business-friendly language
            if self.response_formatter:
                formatted_response = await self.response_formatter.format_response(
                    question, intent, data, query
                )
            else:
                formatted_response = self._simple_response_format(question, intent, data, query)
            
            # Pass question to formatter for better fallback answers
            if hasattr(formatted_response, 'get') and formatted_response.get('answer'):
                # Ensure question is available in metadata for fallback
                if 'metadata' in formatted_response:
                    formatted_response['metadata']['original_question'] = question
            
            return formatted_response
            
        except Exception as e:
            # Fallback response on error
            return {
                "answer": f"I encountered an error processing your question: {str(e)}. Please try rephrasing or contact support.",
                "confidence": "low",
                "query_used": None,
                "metadata": {"error": str(e)}
            }
    
    async def _understand_intent(self, question: str) -> Dict[str, Any]:
        """
        Use LLM to understand user intent and classify the question
        """
        prompt = f"""Analyze the following question about Shopify store analytics and classify it.

Question: "{question}"

Return a JSON object with:
- intent_type: one of ["inventory", "sales", "customers", "products", "general"]
- time_period: extracted time period (e.g., "last 7 days", "next month", "last 30 days") or null
- metrics: list of metrics mentioned (e.g., ["units", "revenue", "orders"])
- product_mentioned: product name if mentioned, or null
- confidence: "high", "medium", or "low"

Example response:
{{
  "intent_type": "inventory",
  "time_period": "next month",
  "metrics": ["units"],
  "product_mentioned": "Product X",
  "confidence": "high"
}}

Only return the JSON object, no additional text."""

        try:
            response = self.llm_client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4"),
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing business questions and extracting intent. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            import json
            intent_data = json.loads(response.choices[0].message.content)
            return intent_data
            
        except Exception as e:
            # Default intent if LLM fails
            return {
                "intent_type": "general",
                "time_period": None,
                "metrics": [],
                "product_mentioned": None,
                "confidence": "low"
            }
    
    def _simple_intent_classification(self, question: str) -> Dict[str, Any]:
        """
        Simple rule-based intent classification when LLM is not available
        """
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["inventory", "stock", "reorder", "units", "available"]):
            intent_type = "inventory"
        elif any(word in question_lower for word in ["sales", "revenue", "selling", "top", "products"]):
            intent_type = "sales"
        elif any(word in question_lower for word in ["customer", "repeat", "orders"]):
            intent_type = "customers"
        else:
            intent_type = "general"
        
        # Extract time period
        time_period = None
        if "last week" in question_lower or "past week" in question_lower:
            time_period = "last week"
        elif "last month" in question_lower or "past month" in question_lower:
            time_period = "last month"
        elif "next week" in question_lower:
            time_period = "next week"
        elif "next month" in question_lower:
            time_period = "next month"
        elif "90 days" in question_lower or "last 90" in question_lower:
            time_period = "last 90 days"
        elif "30 days" in question_lower or "last 30" in question_lower:
            time_period = "last 30 days"
        elif "7 days" in question_lower or "last 7" in question_lower:
            time_period = "last 7 days"
        
        return {
            "intent_type": intent_type,
            "time_period": time_period,
            "metrics": [],
            "product_mentioned": None,
            "confidence": "medium"
        }
    
    def _simple_response_format(
        self,
        question: str,
        intent: Dict[str, Any],
        data: Dict[str, Any],
        query: str
    ) -> Dict[str, Any]:
        """
        Simple response formatting when LLM is not available
        Use the response formatter's fallback method
        """
        # Use response formatter even if LLM is not available
        from app.response_formatter import ResponseFormatter
        formatter = ResponseFormatter(None)  # No LLM client
        
        # Calculate insights
        data_type = data.get("type", "general")
        raw_data = data.get("data", [])
        insights = formatter._calculate_insights(data_type, raw_data, intent)
        
        # Generate fallback answer
        answer = formatter._generate_fallback_answer(insights, data_type, question)
        
        return {
            "answer": answer,
            "confidence": intent.get("confidence", "medium"),
            "query_used": query,
            "metadata": {
                "data_type": data_type,
                "records_analyzed": len(raw_data),
                "intent": intent
            }
        }

