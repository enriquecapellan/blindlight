from fastapi import APIRouter, HTTPException, status, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder

from utils.hashing import Hash
from utils.oauth import get_current_user
from utils.jwttoken import create_access_token
from models.auth import User

from db import (create_user, delete_user, get_users,
                get_user, get_user_by_username, update_user)


router = APIRouter()


@router.get("/", response_description="Get all users from the database")
async def get_all_users():
    users = await get_users()
    return users


@router.post('/register')
async def register(data: User = Body(...)):
    hashed_pass = Hash.bcrypt(data.password)
    user_object = dict(data)
    user_object["password"] = hashed_pass
    await create_user(user_object)
    return {"res": "created"}


@router.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_username(request.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not Hash.verify(user["password"], request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}
