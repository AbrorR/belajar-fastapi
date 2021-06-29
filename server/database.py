import motor.motor_asyncio
from bson.objectid import ObjectId

from pydantic import ValidationError

from decouple import config
from fastapi import FastAPI
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes

from jose import JWTError, jwt
from passlib.context import CryptContext

MONGO_DETAILS = config('MONGO_DETAILS') # read environment variable.

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database_merchant = client.merchants
database_user = client.users

merchant_collection = database_merchant.get_collection("merchants_collection")
user_collection = database_user.get_collection("users_collection") 

def merchant_helper(merchant) -> dict:
    return {
        "id": merchant["_id"],
        "email": merchant["email"],
        "name": merchant["name"],
        "id_user": merchant["id_user"],
    }

def user_helper(user) -> dict:
    return {
        "id_user": str(user["_id"]),
        "email": user["email"],
        "username": user["username"],
        "fullname": user["fullname"],
        "password": user["password"],
        "merchant":user["merchant"],
        "status": user["status"],
    }

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/", 
scopes={"Admin": "Read information about the current user.", "Staff": "Read items."},
)

SECRET_KEY = "d849550a56736ecafa159d5b68e5bd166fd8c7cf96377b804c04e0693de42dab"
ALGORITHM = "HS256"

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     print(token)

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#Login user
@router.post("/")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    found_user = await user_collection.find_one({"username":form_data.username})
    print(found_user)
    if found_user:
        found_password = found_user["password"]
        if form_data.password != found_password:
            raise HTTPException(status_code=400, detail="Incorrect password")
        found_scopes = found_user["scopes"]
        if form_data.scopes != found_scopes:
            raise HTTPException(status_code=400, detail="Not enough permissions")
        access_token = create_access_token(
            data={"sub": found_user["username"],"scopes": form_data.scopes}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    if not found_user: 
        return "user tidak ditemukan"

@router.get("/users/me")
def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") 
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        # token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_scopes.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return username

# @router.get("/items")
# def items(current_user = Depends(get_current_user)):
#     print(current_user)
#     return {"oke"}



# async def login_user(username:str, password:str):
#     found_user = await user_collection.find_one({"username":username})
#     if found_user:
#         found_password = found_user["password"]
#         if password != found_password:
#             return "password salah"
#         return "berhasil login"
#     if not found_user: 
#         return "user tidak ditemukan"

# Retrieve all
async def retrieve_merchants():
    merchants = []
    async for merchant in merchant_collection.find():
        merchants.append(merchant_helper(merchant))
    return merchants

async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users

# Add a new into to the database
async def add_merchant(merchant_data: dict) -> dict:
    merchant = await merchant_collection.insert_one(merchant_data)
    # user = await user_collection.insert_one(merchant_data)
    new_merchant = await merchant_collection.find_one({"_id": merchant.inserted_id})
    # new_user = await user_collection.find_one({"_id": user.inserted_id})
    return merchant_helper(new_merchant)

async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

# Retrieve with a matching ID
async def retrieve_merchant(id:str) -> dict:
    merchant = await merchant_collection.find_one({"_id": id})
    print (merchant)
    if merchant:
        return merchant_helper(merchant)

async def retrieve_user(id:str) -> dict:
    user = await user_collection.find_one({"_id": id})
    if user:
        return user_helper(user)

# Retrieve with a status
async def retrieve_status(status:bool) -> dict:
    user = await user_collection.find_one({"status": status})
    if user:
        return user_helper(user)

# Update with a matching ID
async def update_merchant(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    merchant = await merchant_collection.find_one({"_id": id})
    if merchant:
        updated_merchant = await merchant_collection.update_one(
            {"_id": id}, {"$set": data}
        )
        if updated_merchant:
            return True
        return False

async def update_user(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"_id": id})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": id}, {"$set": data}
        )
        if updated_user:
            return True
        return False

# Delete from the database
async def delete_merchant(id: str):
    merchant = await merchant_collection.find_one({"_id": id})
    if merchant:
        await merchant_collection.delete_one({"_id": id})
        return True

async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True