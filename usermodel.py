from mongoengine import Document, StringField, DateTimeField, BooleanField
from pydantic import BaseModel


class UserModel(Document):
    en_login_id = StringField(required= False)
    name = StringField(required = True)
    email = StringField(required = True)
    gender = StringField(require = True)
    password = StringField(required = True)
    
class UserCreate(BaseModel):
    name: str
    email: str
    gender: str
    password: str
    
class UserCreateById(BaseModel):
    en_login_id: str
    name: str
    email: str
    gender: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str
    
class UserLoginId(BaseModel):
    en_login_id: str