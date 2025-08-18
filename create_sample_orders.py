"""
Test script to add sample orders data to the database
Run this script to populate the orders collection with sample data for testing
"""

from datetime import datetime, timedelta
from pymongo import MongoClient
import random

def create_sample_orders():
    # Connect to MongoDB
    client = MongoClient("localhost", 27017)
    db = client['EWebStore']
    orders_collection = db['orders']
    
    # Sample order data
    sample_orders = [
        {
            "order_id": "ORD-ABC12345",
            "user_id": "sample_user_id_1",  # Replace with actual user ID
            "order_date": datetime.now() - timedelta(days=5),
            "status": "Delivered",
            "total": 2599.99,
            "tracking_number": "TRK1234567890",
            "estimated_delivery": datetime.now() - timedelta(days=1),
            "order_items": [
                {
                    "name": "Gaming Laptop",
                    "product_img": "/static/laptop.jpg",
                    "price": 1999.99,
                    "quantity": 1,
                    "description": "High-performance gaming laptop with RTX graphics"
                },
                {
                    "name": "Wireless Gaming Mouse",
                    "product_img": "/static/mouse.jpg", 
                    "price": 299.99,
                    "quantity": 2,
                    "description": "Precision wireless gaming mouse with RGB lighting"
                }
            ],
            "shipping_address": {
                "name": "John Doe",
                "email": "john@example.com"
            },
            "payment_status": "Paid",
            "created_at": datetime.now() - timedelta(days=5),
            "updated_at": datetime.now() - timedelta(days=1)
        },
        {
            "order_id": "ORD-XYZ98765",
            "user_id": "sample_user_id_1",
            "order_date": datetime.now() - timedelta(days=3),
            "status": "In Transit",
            "total": 1299.50,
            "tracking_number": "TRK9876543210",
            "estimated_delivery": datetime.now() + timedelta(days=2),
            "order_items": [
                {
                    "name": "Mechanical Keyboard",
                    "product_img": "/static/keyboard.jpg",
                    "price": 899.50,
                    "quantity": 1,
                    "description": "RGB mechanical keyboard with blue switches"
                },
                {
                    "name": "USB-C Hub",
                    "product_img": "/static/hub.jpg",
                    "price": 400.00,
                    "quantity": 1,
                    "description": "Multi-port USB-C hub with 4K HDMI output"
                }
            ],
            "shipping_address": {
                "name": "John Doe",
                "email": "john@example.com"
            },
            "payment_status": "Paid",
            "created_at": datetime.now() - timedelta(days=3),
            "updated_at": datetime.now() - timedelta(days=1)
        },
        {
            "order_id": "ORD-DEF54321",
            "user_id": "sample_user_id_1",
            "order_date": datetime.now() - timedelta(days=1),
            "status": "Processing",
            "total": 799.99,
            "tracking_number": "TRK5432167890",
            "estimated_delivery": datetime.now() + timedelta(days=5),
            "order_items": [
                {
                    "name": "Wireless Headphones",
                    "product_img": "/static/headphones.jpg",
                    "price": 799.99,
                    "quantity": 1,
                    "description": "Premium noise-canceling wireless headphones"
                }
            ],
            "shipping_address": {
                "name": "John Doe",
                "email": "john@example.com"
            },
            "payment_status": "Paid",
            "created_at": datetime.now() - timedelta(days=1),
            "updated_at": datetime.now()
        }
    ]
    
    # Clear existing sample orders (optional)
    # orders_collection.delete_many({"user_id": "sample_user_id_1"})
    
    # Insert sample orders
    result = orders_collection.insert_many(sample_orders)
    print(f"Inserted {len(result.inserted_ids)} sample orders")
    
    print("Sample orders created successfully!")
    print("To view these orders, use user_id: 'sample_user_id_1'")
    print("\nOrders created:")
    for order in sample_orders:
        print(f"- {order['order_id']}: {order['status']} - ₹{order['total']}")

if __name__ == "__main__":
    create_sample_orders()