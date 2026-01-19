from sqlalchemy import create_engine
from models import Base
import os

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def init_db():
    Base.metadata.create_all(engine)
    print("DATABASE CONNECTED")