from typing import Annotated
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

# import routers
from auth import auth_router
from cart import cart_router
from product import prod_router
from orders import orders_router


"""
problem statement
Your teams will have to prepare a shopping website or application for an electronic company
Include items like laptops, mouse, keyboards, headsets, controllers, and other accessories
in your catalogue. Include all features that you deem necessary for your project.

Home 
Product Details
Cart
Login/Signup
CheckOut
Privacy Policy
Order Tracking

Admin Panel to add products
"""

# setup main app
app = FastAPI()
app.include_router(auth_router)
app.include_router(prod_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# redirect "/" to "/products"
@app.get("/")
def home(request: Request):
    return RedirectResponse(url='/products')

@app.get("/logout")
def logout(request: Request):
    """Logout route for the main app"""
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key='token')
    response.delete_cookie(key='expiresIn') 
    response.delete_cookie(key='refreshToken')
    response.delete_cookie(key='uid')
    return response
