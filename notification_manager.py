from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()

TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.environ.get("TWILIO_FROM")
TWILIO_TO = os.environ.get("TWILIO_TO")


class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, text):
        self.client.messages.create(
            from_=TWILIO_FROM,
            body=text,
            to=TWILIO_TO
        )
