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

@prod_router.get("/{item}")
def prod_page(request: Request, item: str):
    prods = db_manager.products.find({"_id": ObjectId(item)})
    t_prod = None

    for product in prods:
        t_prod = product

    return templates.TemplateResponse(
            request=request, name='product.html', context={'product': t_prod}
    )
