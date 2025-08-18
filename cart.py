from bson import ObjectId
from utils import DBManager
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

cart_router = APIRouter(prefix="/cart")
templates = Jinja2Templates(directory="templates")

db_manager = DBManager()

@cart_router.get("/")
def cart(request: Request):
	query = {"uid": request.cookies.get('uid')}
	cart_prods = db_manager.users.find_one(query)['cart']

	for prod in cart_prods:
		prod['_id'] = str(prod['_id'])

	print(cart_prods)

	return templates.TemplateResponse(
		request=request, name='cart.html', context={'products': cart_prods}
	)

@cart_router.get("/add_item/{_id}")
def add_to_cart(request: Request, _id: str):
	query = {"uid": request.cookies.get('uid')}
	prod_query = db_manager.products.find_one({"_id": ObjectId(_id)})

	cart_prods = db_manager.users.find_one(query)['cart']
	cart_prods.append(prod_query)
	
	prod_query.pop("reviews")

	update = {"$set": {"cart": cart_prods}}
	db_manager.users.update_one(query, update)

	return RedirectResponse(
		url=f'/products/{_id}'
	)

@cart_router.get("/del_item/{_id}")
def delete_item(request: Request, _id: str):
	query = {'uid': request.cookies.get('uid')}
	cart_prods = db_manager.users.find_one(query)['cart']
	t_prod = None

	for prod in cart_prods:
		if prod['_id'] == ObjectId(_id):
			t_prod = prod

	print(t_prod)

	cart_prods.remove(t_prod)
	update = {"$set": {"cart": cart_prods}}
	db_manager.users.update_one(query, update)

	return RedirectResponse(url='/cart')
