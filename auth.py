import requests
from typing import Annotated
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response, RedirectResponse

from firebase_admin import initialize_app, auth
from firebase_admin.credentials import Certificate

from utils import DBManager

auth_router = APIRouter(prefix="/auth")

templates = Jinja2Templates(directory="templates")

# configure firebase
creds = Certificate("./service.json")
initialize_app(creds)

API_KEY = "AIzaSyDCiq0ZcMw4H9a3GrGtdhDm-bd64A4z1GY"

db_manager = DBManager()


@auth_router.get("/signup")
def signup(request: Request, response_class=HTMLResponse):
	return templates.TemplateResponse(
		request=request, name='signup.html'
		)


@auth_router.post("/signup")
def signup(response: Response, fullname: Annotated[str, Form()],
         email: Annotated[str, Form()],
         password: Annotated[str, Form()],
         response_class=RedirectResponse
    ):
	user = auth.create_user(
	    display_name=fullname,
	    email=email,
	    password=password
	)

	db_manager.users.insert_one(
	    {
	        "display_name": fullname,
	        "profile_img": 'https://img.icons8.com/color/48/user-female--v3.png',
	        "cart": [],
	        "reviews": [],
            "uid": auth.verify_id_token(user.idToken)['uid']
	    }
	)
	
	return RedirectResponse(
	    url="/auth/login", status_code=301
	)


@auth_router.get("/login")
def login(request: Request, response_class = HTMLResponse):
    return templates.TemplateResponse(
        request=request, name='login.html'
    )


@auth_router.post("/login")
def login(
        request: Request,
        email: Annotated[str, Form()], 
        password: Annotated[str, Form()], 
        response_class = HTMLResponse
    ):
    url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}'
    
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    res = requests.post(url, json=data)
    if res.status_code == 200:

        res_data = res.json()
        response = templates.TemplateResponse(
            request=request, name='home.html', context={"isLoggedIn": True}
        )
        user_id = str(auth.verify_id_token(res_data['idToken'], clock_skew_in_seconds=1)['uid'])
        response.set_cookie(key='token', value=res_data['idToken'])
        response.set_cookie(key='expiresIn', value=res_data['expiresIn'])
        response.set_cookie(key='refreshToken', value=res_data['refreshToken'])
        response.set_cookie(key='uid', value=user_id)

        return response

    else:
        print(res.json())
        
