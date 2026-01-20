from sqlalchemy import Column, Integer, String
from db import Base


class PhoneCode(Base):
    tablename = "phone_codes"   # ← КРИТИЧНО

    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False, index=True)
    code = Column(String, nullable=False)