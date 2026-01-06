from fastapi import APIRouter, Request,Response
from app.logic.message_handler import handle_message
from twilio.twiml.messaging_response import MessagingResponse

from app.core.logger import get_logger

logger = get_logger("whatsapp")

router = APIRouter()


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    message = form.get("Body")
    phone = form.get("From")

    logger.info(f"[WEBHOOK] Incoming message='{message}' from={phone}")
    reply = await handle_message(message, phone)

    logger.info(f"[WEBHOOK] Reply='{reply}' to={phone}")

    reply = reply or "Sorry, I didn’t understand that."
    twilio_resp = MessagingResponse()
    twilio_resp.message(reply)
    #return str(twilio_resp)
    return Response(
        content=str(twilio_resp),
        media_type="application/xml"
    )
'''
#return str(twilio_resp) was not returning any response to the user
FastAPI defaults the response Content-Type to application/json.

⚠️ Twilio requires Content-Type: application/xml for TwiML
If not, Twilio silently ignores the message — no error shown.

This is a classic Twilio + FastAPI trap.
'''

