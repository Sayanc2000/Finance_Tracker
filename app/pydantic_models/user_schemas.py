from enum import Enum

from pydantic import BaseModel


class UserLogin(BaseModel):
    email: str
    password: str


class UserToken(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    password: str


class UserDisplay(UserBase):
    id: str
    total: float

    class Config:
        orm_mode = True


class EntryType(str, Enum):
    EXPENSE = 'expense'
    INCOME = 'income'
