from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_merchant,
    delete_merchant,
    retrieve_merchant,
    retrieve_merchants,
    update_merchant,
)

from server.models.merchant import (
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

@router.get("/", response_description="Merchants retrieved")
async def get_merchants():
    merchant = await retrieve_merchants()
    if merchant :
        return ResponseModel(merchant, "Merchant data retrieved successfully")
    return ResponseModel(merchant, "Empty list returned")

@router.get("/{id}", response_description="Merchant data retrieved")
async def get_merchants_data(id):
    merchant = await retrieve_merchant(id)
    if merchant :
        return ResponseModel(merchant, "Merchant data retrieved successfully")
    return ErrorResponseModel("An error occurred", 404, "Merchant doesn't exist")

@router.put("/{id}",)
async def update_merchant_data(id: str, req: UpdateMerchantModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_merchant = await update_merchant(id, req)
    if updated_merchant:
        return ResponseModel(
            "Merchant ID: {} name update is successful" . format(id),
            "Merchant name updated successfully",
        )
    return ErrorResponseModel(
        "An Error Occured",
        404,
        "There was an error updating the merchant data.",
    )