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

from server.models.user import (
    UserModel,
    UpdateUserModel,
)

from server.database import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user,
)

router = APIRouter()

@router.post("/", response_description="Merchant data added into the database")
async def add_merchant_data(merchant: MerchantModel = Body(...)):
    merchant = jsonable_encoder(merchant)
    # user = jsonable_encoder(user)
    new_merchant = await add_merchant(merchant)
    # new_user = await add_user(user)
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

@router.delete("/{id}", response_description="Merchant data deleted from database")
async def delete_merchant_data(id: str):
    deleted_merchant = await delete_merchant(id)
    if deleted_merchant: 
        return ResponseModel(
            "Merchant ID: {} removed" . format(id),
            "Merchant deleted successfully",
        )
    return ErrorResponseModel(
        "An error occured", 404, "Merchant with id {0} doesn't exist".format(id)
    )