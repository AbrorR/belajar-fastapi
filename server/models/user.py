from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

class UserModel(BaseModel):
    email: EmailStr = Field(...)#(...) Field required
    username: str = Field(...)
    fullname: str = Field(...)
    disabled: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example" : {
                "email": "usera@example.com",
                "username": "usera",
                "fullname": "User A",
                "hashed_password": "usera",
                # "disabled": False, 
            }
        }

class UpdateUserModel(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(...)
    fullname: str = Field(...)
    # disabled: Optional[str] = None

    class Config:
        schema_extra = {
            "example" : {
                "email": "usera@example.com",
                "username": "usera",
                "fullname": "User A",
                "hashed_password": "usera",
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