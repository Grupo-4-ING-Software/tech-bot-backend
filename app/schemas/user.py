from sqlalchemy import Column, Integer, String
from services.database_connection_service import Base
from services.database_connection_service import engine

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)

User.metadata.create_all(bind=engine)