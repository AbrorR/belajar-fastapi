from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user,
    get_current_user,
    retrieve_status,
    user_collection,
    merchant_collection

)

from server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserModel,
    UpdateUserModel,
)

router = APIRouter()

@router.post("/", response_description="User data added into the database")
async def add_user_data(user: UserModel):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")

@router.get("/", response_description="Users retrieved")
async def get_user():
    users = await retrieve_users()
    if users :
        return ResponseModel(users, "User data retrieved successfully")
    return ResponseModel(users, "Empty list returned")

@router.get("/findBy{id}", response_description="User data retrieved")
async def get_users_data(id, current_user = Depends(get_current_user)):
    user = await retrieve_user(id)
    if user :
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred", 404, "User doesn't exist")

@router.get("/find")
async def get_users_status(status:bool, current_user = Depends(get_current_user)):
    found_user = await retrieve_status(status)
    if found_user :
        return ResponseModel(found_user, "User status retrieved successfully")
    return ErrorResponseModel("An error occurred", 404, "User doesn't exist")

@router.put("/{id}",)
async def update_user_data(id: str, req: UpdateUserModel, current_user = Depends(get_current_user)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    print(req)
    updated_user = await update_user(id, req)
    if updated_user:
        return ResponseModel(
            "User ID: {} name update is successful" . format(id),
            "User name updated successfully",
        )
    return ErrorResponseModel(
        "An Error Occured",
        404,
        "There was an error updating the user data.",
    )

@router.delete("/{id}" ,response_description="User data deleted from database")
async def delete_user_data(id: str, current_user = Depends(get_current_user)):
    deleted_user = await delete_user(id)
    if deleted_user: 
        return ResponseModel(
            "User ID: {} removed" . format(id),
            "User deleted successfully",
        )
    return ErrorResponseModel(
        "An error occured", 404, "User with id {0} doesn't exist".format(id)
    )

@router.get("/updateUserMerchant")
async def update_user_merchant(id_user: str, current_user = Depends(get_current_user)):
    updateMerchantUser = await merchant_collection.find({"id_user":id_user}).to_list(length=10)
    print(updateMerchantUser)
    if updateMerchantUser:
        updated_merchant_user = await user_collection.update_one(
            {"id": id_user}, {"$set": {"merchant":updateMerchantUser}}
        )
        if updated_merchant_user:
            return "True"
        return "False"
    else:
        return "data tidak merchant tidak ditemukan"
    
