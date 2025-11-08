from fastapi import FastAPI, Request
from app.services.twilio_service import send_whatsapp_message
from app.logic.chatbot_logic import get_bot_response

app = FastAPI()

@app.get("/")
def home():
    return {"message": "WhatsApp Bot is running!"}

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    data = await request.form()
    user_message = data.get("Body")
    from_number = data.get("From")
    '''
    When Twilio sends a message to your webhook (the endpoint you exposed via Ngrok),
    it doesn’t send JSON — it sends form-encoded data (like an HTML form submission).
    Hence the above line parses that incoming form and 
    gives you a dictionary-like object i.e json containing all the fields Twilio sends.
    '''
    user_message = data.get("Body")
    from_number = data.get("From")
    '''
    there are multiple firlds which twilio sends , but we only need body and from here. for ex: 
    to, profile name, smsid etc.
    '''
    print(f"Received message from {from_number}: {user_message}")

    # Get bot reply
    reply = get_bot_response(user_message)
    # here if a bot asks anything it gets feeded in reply for eg. for first step"We offer AI, ML, and Python courses.\nReply a) AI or b) Python.
    # represent the core message flow inside your WhatsApp chatbot.

    # Send reply of bot to whatsapp
    send_whatsapp_message(from_number, reply)
    # send the reply of bot to the sender of the message, we are telling twilio to do this
    return "OK"
