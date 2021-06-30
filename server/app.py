from server.routes.merchant import router as MerchantRouter
from server.routes.user import router as UserRouter
from server.database import router as LoginRouter

from fastapi import FastAPI

app = FastAPI()

app.include_router(LoginRouter, tags=["Login"], prefix="/login")
app.include_router(MerchantRouter, tags=["Merchant"], prefix="/merchant")
app.include_router(UserRouter, tags=["User"], prefix="/user")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
