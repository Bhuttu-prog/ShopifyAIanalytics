"""
Formats raw Shopify data into business-friendly explanations
"""
import os
from typing import Dict, Any
from openai import OpenAI

class ResponseFormatter:
    """
    Converts technical data into simple, layman-friendly language
    """
    
    def __init__(self, llm_client: OpenAI):
        self.llm_client = llm_client
    
    async def format_response(
        self,
        question: str,
        intent: Dict[str, Any],
        data: Dict[str, Any],
        query: str
    ) -> Dict[str, Any]:
        """
        Format the response into business-friendly language
        """
        data_type = data.get("type", "general")
        raw_data = data.get("data", [])
        
        # Calculate insights based on data type
        insights = self._calculate_insights(data_type, raw_data, intent)
        
        # Use LLM to format into natural language (with fallback)
        try:
            formatted_answer = await self._generate_answer(question, insights, data_type, intent)
        except:
            # If LLM fails, use fallback
            formatted_answer = self._generate_fallback_answer(insights, data_type, question)
        
        confidence = intent.get("confidence", "medium")
        
        return {
            "answer": formatted_answer,
            "confidence": confidence,
            "query_used": query,
            "metadata": {
                "data_type": data_type,
                "records_analyzed": len(raw_data),
                "intent": intent
            }
        }
    
    def _calculate_insights(
        self,
        data_type: str,
        raw_data: list,
        intent: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate business insights from raw data
        """
        insights = {}
        
        if data_type == "sales" and raw_data:
            total_revenue = sum(float(order.get("total_price", 0)) for order in raw_data)
            total_orders = len(raw_data)
            avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
            
            # Calculate product sales
            product_sales = {}
            for order in raw_data:
                for line_item in order.get("line_items", []):
                    product_title = line_item.get("title", "Unknown")
                    quantity = int(line_item.get("quantity", 0))
                    if product_title in product_sales:
                        product_sales[product_title] += quantity
                    else:
                        product_sales[product_title] = quantity
            
            top_products = sorted(
                product_sales.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            insights = {
                "total_revenue": total_revenue,
                "total_orders": total_orders,
                "avg_order_value": avg_order_value,
                "top_products": top_products,
                "time_period": intent.get("time_period", "specified period")
            }
            
        elif data_type == "inventory" and raw_data:
            total_available = sum(int(level.get("available", 0)) for level in raw_data)
            total_incoming = sum(int(level.get("incoming", 0)) for level in raw_data)
            total_committed = sum(int(level.get("committed", 0)) for level in raw_data)
            
            insights = {
                "total_available": total_available,
                "total_incoming": total_incoming,
                "total_committed": total_committed,
                "net_available": total_available - total_committed + total_incoming,
                "product_count": len(raw_data)
            }
            
        elif data_type == "customers" and raw_data:
            total_customers = len(raw_data)
            # Find repeat customers (orders_count > 1)
            repeat_customers = [c for c in raw_data if c.get("orders_count", 0) > 1]
            repeat_customers_sorted = sorted(
                repeat_customers,
                key=lambda x: x.get("orders_count", 0),
                reverse=True
            )
            
            insights = {
                "total_customers": total_customers,
                "repeat_customers_count": len(repeat_customers),
                "repeat_customers": repeat_customers_sorted[:5]  # Top 5 repeat customers
            }
            
        else:
            insights = {
                "message": "Data retrieved but analysis needed",
                "record_count": len(raw_data)
            }
        
        return insights
    
    async def _generate_answer(
        self,
        question: str,
        insights: Dict[str, Any],
        data_type: str,
        intent: Dict[str, Any]
    ) -> str:
        """
        Use LLM to generate a natural language answer
        """
        prompt = f"""Based on the following question and data insights, provide a clear, business-friendly answer.

Original Question: "{question}"

Data Insights:
{self._format_insights_for_llm(insights, data_type)}

Provide a concise, helpful answer (2-3 sentences) that directly addresses the question. 
Use simple language that a business owner would understand. 
If the data suggests a recommendation, include it."""

        try:
            response = self.llm_client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4"),
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful business analytics assistant. Provide clear, actionable insights in simple language."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Fallback to template-based response
            return self._generate_fallback_answer(insights, data_type, question)
    
    def _format_insights_for_llm(self, insights: Dict[str, Any], data_type: str) -> str:
        """
        Format insights dictionary into readable text for LLM
        """
        if data_type == "sales":
            return f"""
            Total Revenue: ${insights.get('total_revenue', 0):.2f}
            Total Orders: {insights.get('total_orders', 0)}
            Average Order Value: ${insights.get('avg_order_value', 0):.2f}
            Top Products: {', '.join([f'{p[0]} ({p[1]} units)' for p in insights.get('top_products', [])])}
            Time Period: {insights.get('time_period', 'N/A')}
            """
        elif data_type == "inventory":
            return f"""
            Total Available Units: {insights.get('total_available', 0)}
            Incoming Units: {insights.get('total_incoming', 0)}
            Committed Units: {insights.get('total_committed', 0)}
            Net Available: {insights.get('net_available', 0)}
            Products Tracked: {insights.get('product_count', 0)}
            """
        elif data_type == "customers":
            repeat_info = ""
            if insights.get('repeat_customers'):
                repeat_list = ", ".join([
                    f"{c.get('first_name', '')} {c.get('last_name', '')} ({c.get('orders_count', 0)} orders)"
                    for c in insights.get('repeat_customers', [])[:3]
                ])
                repeat_info = f"\nRepeat Customers: {repeat_list}"
            return f"""
            Total Customers: {insights.get('total_customers', 0)}
            Repeat Customers: {insights.get('repeat_customers_count', 0)}{repeat_info}
            """
        else:
            return str(insights)
    
    def _generate_fallback_answer(
        self,
        insights: Dict[str, Any],
        data_type: str,
        question: str
    ) -> str:
        """
        Generate a template-based answer if LLM fails
        """
        if data_type == "sales":
            revenue = insights.get("total_revenue", 0)
            orders = insights.get("total_orders", 0)
            avg_order = insights.get("avg_order_value", 0)
            top_products = insights.get("top_products", [])
            
            answer = f"Based on your sales data, you generated ${revenue:.2f} in revenue from {orders} orders, with an average order value of ${avg_order:.2f}."
            
            if top_products and ("top" in question.lower() or "selling" in question.lower() or "best" in question.lower()):
                product_list = ", ".join([f"{name} ({qty} units)" for name, qty in top_products[:5]])
                answer += f" Your top selling products were: {product_list}."
            
            return answer
        
        elif data_type == "inventory":
            available = insights.get("total_available", 0)
            incoming = insights.get("total_incoming", 0)
            committed = insights.get("total_committed", 0)
            net = insights.get("net_available", 0)
            product_count = insights.get("product_count", 0)
            
            answer = f"Your inventory currently shows {available} available units across {product_count} products."
            if incoming > 0:
                answer += f" You have {incoming} units incoming."
            if committed > 0:
                answer += f" {committed} units are committed to orders."
            answer += f" Your net available inventory is {net} units."
            
            # Add recommendation for reordering
            if "reorder" in question.lower() or "need" in question.lower():
                if "week" in question.lower():
                    # Estimate based on current inventory
                    daily_usage = available / 30 if available > 0 else 5
                    recommended = max(int(daily_usage * 7), 20)
                    answer += f" Based on current inventory levels, you should reorder approximately {recommended} units for next week to maintain adequate stock."
                elif "month" in question.lower():
                    daily_usage = available / 30 if available > 0 else 5
                    recommended = max(int(daily_usage * 30), 50)
                    answer += f" Based on current inventory levels, you should reorder approximately {recommended} units for next month to maintain adequate stock."
            
            return answer
        
        elif data_type == "customers":
            total = insights.get("total_customers", 0)
            repeat_count = insights.get("repeat_customers_count", 0)
            repeat_customers = insights.get("repeat_customers", [])
            
            if "repeat" in question.lower():
                answer = f"You have {repeat_count} repeat customers out of {total} total customers."
                if repeat_customers:
                    top_repeat = repeat_customers[:3]
                    names = ", ".join([f"{c.get('first_name', '')} {c.get('last_name', '')} ({c.get('orders_count', 0)} orders)" for c in top_repeat])
                    answer += f" Your top repeat customers are: {names}."
                return answer
            else:
                return f"Your store has {total} customers in the system."
        
        else:
            return "I've retrieved the data, but need more context to provide a specific answer. Please try rephrasing your question."

