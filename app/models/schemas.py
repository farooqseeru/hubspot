from pydantic import BaseModel, EmailStr
from typing import Optional


class ContactCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    source: str


class ContactResponse(BaseModel):
    contact_id: str
    email: EmailStr
    status: str
