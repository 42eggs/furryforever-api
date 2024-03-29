import random
from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter, Response
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2
from ..utils import get_age_group, validate_dog_images
from sqlalchemy import func

router = APIRouter(prefix="/dogs", tags=["Dogs"])


@router.get("/", response_model=List[schemas.DogResponse])
def get_dogs(
    db: Session = Depends(get_db),
    # Uncomment if you want the user to be logged in to see the dogs
    # current_user = Depends(oauth2.get_current_user),
    limit: int = 12,
    skip: int = 0,
    search: Optional[str] = "",
    search_by_country: Optional[str] = "",
    search_by_city: Optional[str] = "",
    # Find a better way to implement search by age group
    # search_by_age_group: Optional[int] = 0,
    disabled: Optional[bool] = False,
    street_rescue: Optional[bool] = False,
    potty_trained: Optional[bool] = False,
):
    dogs = (
        db.query(models.Dog)
        .filter(models.Dog.name.contains(search))
        .filter(models.Dog.country.contains(search_by_country))
        .filter(models.Dog.city.contains(search_by_city))
        # Find a better way to implement search by age group
        # .filter(models.Dogs.age_group == search_by_age_group)
        .filter((models.Dog.disabled == disabled) | (models.Dog.disabled == True))
        .filter(
            (models.Dog.street_rescue == street_rescue)
            | (models.Dog.street_rescue == True)
        )
        .filter(
            (models.Dog.potty_trained == potty_trained)
            | (models.Dog.potty_trained == True)
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
    return dogs


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.DogResponse
)
def create_dog(
    dog: schemas.DogCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    # TODO: Validate city and country names

    # Validate the schema wrt the images
    validate_dog_images(dog)

    dog_dict_without_images = dog.dict()
    dog_dict_without_images.pop("images")

    try:
        # Begin a transaction
        with db.begin():
            new_dog = models.Dog(
                owner_id=current_user.id,
                age_group=get_age_group(dog.age_months),
                **dog_dict_without_images,
            )
            db.add(new_dog)
            db.commit()
            db.refresh(new_dog)

            for image in dog.images:
                db_image = models.DogImage(**image.dict(), dog_id=new_dog.id)
                db.add(db_image)

            db.commit()

    except Exception as e:
        # Rollback the transaction in case of any exception
        db.rollback()
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occured while inserting data",
        )

    return new_dog


@router.put("/{id}", response_model=schemas.DogResponse)
def update_dog(
    id: int,
    updated_dog: schemas.DogCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    dog_query = db.query(models.Dog).filter(models.Dog.id == id)

    dog = dog_query.first()

    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dog with id: {id} does not exist",
        )

    if not current_user.is_admin and dog.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    validate_dog_images(updated_dog)
    updated_dog_dict = updated_dog.dict()
    updated_dog_dict.update({"age_group": get_age_group(updated_dog.age_months)})
    updated_dog_dict.pop("images")

    try:
        with db.begin():
            dog_query.update(updated_dog_dict, synchronize_session=False)
            db.commit()

            # Delete all the existing images for the dog
            db.query(models.DogImage).filter(models.DogImage.dog_id == id).delete()

            # Create and add the new images for the dog
            for image in updated_dog.images:
                db_image = models.DogImage(**image.dict(), dog_id=id)
                db.add(db_image)

            db.commit()

    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occured while updating data",
        )

    return dog_query.first()


@router.get("/{id}", response_model=schemas.DogResponse)
def get_dog(
    id: int,
    db: Session = Depends(get_db),
    # Uncomment if you want the user to be logged in to see the dogs
    # current_user = Depends(oauth2.get_current_user),
):
    dog = db.query(models.Dog).filter(models.Dog.id == id).first()

    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dog with id: {id} does not exist",
        )
    return dog


@router.delete("/{id}")
def delete_dog(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    delete_query = db.query(models.Dog).filter(models.Dog.id == id)

    dog = delete_query.first()

    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dog with id: {id} does not exist",
        )

    if not current_user.is_admin and dog.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
