from fastapi import status, HTTPException, Depends, APIRouter, Response
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user or not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials",
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
