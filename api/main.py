from fastapi.middleware.cors import CORSMiddleware

from api.routers.auth import auth_router
from api.routers.posts import post_router
from api.routers.users import user_router
from api.routers.vote import vote_router
from app import app

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(vote_router)

# Used to create tables initially . After alembic setup this is not required.
# from api import models
# from api.database_connection import engine
# models.Base.metadata.create_all(bind=engine)
