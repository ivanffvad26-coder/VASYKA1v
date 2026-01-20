import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

print("DATABASE_URL ENV =", os.getenv("DATABASE_URL"))
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///db.sqlite3"
)

print("DATABASE_URL USED=", DATABASE_URL)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()