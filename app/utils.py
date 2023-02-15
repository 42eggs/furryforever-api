import random
from fastapi import HTTPException, status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_age_group(age):
    if age <= 2:
        return 1
    elif age <= 6:
        return 2
    elif age <= 12:
        return 3
    elif age <= 24:
        return 4
    elif age <= 48:
        return 5
    elif age <= 96:
        return 6
    else:
        return 7


def validate_dog_images(dog):
    if not dog.images:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one image is required.",
        )

    if len(dog.images) > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A dog can have at most 5 images",
        )

    if len(dog.images) == 1:
        dog.images[0].is_primary = True
    else:
        flag = 0
        for image in dog.images:
            if image.is_primary == True:
                flag = flag + 1

        if flag == 0:
            primary_image = random.choice(dog.images)
            primary_image.is_primary = True

        if flag > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only one image can be primary",
            )
