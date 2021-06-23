from typing import List, Optional
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
    email: EmailStr = Field(...)#(...) Field required
    username: str = Field(...)
    fullname: str = Field(...)
    password: str = Field(...)
    merchant: List[MerchantModel] = None
    # disabled: Optional[str] = None
    
    # class Config:
    #     schema_extra = {
    #         "example" : {
    #             "email": "usera@example.com",
    #             "username": "usera",
    #             "fullname": "User A",
    #             "password": "usera",
    #             # "hashed_password": "usera",
    #             # "disabled": False, 
    #         }
    #     }

class UpdateUserModel(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(...)
    fullname: str = Field(...)
    password: str = Field(...)
    # disabled: Optional[str] = None

    class Config:
        schema_extra = {
            "example" : {
                "email": "usera@example.com",
                "username": "usera",
                "fullname": "User A",
                "password": "usera",
                # "hashed_password": "usera",
                # "disabled": False,
            }
        }
    
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