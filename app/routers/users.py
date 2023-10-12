from fastapi import status, HTTPException, Depends, APIRouter, Response
from app import oauth2
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_pass = utils.hash(user.password)
        user.password = hashed_pass
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User Already Exists"
        )


@router.get("/", response_model=schemas.UserResponse)
def get_user(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"User with id: {id} does not exist",
    #     )

    return db.query(models.User).filter(models.User.id == current_user.id).first()


@router.get("/{email}", response_model=schemas.UserResponse)
def get_user_by_email(
    email: str,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )

    return user


@router.delete("/{id}")
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    delete_query = db.query(models.User).filter(models.User.id == id)
    user = delete_query.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )

    delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
