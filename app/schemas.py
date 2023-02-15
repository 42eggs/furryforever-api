import re
from pydantic import BaseModel, EmailStr, conint, constr, validator
from datetime import datetime
from typing import Optional


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone: str


class UserCreate(UserBase):
    password: str

    @validator("phone")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Auth Schemas

# OAuth2PasswordRequestForm is used instead of another pydantic model for email and password


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str


# Dog Schemas


class DogBase(BaseModel):
    name: str
    description: str
    city: str
    country: str
    age_months: int
    disabled: bool = False
    street_rescue: bool = False
    potty_trained: bool = False


class DogCreate(DogBase):
    pass


class DogResponse(DogBase):
    id: int
    created_at: datetime
    owner_id: int
    age_group: int

    class Config:
        orm_mode = True


# Adoption Request Schemas


class RequestAdoptionBase(BaseModel):
    dog_id: int


class RequestAdoptionCreate(RequestAdoptionBase):
    pass


class RequestAdoptionResponseBy(RequestAdoptionBase):
    requested_by_id: int
    requested_by: UserResponse
    dog: DogResponse
    created_at: datetime

    class Config:
        orm_mode = True


class RequestAdoptionResponseTo(RequestAdoptionBase):
    requested_to_id: int
    requested_to: UserResponse
    dog: DogResponse
    created_at: datetime

    class Config:
        orm_mode = True
