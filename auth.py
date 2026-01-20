import random
from flask import Blueprint, request, session, redirect, url_for
from models import User, PhoneCode
from sms import send_sms
from db import get_db

auth = Blueprint("auth", __name__)

@auth.route("/send-code", methods=["POST"])
def send_code():
    phone = request.json.get("phone")
    if not phone:
        return {"error": "Phone required"}, 400
    
    code = str(random.randint(100000, 999999))

    db = get_db()
    db.query(PhoneCode).filter_by(phone=phone).delete()
    db.add(PhoneCode(phone=phone, code=code))
    db.commit()
    db.close()

    send_sms(phone, code)

    return {"message": "SMS sent"}

@auth.route("/verify-code", methods={"POST"})
def verify_code():
    phone = request.json.get("phone")
    code = request.json.get("code")

    if not phone or not code:
        return {"error": "Phone and code required"}, 400

    db = get_db()
    record = db.query(PhoneCode).filter_by(
        phone=phone,
        code=code
        ).first()

    if not record:
        db.close()
        return {"error": "Invalid code"}, 400
    
    user = db.query(User).filter_by(phone=phone).first()

    if not user:
        user = User(phone=phone)
        db.add(user)
        db.commit()

    session["user_id"] = user.id

    db.delete(record)
    db.commit()
    db.close()

    return {"message": "Logged in"}
