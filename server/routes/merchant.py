from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from fastapi-merchant.server.database import (
    add_merchant,
    delete_merchant,
    retrieve_merchant,
    retrieve_merchants,
    update_merchant,
)

from fastapi-merchant.server.models.merchant import (
    ErrorResponseModel,
    ResponseModel,
    MerchantModel,
    UpdateMerchantModel,
)

router = APIRouter()

@router.post("/", response_description="Merchant data added into the database")
async def add_merchant_data(merchant: MerchantModel = Body(...)):
    merchant = jsonable_encoder(merchant)
    new_merchant = await add_merchant(merchant)
    return ResponseModel(new_merchant, "Merchant added successfully.")