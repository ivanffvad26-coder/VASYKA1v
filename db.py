import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL для Render (PostgreSQL) или локально SQLite
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite:///database.db"
)

engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


def get_db():
    return SessionLocal()


def init_db():
    # импорт ТОЛЬКО здесь — важно
    from models import PhoneCode
    Base.metadata.create_all(bind=engine)