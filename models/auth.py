from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class UserType(str, Enum):
    admin = "ADMIN"
    ong = "ONG"
    user = "USER"


class User(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    type: UserType = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "jdoe@gmail.com",
                "password": "Secure123",
                "type": "ADMIN",
            }
        }


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
