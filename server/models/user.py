from typing import List
from pydantic import BaseModel, EmailStr, Field
import uuid
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from server.models.merchant import (
    ErrorResponseModel,
    ResponseModel,
    MerchantModel,
    UpdateMerchantModel,
)

class UserModel(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="_id")
    email: EmailStr 
    username: str 
    fullname: str 
    password: str 
    merchant: List[MerchantModel] = []
    status: bool
    scopes: List[str] = []
    
    class Config:
        schema_extra = {
            "example" : {
                "email": "usera@example.com",
                "username": "usera",
                "fullname": "User A",
                "password": "usera",
                "status": True
            }
        }

class UpdateUserModel(BaseModel):
    email: EmailStr  
    username: str 
    fullname: str 
    password: str
    merchant: List[MerchantModel] = None
    status: bool

    class Config:
        schema_extra = {
            "example" : {
                "email": "usera@example.com",
                "username": "usera",
                "fullname": "User A",
                "password": "usera",
                "status": True,
            }
        }

class UpdateUserMerchant(BaseModel):
    id_user: str

    # class Config:
    #     schema_extra = {
    #         "example" : {
    #             "id_user": "3a86bffa-a6c8-4257-b8c1-29f8a8726bc1",
    #         }
    #     }
    
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }