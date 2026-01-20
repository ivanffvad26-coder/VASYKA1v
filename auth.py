import os
from twilio.rest import Client
from sqlalchemy.orm import Session
from models import User

TWILIO_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
VERIFY_SID = os.environ["TWILIO_VERIFY_SID"]

client = Client(TWILIO_SID, TWILIO_TOKEN)


def send_code(phone: str):
    client.verify.services(VERIFY_SID).verifications.create(
        to=phone,
        channel="sms"
    )


def check_code(phone: str, code: str, db: Session):
    result = client.verify.services(VERIFY_SID).verification_checks.create(
        to=phone,
        code=code
    )

    if result.status != "approved":
        return None

    user = db.query(User).filter_by(phone=phone).first()
    if not user:
        user = User(phone=phone)
        db.add(user)
        db.commit()
        db.refresh(user)

    return user