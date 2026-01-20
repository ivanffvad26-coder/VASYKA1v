import os
from twilio.rest import Client

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_phone = os.environ.get("TWILIO_PHONE")

client = Client(account_sid, auth_token)

def send_sms(phone, code):
    message = client.messages.create(
        body=f"Ваш код подтверждения: {code}",
        from_=twilio_phone,
        to=phone
    )
    return message.sid
