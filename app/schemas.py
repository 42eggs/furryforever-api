import re
from pydantic import BaseModel, EmailStr, conint, constr, validator
from datetime import datetime
from typing import Optional


# User Schemas


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone: str

    @validator("phone")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    phone: str
    created_at: datetime

    class Config:
        orm_mode = True


# Auth Schemas
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserToken(BaseModel):
    access_token: str
    token_type: str


class UserTokenData(BaseModel):
    user_id: Optional[str] = None


# Dog Schemas


class DogBase(BaseModel):
    name: str
    description: str
    age_months: int
    age_group: bool
    disabled: bool = False
    street_rescue: bool = False
    potty_trained: bool = False


class DogCreate(DogBase):
    pass


class DogResponse(DogBase):
    id: int
    created_at: datetime
    owner_id: int

    # Uncomment this to get the owner's details
    # owner: UserOut

    class Config:
        orm_mode = True


# Adoption Request Schemas


class RequestAdoptionBase(BaseModel):
    requested_to_id: int
    dog_id: int
    requested_by_id: int


class RequestAdoptionCreate(BaseModel):
    pass


class RequestAdoptionResponse(RequestAdoptionBase):
    created_at: datetime
    requested_by: UserResponse
    dog: DogResponse

    class Config:
        orm_mode = True
