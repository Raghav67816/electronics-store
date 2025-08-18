from bson import ObjectId
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from utils import DBManager


prod_router = APIRouter(prefix="/products")
templates = Jinja2Templates(directory="templates")

db_manager = DBManager()

def init_prod_col(prod_col_: DBManager):
    prod_col = prod_col_
    print("Product collection setup complete.")

@prod_router.get("/")
def prod_home(request: Request):
    idToken = request.cookies.get("idToken")
    products = db_manager.get_all_products()

    if idToken != "" or idToken != None:
        is_logged_in = False

        if request.cookies.get("refreshToken") is None:
            is_logged_in = False
        else:
            is_logged_in = True
    
    return templates.TemplateResponse(
        request=request, name='home.html', context={'isLoggedIn': is_logged_in, 'products': products}
    )

@prod_router.get("/view/{_id}")
def prod_page(request: Request, _id: str):
    prods = db_manager.products.find({"_id": ObjectId(_id)})
    t_prod = None
    is_in_cart = False

    for product in prods:
        t_prod = product

    cart_prods = db_manager.users.find_one({'uid': request.cookies.get('uid')})
    if cart_prods == None:
        is_in_cart = False

    else:
        cart_prods = cart_prods['cart']
        for prod in cart_prods:
            if prod['_id'] == ObjectId(_id):
                is_in_cart = True
            else:
                is_in_cart = False

    return templates.TemplateResponse(
            request=request, name='product.html', context={'product': t_prod, 'alreadyInCart': is_in_cart}
    )

@prod_router.get("/checkout")
def checkout(request: Request):
    return templates.TemplateResponse(
        request=request, name='checkout.html'
    )
