from tortoise import Tortoise, fields
from tortoise.models import Model
from passlib.context import CryptContext
from pydantic import BaseModel




class User_s(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    password = fields.TextField()
    created_at=fields.DatetimeField(auto_now_add=True)
    updated_at=fields.DatetimeField(auto_now=True)


    def __str__(self) :
        return self.name
 

   
    

    





class createUser(BaseModel):
    name:str
    password:str
   
    






