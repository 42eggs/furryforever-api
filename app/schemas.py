import re
from pydantic import BaseModel, EmailStr, conint, constr, validator
from datetime import datetime
from typing import List, Optional


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone: str


class UserCreate(UserBase):
    password: str

    _phone_regex = re.compile(r"^\+\d{7,15}\d$", re.IGNORECASE)

    @validator("phone")
    def validate_phone(cls, value):
        if not cls._phone_regex.match(value):
            raise ValueError("Invalid phone number")
        return value.strip()


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Auth Schemas


# OAuth2PasswordRequestForm is used instead of another pydantic model for email and password


# used to validate jwt response from /login/
class Token(BaseModel):
    access_token: str
    token_type: str


# used to validate in Oauth.py
class TokenData(BaseModel):
    user_id: str


# Dog's Images schemas


class DogImageBase(BaseModel):
    url: str
    is_primary: bool = False

    _url_regex = re.compile(
        r"^(https?|ftp)://[^\s/$.?#].[^\s]*\.(jpg|jpeg|png|gif)$", re.IGNORECASE
    )

    @validator("url")
    def validate_url(cls, value):
        if not cls._url_regex.match(value):
            raise ValueError("Invalid image URL")
        return value


class DogImageCreate(DogImageBase):
    pass


class DogImageResponse(DogImageBase):
    id: int

    class Config:
        orm_mode = True


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
    images: List[DogImageCreate]
    pass


class DogResponse(DogBase):
    id: int
    created_at: datetime
    owner_id: int
    age_group: int
    images: List[DogImageResponse]

    class Config:
        orm_mode = True


# Adoption Request Schemas


class RequestAdoptionBase(BaseModel):
    dog_id: int


class RequestAdoptionCreate(RequestAdoptionBase):
    pass


class RequestAdoptionResponseBase(RequestAdoptionBase):
    dog: DogResponse
    created_at: datetime

    class Config:
        orm_mode = True


class RequestAdoptionResponseBy(RequestAdoptionResponseBase):
    requested_by_id: int
    requested_by: UserResponse

    # class Config:
    #     orm_mode = True


class RequestAdoptionResponseTo(RequestAdoptionResponseBase):
    requested_to_id: int
    requested_to: UserResponse

    # class Config:
    #     orm_mode = True
