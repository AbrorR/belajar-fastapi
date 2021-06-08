import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.merchant

merchant_collection = database.get_collection("merchant_collection")

def merchant_helper(merchant) -> dict:
    return {
        "id": str(merchant["_id"]),
        "email": merchant["email"],
        "name": merchant["name"],
    }