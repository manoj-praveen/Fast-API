from api import models
from api.database_connection import engine
from api.routers.auth import auth_router
from api.routers.posts import post_router
from api.routers.users import user_router
from app import app

app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)

models.Base.metadata.create_all(bind=engine)
