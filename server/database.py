# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./fastapi.db"
# # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

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

#Login user
async def login_user(username:str, password:str):
    found_user = await user_collection.find_one({"username":username})
    if found_user:
        found_password = found_user["password"]
        if password != found_password:
            return "password salah"
        return "berhasil login"
    if not found_user: 
        return "user tidak ditemukan"

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