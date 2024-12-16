from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.services.database_connection_service import Base
from app.services.database_connection_service import engine

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

User.metadata.create_all(bind=engine)