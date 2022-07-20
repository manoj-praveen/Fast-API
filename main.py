from app import app
from schemas.request_schema import PostSchema


@app.get("/")
def root():
    return {"message": "Welcome!!"}


@app.post("/posts")
def create_posts(request_payload: PostSchema):
    print(request_payload.content)
    print(request_payload.title)
    return {"message": "successfully added"}
