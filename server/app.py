from fastapi import FastAPI
from fastapi-merchant.server.routes.merchant import router as MerchantRouter

app = FastAPI()

app.include_router(MerchantRouter, tags=["Merchant"], prefix="/merchant")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}