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
