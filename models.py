from pydantic import BaseModel

"""
new user model

full name
email
password
"""
class User(BaseModel):
    name: str
    email: str
    passwd: str

    
