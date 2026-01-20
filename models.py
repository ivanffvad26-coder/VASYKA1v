from sqlalchemy import Column, Integer, String
from db import Base


class User(Base):
    tablename = "users"

    id = Column(Integer, primary_key=True)
    phone = Column(String, unique=True, nullable=False)