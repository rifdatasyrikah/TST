from typing import List
from pydantic import BaseModel, Field, EmailStr

class UserSchema(BaseModel):
    nim : int = Field(default=None)
    email : EmailStr = Field(default=None)
    password : str = Field(default=None)
    class Config:
        the_schema = {
            "user_demo" :{ 
                "nim" : "18220099",
                "email" : "rifda.tasyrikah@gmail.com",
                "password" : "12345678"
            }
        }

class UserLoginSchema(BaseModel):
    email : EmailStr = Field(default=None)
    password : str = Field(default=None)
    class Config:
        the_schema = {
            "user_demo" :{ 
                "email" : "rifda.tasyrikah@gmail.com",
                "password" : "12345678"
            }
        }