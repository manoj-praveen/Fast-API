from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api import models
from api.database_connection import get_db
from api.routers import oauth2
from api.schemas.request_schema import VoteSchema

vote_router = APIRouter(
    prefix="/votes", tags=['Vote']
)


@vote_router.post("/", status_code=status.HTTP_201_CREATED)
def vote(request_payload: VoteSchema, db: Session = Depends(get_db),
         current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == request_payload.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with the given id doesn't exists - id: {request_payload.post_id}"
        )
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == models.Post.id,
        models.Vote.user_id == current_user
    )
    found_vote = vote_query.first()
    if request_payload.vote_direction == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user} already liked the post {request_payload.post_id}."
            )
        new_vote = models.Vote(user_id=current_user, post_id=request_payload.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added the vote."}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote doesn't exists."
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully removed the vote."}
