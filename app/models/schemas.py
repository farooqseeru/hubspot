# app/models/schemas.py

from pydantic import BaseModel
from typing import Optional


class Customer(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
