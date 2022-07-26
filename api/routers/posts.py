from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from api import models
from api.database_connection import get_db
from api.routers import oauth2
from api.schemas.request_schema import PostSchema
from api.schemas.response_schema import (PostResponseSchema,
                                         PostVoteResponseSchema)

post_router = APIRouter(
    prefix="/posts", tags=['Posts']
)


@post_router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponseSchema)
def create_posts(request_payload: PostSchema, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**request_payload.dict())
    new_post.user_id = current_user
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@post_router.get("/", response_model=List[PostVoteResponseSchema])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, offset: int = 0,
              search: Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,
        models.Post.id == models.Vote.post_id,
        isouter=True
    ).group_by(models.Post.id).filter(
        models.Post.title.contains(search)
    ).limit(limit).offset(offset).all()
    return posts


@post_router.get("/{post_id}", response_model=PostVoteResponseSchema)
def get_post(post_id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,
        models.Post.id == models.Vote.post_id,
        isouter=True
    ).group_by(models.Post.id).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with the given id doesn't exists - id: {post_id}"
        )
    return post


@post_router.put("/{post_id}", response_model=PostResponseSchema)
def update_post(post_id: int, request_payload: PostSchema, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with the given id doesn't exists - id: {post_id}"
        )
    if post.user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action."
        )
    post_query.update(request_payload.dict())
    db.commit()
    updated_post = post_query.first()
    return updated_post


@post_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with the given id doesn't exists - id: {post_id}"
        )
    if post.user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action."
        )
    post_query.delete()
    db.commit()
