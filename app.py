from flask import Flask, request, jsonify
from flask_cors import CORS
from db import engine, Base, get_db
from auth import send_code, check_code
from sqlalchemy.orm import Session

app = Flask(__name__)
CORS(app)

Base.metadata.create_all(bind=engine)


@app.post("/send-code")
def send_sms():
    phone = request.json.get("phone")
    if not phone:
        return {"error": "phone required"}, 400

    send_code(phone)
    return {"status": "sent"}


@app.post("/verify-code")
def verify():
    phone = request.json.get("phone")
    code = request.json.get("code")

    if not phone or not code:
        return {"error": "phone and code required"}, 400

    db: Session = next(get_db())
    user = check_code(phone, code, db)

    if not user:
        return {"error": "invalid code"}, 401

    return {
        "status": "ok",
        "user_id": user.id
    }


@app.get("/")
def health():
    return {"status": "ok"}