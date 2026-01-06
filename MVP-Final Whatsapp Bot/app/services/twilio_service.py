'''
You already have this file; keep or remove based on whether you want proactive messages (not via webhook). 
The current flow doesn’t require it, because we reply via MessagingResponse.
'''

from twilio.rest import Client
#from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
import os
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(account_sid, auth_token)

#optional
def send_whatsapp_message(to, body):
    from_whatsapp = "whatsapp:+14155238886"  # Twilio Sandbox number
    to_whatsapp = f"whatsapp:{to}"
    message = client.messages.create(from_=from_whatsapp, body=body, to=to_whatsapp)
    return message.sid
