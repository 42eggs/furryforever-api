from fastapi import status, HTTPException, Depends, APIRouter, Response
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=schemas.UserToken)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_db = db.query(models.User).filter(models.User.email == user.username).first()

    if not user_db or not utils.verify(user.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials",
        )

    access_token = oauth2.create_access_token(data={"user_id": user_db.id})

    return {"access_token": access_token, "token_type": "bearer"}
