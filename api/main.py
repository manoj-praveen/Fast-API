from fastapi import status, HTTPException, Depends
from sqlalchemy.orm import Session

from api import models
from api.database_connection import engine, get_db
from app import app
from schemas.request_schema import PostSchema

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Welcome!!"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(request_payload: PostSchema, db: Session = Depends(get_db)):
    new_post = models.Post(**request_payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": new_post}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with the given id doesn't exists - id: {post_id}"
        )
    return {"data": post}


@app.put("/posts/{post_id}")
def update_post(post_id: int, request_payload: PostSchema, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with the given id doesn't exists - id: {post_id}"
        )
    post_query.update(request_payload.dict())
    db.commit()
    updated_post = post_query.first()
    return {"data": updated_post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with the given id doesn't exists - id: {post_id}"
        )
    post_query.delete()
    db.commit()
