from typing import Optional
import uuid
from pydantic import BaseModel, EmailStr, Field

class MerchantModel(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="_id")
    email: EmailStr
    name: str
    id_user : str
    
    class Config:
        schema_extra = {
            "example" : {
                "email": "merchanta@gmail.com",
                "name": "Merchant A",
                "id_user": "usera"
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