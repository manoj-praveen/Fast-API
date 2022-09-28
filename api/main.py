from app import app
from schemas.request_schema import PostSchema


@app.get("/")
def root():
    return {"message": "Welcome!!"}


@app.post("/posts")
def create_posts(request_payload: PostSchema):
    return {"message": "successfully added"}


@app.get("/posts")
def get_posts():
    pass


@app.get("/posts/{post_id}")
def get_post(post_id):
    print(post_id)
    pass


@app.put("/posts/{post_id}")
def update_post(post_id: int):
    pass


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    pass
