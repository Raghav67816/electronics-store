from datetime import datetime, timedelta
from bson import ObjectId
from utils import DBManager
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import random
import string

orders_router = APIRouter(prefix="/orders")
templates = Jinja2Templates(directory="templates")

db_manager = DBManager()

def generate_order_id():
    """Generate a unique order ID"""
    return 'ORD-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def generate_tracking_number():
    """Generate a tracking number"""
    return 'TRK' + ''.join(random.choices(string.digits, k=10))

@orders_router.get("/")
def view_orders(request: Request, demo: str = None, status: str = None):
    """View all orders for the logged-in user"""
    uid = request.cookies.get('uid')
    
    # Demo mode for testing
    if demo == "true":
        uid = "sample_user_id_1"
    elif not uid:
        return RedirectResponse(url='/auth/login')
    
    # Get user's orders
    orders_query = {"user_id": uid}
    
    # Apply status filter if provided
    if status and status != "All Orders":
        orders_query["status"] = status
    
    orders = list(db_manager.orders.find(orders_query).sort("order_date", -1))
    
    # Convert ObjectId to string for template rendering
    for order in orders:
        order['_id'] = str(order['_id'])
        if 'order_items' in order:
            for item in order['order_items']:
                if '_id' in item:
                    item['_id'] = str(item['_id'])
    
    # Check if user is logged in for header
    isLoggedIn = bool(uid)
    
    return templates.TemplateResponse(
        request=request, 
        name='orders.html', 
        context={
            'orders': orders, 
            'isLoggedIn': isLoggedIn,
            'current_filter': status or 'All Orders'
        }
    )

@orders_router.post("/")
def handle_post_redirects(request: Request):
    """Handle POST requests that get redirected to orders root"""
    # This handles cases where cancel/other actions get redirected here
    return RedirectResponse(url='/orders', status_code=302)

@orders_router.post("/create")
def create_order(request: Request):
    """Create a new order from cart items"""
    uid = request.cookies.get('uid')
    if not uid:
        return RedirectResponse(url='/auth/login')
    
    # Get user's cart
    query = {"uid": uid}
    user_data = db_manager.users.find_one(query)
    
    if not user_data or not user_data.get('cart'):
        return RedirectResponse(url='/cart')
    
    cart_items = user_data['cart']
    
    # Calculate total
    total = sum(item.get('price', 0) for item in cart_items)
    
    # Create order document
    order = {
        "order_id": generate_order_id(),
        "user_id": uid,
        "order_date": datetime.now(),
        "status": "Processing",
        "total": total,
        "tracking_number": generate_tracking_number(),
        "estimated_delivery": datetime.now() + timedelta(days=random.randint(3, 7)),
        "order_items": cart_items.copy(),
        "shipping_address": {
            "name": user_data.get('name', ''),
            "email": user_data.get('email', ''),
            # Add more address fields as needed
        },
        "payment_status": "Paid",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    # Insert order into orders collection
    db_manager.orders.insert_one(order)
    
    # Clear user's cart
    update = {"$set": {"cart": []}}
    db_manager.users.update_one(query, update)
    
    return RedirectResponse(url='/orders', status_code=302)

@orders_router.get("/{order_id}")
def view_order_details(request: Request, order_id: str):
    """View details of a specific order"""
    uid = request.cookies.get('uid')
    if not uid:
        return RedirectResponse(url='/auth/login')
    
    # Find the order
    order = db_manager.orders.find_one({
        "order_id": order_id,
        "user_id": uid
    })
    
    if not order:
        return RedirectResponse(url='/orders')
    
    # Convert ObjectId to string
    order['_id'] = str(order['_id'])
    if 'order_items' in order:
        for item in order['order_items']:
            if '_id' in item:
                item['_id'] = str(item['_id'])
    
    isLoggedIn = bool(uid)
    
    return templates.TemplateResponse(
        request=request,
        name='order_details.html',
        context={'order': order, 'isLoggedIn': isLoggedIn}
    )

@orders_router.post("/cancel/{order_id}")
def cancel_order_alt(request: Request, order_id: str):
    """Alternative cancel order route to avoid redirect issues"""
    return cancel_order(request, order_id)

@orders_router.post("/{order_id}/cancel")
def cancel_order(request: Request, order_id: str):
    """Cancel an order"""
    uid = request.cookies.get('uid')
    if not uid:
        return RedirectResponse(url='/auth/login')
    
    # Update order status
    query = {"order_id": order_id, "user_id": uid}
    update = {
        "$set": {
            "status": "Cancelled",
            "updated_at": datetime.now()
        }
    }
    
    result = db_manager.orders.update_one(query, update)
    
    return RedirectResponse(url='/orders', status_code=302)

@orders_router.get("/track/{order_id}")
def track_order(request: Request, order_id: str):
    """Track an order"""
    uid = request.cookies.get('uid')
    if not uid:
        return RedirectResponse(url='/auth/login')
    
    # Find the order
    order = db_manager.orders.find_one({
        "order_id": order_id,
        "user_id": uid
    })
    
    if not order:
        return RedirectResponse(url='/orders')
    
    # Convert ObjectId to string
    order['_id'] = str(order['_id'])
    
    isLoggedIn = bool(uid)
    
    return templates.TemplateResponse(
        request=request,
        name='track_order.html',
        context={'order': order, 'isLoggedIn': isLoggedIn}
    )

# Admin functions (optional)
@orders_router.get("/admin/all")
def admin_view_all_orders(request: Request):
    """Admin view to see all orders (implement proper admin authentication)"""
    # TODO: Add admin authentication check
    
    orders = list(db_manager.orders.find().sort("order_date", -1))
    
    # Convert ObjectId to string
    for order in orders:
        order['_id'] = str(order['_id'])
        if 'order_items' in order:
            for item in order['order_items']:
                if '_id' in item:
                    item['_id'] = str(item['_id'])
    
    return templates.TemplateResponse(
        request=request,
        name='admin_orders.html',
        context={'orders': orders, 'isLoggedIn': True}
    )

@orders_router.post("/admin/{order_id}/status")
def admin_update_order_status(request: Request, order_id: str, status: str = Form(...)):
    """Admin function to update order status"""
    # TODO: Add admin authentication check
    
    query = {"order_id": order_id}
    update = {
        "$set": {
            "status": status,
            "updated_at": datetime.now()
        }
    }
    
    result = db_manager.orders.update_one(query, update)
    
    return RedirectResponse(url='/orders/admin/all')