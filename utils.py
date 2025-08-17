from pymongo import MongoClient
from fastapi import Request

class DBManager:
    def __init__(self):

        self.client = MongoClient("localhost", 27017)
        self.db = self.client['EWebStore']

        self.products = self.db['products']        
        self.users = self.db['Users']

    # get all products (no filter)
    def get_all_products(self) -> list:
        prods = []
        for prod in self.products.find():
            prods.append(prod)
        return prods

"""
is_logged_in 

Checks if the user is logged in by using get_cookies method.
cookie exists:
    -> logged in 

if not:
    -> logged out


WARNING: USERS MUST USE LOGOUT BUTTON
"""
def is_logged_in(request: Request) -> bool:
    if request.cookies.get("refreshToken") is None:
        return False

    else:
        return True
