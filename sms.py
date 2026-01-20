import os
from twilio.rest import Client

account_sid = os.environ.get("TWILLIO_SID")
auth_token = os.environ.get("TWILIO_TOKEN")
twilio_phone = os.environ.get("TWILIO_PHONE")

client = Client(account_sid, auth_token)

def send_sms(phone, code):
    client.messages.create(
        body=f"Ваш код подтверждения: {code}",
        from=twilio_phone,
        to=phone
    )