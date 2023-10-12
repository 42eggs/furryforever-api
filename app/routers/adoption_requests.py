from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2
from typing import List, Optional

router = APIRouter(prefix="/adoption_requests", tags=["Adoption Requests"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def request_adoption(
    request_for_adoption: schemas.RequestAdoptionCreate,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # Check if the dog exists
    if (
        not db.query(models.Dog)
        .filter(models.Dog.id == request_for_adoption.dog_id)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dog with id: {request_for_adoption.dog_id} does not exist",
        )

    # query result to check if the user is requesting to adopt a dog which it already owns
    if (
        db.query(models.Dog)
        .filter(models.Dog.id == request_for_adoption.dog_id)
        .filter(models.Dog.owner_id == current_user.id)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {current_user.id} is already the owner of dog {request_for_adoption.dog_id}",
        )

    # query result to check if the user has already requested adoption for the dog
    if (
        db.query(models.AdoptionRequest)
        .filter(
            (models.AdoptionRequest.dog_id == request_for_adoption.dog_id)
            & (models.AdoptionRequest.requested_by_id == current_user.id)
        )
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {current_user.id} has already requested adoption for dog {request_for_adoption.dog_id}",
        )

    # Query to get owner of the dog which has been requested from the Dog table
    dog_owner_int = int(
        db.query(models.Dog)
        .filter(models.Dog.id == request_for_adoption.dog_id)
        .first()
        .owner_id
    )

    new_adoption_request = models.AdoptionRequest(
        dog_id=request_for_adoption.dog_id,
        requested_by_id=current_user.id,
        requested_to_id=dog_owner_int,
    )
    db.add(new_adoption_request)
    db.commit()
    return {"message": "Adoption Request Created"}


# Adoption Requests by others to me (authenticated user)
@router.get("/to_me", response_model=List[schemas.RequestAdoptionResponseToMe])
def adoption_requests(
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    query_result = (
        db.query(models.AdoptionRequest)
        .filter(models.AdoptionRequest.requested_to_id == current_user.id)
        .all()
    )

    if not query_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Adoption Requests to user with id: {current_user.id} exist",
        )

    return query_result


# Adoption Requests to others by me (authenticated user)
@router.get("/by_me", response_model=List[schemas.RequestAdoptionResponseByMe])
def adoption_requests(
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    query_result = (
        db.query(models.AdoptionRequest)
        .filter(models.AdoptionRequest.requested_by_id == current_user.id)
        .all()
    )

    if not query_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Adoption Requests from user with id: {current_user.id} exist",
        )

    return query_result
