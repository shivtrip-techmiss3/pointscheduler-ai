from twilio.rest import Client #This gives us access to Twilio’s REST API.
import os
from dotenv import load_dotenv

load_dotenv()


account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(account_sid, auth_token) #Twilio verifies our account before sending any messages.

def send_whatsapp_message(to: str, message: str):
    client.messages.create(
        body=message,
        from_=twilio_number,
        to=to
    )# Sends a WhatsApp message from our Twilio number to the user.
'''
this function basically tells twilio that : Send this message to the person who sent us a message.”
the above code connects to Twilio using our credentials,
then sends the WhatsApp message to the given number.
'''
