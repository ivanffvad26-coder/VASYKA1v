import os
from twilio.rest import Client

TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_TOKEN = os.environ["TWILIO_TOKEN"]
TWILIO_PHONE = os.environ["TWILIO_PHONE"]

client = Client(TWILIO_SID, TWILIO_TOKEN)


def send_sms(phone: str, code: str):
    client.messages.create(
        body=f"Ваш код подтверждения: {code}",
        from_=TWILIO_PHONE,
        to=phone
    )