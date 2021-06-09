from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class MerchantModel(BaseModel):
    email: EmailStr = Field(...)#(...) Field required
    name: str = Field(...)
    
    class Config:
        schema_extra = {
            "example" : {
                "email": "merchanta@gmail.com",
                "name": "Merchant A", 
            }
        }

class UpdateMerchantModel(BaseModel):
    email: Optional[EmailStr]
    name: Optional[str]

    class Config:
        schema_extra = {
            "example" : {
                "email": "merchantb@gmail.com",
                "name": "Merchant B",
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