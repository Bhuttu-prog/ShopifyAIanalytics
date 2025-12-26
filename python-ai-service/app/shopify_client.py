"""
Shopify API client for executing queries and fetching data
"""
import os
import httpx
from typing import Dict, Any, Optional

class ShopifyClient:
    """
    Handles communication with Shopify APIs
    """
    
    def __init__(self):
        self.base_url = "https://{shop}.myshopify.com/admin/api/2024-01"
    
    async def execute_query(self, store_id: str, query: str, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute ShopifyQL query or use REST API based on intent
        """
        # For this implementation, we'll use REST API as ShopifyQL requires GraphQL
        # In production, you'd use Shopify's GraphQL Analytics API
        
        intent_type = intent.get("intent_type", "general")
        
        if intent_type == "inventory":
            return await self._fetch_inventory_data(store_id, intent)
        elif intent_type == "sales":
            return await self._fetch_sales_data(store_id, intent)
        elif intent_type == "customers":
            return await self._fetch_customer_data(store_id, intent)
        elif intent_type == "products":
            return await self._fetch_product_data(store_id, intent)
        else:
            return await self._fetch_general_data(store_id)
    
    async def _fetch_inventory_data(self, store_id: str, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch inventory data from Shopify
        """
        access_token = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
        product_name = intent.get("product_mentioned")
        
        # Return mock inventory data
        mock_inventory = [
            {
                "inventory_item_id": 1,
                "location_id": 1,
                "available": 45,
                "incoming": 50,
                "committed": 5,
                "product_title": "Coffee Beans Premium"
            },
            {
                "inventory_item_id": 2,
                "location_id": 1,
                "available": 23,
                "incoming": 0,
                "committed": 8,
                "product_title": "Vintage Mug Set"
            },
            {
                "inventory_item_id": 3,
                "location_id": 1,
                "available": 12,
                "incoming": 20,
                "committed": 3,
                "product_title": "Artisan Tea Collection"
            },
            {
                "inventory_item_id": 4,
                "location_id": 1,
                "available": 8,
                "incoming": 0,
                "committed": 2,
                "product_title": "Espresso Machine"
            },
            {
                "inventory_item_id": 5,
                "location_id": 1,
                "available": 34,
                "incoming": 15,
                "committed": 6,
                "product_title": "Coffee Grinder"
            },
            {
                "inventory_item_id": 6,
                "location_id": 1,
                "available": 67,
                "incoming": 0,
                "committed": 12,
                "product_title": "French Press"
            },
            {
                "inventory_item_id": 7,
                "location_id": 1,
                "available": 5,
                "incoming": 0,
                "committed": 1,
                "product_title": "Milk Frother"
            }
        ]
        
        # Filter by product if specified
        if product_name:
            filtered = [inv for inv in mock_inventory if product_name.lower() in inv.get("product_title", "").lower()]
            if filtered:
                mock_inventory = filtered
        
        return {
            "type": "inventory",
            "data": mock_inventory,
            "count": len(mock_inventory)
        }
    
    async def _fetch_sales_data(self, store_id: str, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch sales/order data from Shopify
        """
        access_token = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
        time_period = intent.get("time_period", "last 30 days")
        
        # Return mock data for demo purposes
        mock_orders = [
            {
                "id": 1,
                "order_number": 1001,
                "total_price": "125.50",
                "created_at": "2024-12-20T10:30:00Z",
                "line_items": [
                    {"title": "Coffee Beans Premium", "quantity": 2, "price": "45.00"},
                    {"title": "Vintage Mug Set", "quantity": 1, "price": "35.50"}
                ],
                "customer": {"email": "john.doe@example.com", "first_name": "John", "last_name": "Doe"}
            },
            {
                "id": 2,
                "order_number": 1002,
                "total_price": "89.99",
                "created_at": "2024-12-19T14:20:00Z",
                "line_items": [
                    {"title": "Artisan Tea Collection", "quantity": 1, "price": "89.99"}
                ],
                "customer": {"email": "jane.smith@example.com", "first_name": "Jane", "last_name": "Smith"}
            },
            {
                "id": 3,
                "order_number": 1003,
                "total_price": "156.75",
                "created_at": "2024-12-18T09:15:00Z",
                "line_items": [
                    {"title": "Coffee Beans Premium", "quantity": 3, "price": "45.00"},
                    {"title": "Espresso Machine", "quantity": 1, "price": "21.75"}
                ],
                "customer": {"email": "john.doe@example.com", "first_name": "John", "last_name": "Doe"}
            },
            {
                "id": 4,
                "order_number": 1004,
                "total_price": "67.50",
                "created_at": "2024-12-17T16:45:00Z",
                "line_items": [
                    {"title": "Vintage Mug Set", "quantity": 2, "price": "35.50"}
                ],
                "customer": {"email": "mike.johnson@example.com", "first_name": "Mike", "last_name": "Johnson"}
            },
            {
                "id": 5,
                "order_number": 1005,
                "total_price": "234.99",
                "created_at": "2024-12-16T11:30:00Z",
                "line_items": [
                    {"title": "Coffee Beans Premium", "quantity": 4, "price": "45.00"},
                    {"title": "Coffee Grinder", "quantity": 1, "price": "54.99"}
                ],
                "customer": {"email": "sarah.williams@example.com", "first_name": "Sarah", "last_name": "Williams"}
            },
            {
                "id": 6,
                "order_number": 1006,
                "total_price": "45.00",
                "created_at": "2024-12-15T13:20:00Z",
                "line_items": [
                    {"title": "Coffee Beans Premium", "quantity": 1, "price": "45.00"}
                ],
                "customer": {"email": "john.doe@example.com", "first_name": "John", "last_name": "Doe"}
            },
            {
                "id": 7,
                "order_number": 1007,
                "total_price": "124.99",
                "created_at": "2024-12-14T10:10:00Z",
                "line_items": [
                    {"title": "Artisan Tea Collection", "quantity": 1, "price": "89.99"},
                    {"title": "Vintage Mug Set", "quantity": 1, "price": "35.50"}
                ],
                "customer": {"email": "jane.smith@example.com", "first_name": "Jane", "last_name": "Smith"}
            },
            {
                "id": 8,
                "order_number": 1008,
                "total_price": "178.50",
                "created_at": "2024-12-13T15:30:00Z",
                "line_items": [
                    {"title": "Espresso Machine", "quantity": 2, "price": "21.75"},
                    {"title": "Coffee Beans Premium", "quantity": 3, "price": "45.00"}
                ],
                "customer": {"email": "david.brown@example.com", "first_name": "David", "last_name": "Brown"}
            }
        ]
        
        return {
            "type": "sales",
            "data": mock_orders,
            "count": len(mock_orders),
            "time_period": time_period
        }
    
    async def _fetch_customer_data(self, store_id: str, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch customer data from Shopify
        """
        access_token = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
        
        # Return mock customer data with order counts for repeat customer analysis
        mock_customers = [
            {
                "id": 1,
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "orders_count": 3,
                "total_spent": "227.50",
                "created_at": "2024-11-01T10:00:00Z"
            },
            {
                "id": 2,
                "email": "jane.smith@example.com",
                "first_name": "Jane",
                "last_name": "Smith",
                "orders_count": 2,
                "total_spent": "214.98",
                "created_at": "2024-11-15T14:00:00Z"
            },
            {
                "id": 3,
                "email": "mike.johnson@example.com",
                "first_name": "Mike",
                "last_name": "Johnson",
                "orders_count": 1,
                "total_spent": "67.50",
                "created_at": "2024-12-01T09:00:00Z"
            },
            {
                "id": 4,
                "email": "sarah.williams@example.com",
                "first_name": "Sarah",
                "last_name": "Williams",
                "orders_count": 1,
                "total_spent": "234.99",
                "created_at": "2024-12-05T11:00:00Z"
            },
            {
                "id": 5,
                "email": "david.brown@example.com",
                "first_name": "David",
                "last_name": "Brown",
                "orders_count": 1,
                "total_spent": "178.50",
                "created_at": "2024-12-10T15:00:00Z"
            },
            {
                "id": 6,
                "email": "emily.davis@example.com",
                "first_name": "Emily",
                "last_name": "Davis",
                "orders_count": 4,
                "total_spent": "456.75",
                "created_at": "2024-10-20T12:00:00Z"
            },
            {
                "id": 7,
                "email": "robert.wilson@example.com",
                "first_name": "Robert",
                "last_name": "Wilson",
                "orders_count": 2,
                "total_spent": "189.99",
                "created_at": "2024-11-25T16:00:00Z"
            }
        ]
        
        return {
            "type": "customers",
            "data": mock_customers,
            "count": len(mock_customers)
        }
    
    async def _fetch_product_data(self, store_id: str, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch product data from Shopify
        """
        access_token = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
        
        # Return mock product data
        mock_products = [
            {
                "id": 1,
                "title": "Coffee Beans Premium",
                "vendor": "Cafe Nostalgia",
                "product_type": "Coffee",
                "variants": [{"price": "45.00", "inventory_quantity": 45}],
                "created_at": "2024-01-15T10:00:00Z"
            },
            {
                "id": 2,
                "title": "Vintage Mug Set",
                "vendor": "Cafe Nostalgia",
                "product_type": "Accessories",
                "variants": [{"price": "35.50", "inventory_quantity": 23}],
                "created_at": "2024-02-20T10:00:00Z"
            },
            {
                "id": 3,
                "title": "Artisan Tea Collection",
                "vendor": "Cafe Nostalgia",
                "product_type": "Tea",
                "variants": [{"price": "89.99", "inventory_quantity": 12}],
                "created_at": "2024-03-10T10:00:00Z"
            },
            {
                "id": 4,
                "title": "Espresso Machine",
                "vendor": "Cafe Nostalgia",
                "product_type": "Equipment",
                "variants": [{"price": "21.75", "inventory_quantity": 8}],
                "created_at": "2024-04-05T10:00:00Z"
            },
            {
                "id": 5,
                "title": "Coffee Grinder",
                "vendor": "Cafe Nostalgia",
                "product_type": "Equipment",
                "variants": [{"price": "54.99", "inventory_quantity": 34}],
                "created_at": "2024-05-12T10:00:00Z"
            }
        ]
        
        return {
            "type": "products",
            "data": mock_products,
            "count": len(mock_products)
        }
    
    async def _fetch_general_data(self, store_id: str) -> Dict[str, Any]:
        """
        Fetch general store data
        """
        return {
            "type": "general",
            "data": [],
            "message": "General query - specific implementation needed"
        }

