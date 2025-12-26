"""
Generates ShopifyQL queries from natural language questions
"""
import os
from typing import Dict, Any
from openai import OpenAI

class QueryGenerator:
    """
    Converts natural language questions into ShopifyQL queries
    """
    
    def __init__(self, llm_client: OpenAI):
        self.llm_client = llm_client
    
    async def generate_query(self, question: str, intent: Dict[str, Any]) -> str:
        """
        Generate ShopifyQL query based on question and intent
        """
        prompt = self._build_prompt(question, intent)
        
        try:
            response = self.llm_client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4"),
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert at generating ShopifyQL queries. 
                        ShopifyQL is Shopify's analytics query language. 
                        Common tables: orders, products, inventory_levels, customers.
                        Always return ONLY the ShopifyQL query, no explanations."""
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=500
            )
            
            query = response.choices[0].message.content.strip()
            # Remove markdown code blocks if present
            if query.startswith("```"):
                query = query.split("```")[1]
                if query.startswith("sql") or query.startswith("shopifyql"):
                    query = query.split("\n", 1)[1]
            
            return query
            
        except Exception as e:
            # Fallback to a basic query
            return self._generate_fallback_query(intent)
    
    def _build_prompt(self, question: str, intent: Dict[str, Any]) -> str:
        """
        Build prompt for LLM to generate ShopifyQL
        """
        intent_type = intent.get("intent_type", "general")
        time_period = intent.get("time_period")
        product = intent.get("product_mentioned")
        
        examples = {
            "inventory": """
            Example: "How many units of Product X will I need next month?"
            ShopifyQL:
            FROM inventory_levels
            WHERE product_title = 'Product X'
            SELECT available, incoming, committed
            """,
            "sales": """
            Example: "What were my top 5 selling products last week?"
            ShopifyQL:
            FROM orders
            WHERE created_at >= '2024-01-01' AND created_at < '2024-01-08'
            GROUP BY product_title
            SELECT product_title, SUM(quantity) as total_sold
            ORDER BY total_sold DESC
            LIMIT 5
            """,
            "customers": """
            Example: "Which customers placed repeat orders in the last 90 days?"
            ShopifyQL:
            FROM orders
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 90 DAY)
            GROUP BY customer_email
            HAVING COUNT(*) > 1
            SELECT customer_email, COUNT(*) as order_count
            """
        }
        
        prompt = f"""Generate a ShopifyQL query for the following question:

Question: "{question}"

Intent: {intent_type}
Time Period: {time_period or "not specified"}
Product: {product or "not specified"}

{examples.get(intent_type, examples["sales"])}

Generate the ShopifyQL query for this specific question:"""
        
        return prompt
    
    def _generate_fallback_query(self, intent: Dict[str, Any]) -> str:
        """
        Generate a basic fallback query if LLM fails
        """
        intent_type = intent.get("intent_type", "general")
        
        if intent_type == "inventory":
            return """
            FROM inventory_levels
            SELECT available, incoming, committed
            LIMIT 10
            """
        elif intent_type == "sales":
            return """
            FROM orders
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            SELECT SUM(total_price) as total_revenue, COUNT(*) as order_count
            """
        elif intent_type == "customers":
            return """
            FROM customers
            SELECT COUNT(*) as total_customers
            """
        else:
            return """
            FROM orders
            SELECT COUNT(*) as total_orders
            LIMIT 1
            """

