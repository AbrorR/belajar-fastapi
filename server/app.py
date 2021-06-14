from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from server.routes.merchant import router as MerchantRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

fake_users_db = {
    "usera": {
        "username": "usera",
        "full_name": "User A",
        "email": "usera@example.com",
        "hashed_password": "usera",
        "disabled": False,
    },
    "userb": {
        "username": "userb",
        "full_name": "User B",
        "email": "userb@example.com",
        "hashed_password": "userb",
        "disabled": True,
    },
}

app = FastAPI()

app.include_router(MerchantRouter, tags=["Merchant"], prefix="/merchant")

def fake_hash_password(password: str) :
    return "user" + password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: EmailStr = None
    fullname: Optional[str] = None
    disabled: Optional[str] = None

class UserInDB(User):
    hashed_password: str

def get_user(db, username:str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate" : "Bearer"},
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user