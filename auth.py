import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import SessionLocal
from models import User, PhoneCode
from sms import send_sms

auth = APIRouter(prefix="/auth")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@auth.post("/send-code")
def send_code(phone: str, db: Session = Depends(get_db)):
    code = str(random.randint(100000, 999999))

    record = PhoneCode(phone=phone, code=code)
    db.add(record)
    db.commit()

    send_sms(phone, code)

    return {"status": "code_sent"}


@auth.post("/verify")
def verify_code(phone: str, code: str, db: Session = Depends(get_db)):
    record = db.query(PhoneCode).filter_by(phone=phone, code=code).first()

    if not record:
        raise HTTPException(status_code=400, detail="Неверный код")

    user = db.query(User).filter_by(phone=phone).first()
    if not user:
        user = User(phone=phone)
        db.add(user)
        db.commit()

    return {"status": "ok", "user_id": user.id}