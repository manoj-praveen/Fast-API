from api.database_connection import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='TRUE')
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')
    )
