from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class ContactCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    phone: str = Field(pattern=r'^\+?1?\d{9,15}$', description="Phone number in international format")
    birthday: date
    data_add: Optional[str] = Field(max_length=250)


class ContactUpdate(ContactCreate):
    pass


class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    data_add: Optional[str]

    class Config:
        orm_mode = True


