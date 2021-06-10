import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

MONGO_DETAILS = config('MONGO_DETAILS') # read environment variable.

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.merchants

merchant_collection = database.get_collection("merchants_collection")

def merchant_helper(merchant) -> dict:
    return {
        "id": str(merchant["_id"]),
        "email": merchant["email"],
        "name": merchant["name"],
    }

# Retrieve all merchants present in the database
async def retrieve_merchants():
    merchants = []
    async for merchant in merchant_collection.find():
        merchants.append(merchant_helper(merchant))
    return merchants

# Add a new merchant into to the database
async def add_merchant(merchant_data: dict) -> dict:
    merchant = await merchant_collection.insert_one(merchant_data)
    new_merchant = await merchant_collection.find_one({"_id": merchant.inserted_id})
    return merchant_helper(new_merchant)

# Retrieve a merchant with a matching ID
async def retrieve_merchant(id:str) -> dict:
    merchant = await merchant_collection.find_one({"_id": ObjectId(id)})
    if merchant:
        return merchant_helper(merchant)

# Update a merchant with a matching ID
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

# Delete a merchant from the database
async def delete_merchant(id: str):
    merchant = await merchant_collection.find_one({"_id": ObjectId(id)})
    if merchant:
        await merchant_collection.delete_one({"_id": ObjectId(id)})
        return True