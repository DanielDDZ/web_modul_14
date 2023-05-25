from datetime import date
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    first_name: str = Field(min_length=3, strict=True, max_length=30)
    second_name: str = Field(min_length=3, strict=True, max_length=50)
    email: EmailStr
    phone: str = Field(min_length=10, strict=True, max_length=13)
    birthday: date
    description: str = Field(min_length=3, strict=True, max_length=250)


class ContactResponse(ContactModel):
    id: int = 1
    first_name: str = "User"
    second_name: str = "Example"
    email: EmailStr = "example@gmail.com"
    phone: str = "0000000000"
    birthday: date = date(year=1995, month=8, day=19)
    description: str = "Created first contact for test"
    authuser_id: int = 0

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=16)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "Contact successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
