import time
from fastapi import status, HTTPException
from app import app
from schemas.request_schema import PostSchema

import psycopg2
from psycopg2.extras import RealDictCursor

while True:
    try:
        connection = psycopg2.connect(
            host='localhost',
            database='fast',
            user='postgres',
            port=5432,
            password='manoj1498',
            cursor_factory=RealDictCursor
        )
        cursor = connection.cursor()
        print("Connected Successfully!!")
        break
    except Exception as error:
        time.sleep(10)
        print(f"Failed to connect with database. error: {error}")


@app.get("/")
def root():
    return {"message": "Welcome!!"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(request_payload: PostSchema):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (request_payload.title,
         request_payload.content,
         request_payload.published)
    )
    new_post = cursor.fetchone()
    connection.commit()
    return {"message": new_post}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM Posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(post_id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with the given id doesn't exists - id: {post_id}"
        )
    return {"data": post}


@app.put("/posts/{post_id}")
def update_post(post_id: int, request_payload: PostSchema):
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",
                   (request_payload.title,
                    request_payload.content,
                    request_payload.published,
                    str(post_id)))
    updated_post = cursor.fetchone()
    connection.commit()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with the given id doesn't exists - id: {post_id}"
        )
    return {"data": updated_post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(post_id)))
    deleted_post = cursor.fetchone()
    connection.commit()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with the given id doesn't exists - id: {post_id}"
        )
