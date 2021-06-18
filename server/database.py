import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

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
        "id": str(merchant["_id"]),
        "email": merchant["email"],
        "name": merchant["name"],
    }

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "username": user["username"],
        "fullname": user["fullname"],
        "password": user["password"],
        # "disabled": user["False"],
    }

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "d849550a56736ecafa159d5b68e5bd166fd8c7cf96377b804c04e0693de42dab"
ALGORITHM = "HS256"

@app.get("/users")
def get_current_user(token = Depends (oauth2_scheme)):
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
        return username
    except JWTError:
        raise credentials_exception
    # user = user_collection.find_one({"username":token_data.username})
    # if user is None:
    #     raise credentials_exception
    # return user

# async def get_current_active_user(current_user: user_collection = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

def create_access_token(data: dict):
    to_encode = data.copy()
    # if expires_delta:
    #     expire = datetime.utcnow() + expires_delta
    # else:
    #     expire = datetime.utcnow() + timedelta(minutes=15)
    # to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#Login user
@app.post("/token")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    found_user = await user_collection.find_one({"username":form_data.username})
    print(found_user)
    if found_user:
        found_password = found_user["password"]
        if form_data.password != found_password:
            raise HTTPException(status_code=400, detail="Incorrect password")
        access_token = create_access_token(
            data={"sub": found_user["username"]}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    if not found_user: 
        return "user tidak ditemukan"

@app.get("/items")
def items(current_user = Depends(get_current_user)):
    print(current_user)
    return {"oke"}

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
    new_merchant = await merchant_collection.find_one({"_id": merchant.inserted_id})
    return merchant_helper(new_merchant)

async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

# Retrieve with a matching ID
async def retrieve_merchant(id:str) -> dict:
    merchant = await merchant_collection.find_one({"_id": ObjectId(id)})
    if merchant:
        return merchant_helper(merchant)

async def retrieve_user(id:str) -> dict:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)

# Update with a matching ID
async def update_merchant(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    merchant = await merchant_collection.find_one({"_id": ObjectId(id)})
    if merchant:
        updated_merchant = await merchant_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_merchant:
            return True
        return False

async def update_user(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False

# Delete from the database
async def delete_merchant(id: str):
    merchant = await merchant_collection.find_one({"_id": ObjectId(id)})
    if merchant:
        await merchant_collection.delete_one({"_id": ObjectId(id)})
        return True

async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True