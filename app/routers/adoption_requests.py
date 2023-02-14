from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2
from typing import List, Optional

router = APIRouter(prefix="/adoption_requests", tags=["Adoption Requests"])


@router.get("/", response_model=List[schemas.RequestAdoptionResponse])
def adoption_requests(
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    return {"message": "Adoption Requests"}


@router.post("/", status_code=status.HTTP_201_CREATED)
def request_adoption(
    request_for_adoption: schemas.RequestAdoptionCreate,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    return {"message": "Adoption Request Created"}
    # if not db.query(models.Post).filter(models.Post.id == vote.post_id).first():
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with id: {vote.post_id} does not exist",
    #     )

    # vote_query = db.query(models.Vote).filter(
    #     models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    # )
    # found_vote = vote_query.first()
    # if vote.dir == 1:
    #     if found_vote:
    #         raise HTTPException(
    #             status_code=status.HTTP_409_CONFLICT,
    #             detail=f"User {current_user.id} has already voted on post {vote.post_id}",
    #         )
    #     new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
    #     db.add(new_vote)
    #     db.commit()
    #     return {"message": "Vote added"}

    # else:
    #     if not found_vote:
    #         raise HTTPException(
    #             status_code=status.HTTP_409_CONFLICT,
    #             detail=f"User {current_user.id} has not voted on post {vote.post_id}",
    #         )
    #     vote_query.delete(synchronize_session=False)
    #     db.commit()
    #     return {"message": "Vote removed"}
