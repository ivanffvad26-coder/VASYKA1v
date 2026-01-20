from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db import Base


class User(Base):
    tablename = "users"

    id = Column(Integer, primary_key=True)
    phone = Column(String, unique=True, nullable=False)


class PhoneCode(Base):
    tablename = "phone_codes"   # ← ВОТ ЭТОГО У ТЕБЯ НЕ БЫЛО

    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False)
    code = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)