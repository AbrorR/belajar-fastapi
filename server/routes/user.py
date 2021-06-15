from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user,
)

from server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserModel,
    UpdateUserModel,
)

router = APIRouter()

@router.post("/", response_description="User data added into the database")
async def add_user_data(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")

@router.get("/", response_description="Users retrieved")
async def get_user():
    user = await retrieve_users()
    if user :
        return ResponseModel(user, "User data retrieved successfully")
    return ResponseModel(user, "Empty list returned")

@router.get("/{id}", response_description="User data retrieved")
async def get_users_data(id):
    user = await retrieve_user(id)
    if user :
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred", 404, "User doesn't exist")

@router.put("/{id}",)
async def update_user_data(id: str, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
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

@router.delete("/{id}", response_description="User data deleted from database")
async def delete_user_data(id: str):
    deleted_user = await delete_user(id)
    if deleted_user: 
        return ResponseModel(
            "User ID: {} removed" . format(id),
            "User deleted successfully",
        )
    return ErrorResponseModel(
        "An error occured", 404, "User with id {0} doesn't exist".format(id)
    )