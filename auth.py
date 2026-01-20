import random
from Flask import Blueprint, request, session
from db import db
from models import User, PhoneCode
from sms import send_sms

auth = Blueprint("auth", __name__)

@auth.route("/send-code", methods=["POST"])
def send_code():
    phone = request.json.get("phone")
    if not phone:
        return {"error": "Phone required"}, 400
    
    code = str(random.randint(100000, 999999))

    db = SessionLocal()
    db.query(PhoneCode).filter_by(phone=phone).delate()
    db.add(PhoneCode(phone=phone, code=code))
    db.commit()
    db.close()

    send_sms(phone, code)

    return {"message": "SMS sent"}

@auth.route("/verify-code", methods={"POST"})
def verify_code():
    phone = request.json.get("phone")
    code = request.json.get("code")

    db = SessionLocal()
    record = db.query(PhoneCode).filter_by(phone=phone, code=code).first()

    if not record:
        db.close()
        return {"error": "Invalid code"}, 400
    
    user = db.query(User).filter_by(phone=phone).first()
    if not user:
        user = User(phone=phone)
        db.add(user)

    db.delete(record)
    db.commit()
    session["user_id"] = user.id
    db.close()

    return {"message": "Logged in"}
