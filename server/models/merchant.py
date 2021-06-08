from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class MerchantModel(BaseModel):
    id: int = Field(...) #(...) Field required
    email: EmailStr = Field(...)
    name: str = Field(...)
    
    class Config:
        schema_extra = {
            "example" : {
                "id": "1",
                "email": "merchanta@gmail.com",
                "name": "Merchant A", 
            }
        }

class UpdateMerchantModel(BaseModel):
    id: Optional[int]
    email: Optional[EmailStr]
    name: Optional[str]

    class Config:
        schema_extra = {
            "example" : {
                "id": "1",
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