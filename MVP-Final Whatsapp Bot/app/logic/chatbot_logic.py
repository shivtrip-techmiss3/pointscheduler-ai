
# End-to-end WhatsApp bot logic with user login + create appointment (minimal flow)

from datetime import datetime, timedelta
from typing import Dict, Any
# import logging
from app.core.logger import get_logger

logger = get_logger("chatbot")
# logger = logging.getLogger("bot")
# logger.setLevel(logging.INFO)
from app.services.appointment_service import (
    check_availability,
    book_appointment,
)
from app.services.user_service import (
    bot_login,
    # save_user_name,
    # save_user_address,
    update_patient
)

SUPPORTED_CITIES = ["mumbai", "pune", "bangalore"]

# In-memory state (replace with Redis in prod)
USER_STATE: Dict[str, Dict[str, Any]] = {}


# ------------------------------
# Helpers
# ------------------------------

def get_state(phone: str) -> Dict[str, Any]:
    return USER_STATE.setdefault(phone, {})


def reset_state(phone: str) -> None:
    USER_STATE.pop(phone, None)


# ------------------------------
# Main Handler
# ------------------------------

async def handle_incoming_message(message: str, phone: str) -> str:

    logger.info(f"[BOT] handle_incoming_message called | phone={phone} | msg='{message}'")
    msg = (message or "").strip()
    msg_lower = msg.lower()

    state = get_state(phone)
    step = state.get("step")

    logger.info(f"[BOT] Current state | phone={phone} | step={step}")


    # STEP 0: LOGIN / IDENTIFY USER — ALWAYS ALLOW GREETING
    if msg_lower in ("hi", "hello", "start", "book", "book appointment"):
        logger.info(f"[BOT] Login trigger detected for {phone}")
        # reset state on fresh start
        state.clear()

        login_resp = await bot_login(phone)

        logger.info(f"[BOT] Login response for {phone}: {login_resp}")

        if not login_resp.get("success"):
            logger.error(f"[BOT] Login failed for {phone}")
            return "Sorry, we could not verify your profile right now. Please try again later."

        patient = login_resp.get("data", {})
        logger.info(f"[BOT] Patient data: {patient}")
        state["patientId"] = patient.get("id")

        if patient.get("fullName") == "Pending":
            state["step"] = "collect_name"
            logger.info(f"[BOT] Patient data: {patient}")
            return "Welcome! Please tell me your full name."

        state["step"] = "city"
        return (
            f"Welcome back {patient.get('fullName')}! 👋\n"
            "Please select your city:\n"
            "Options: Mumbai, Pune, Bangalore, Other"
        )





    # ==================================================
    # STEP 1: COLLECT NAME (new user)
    # ==================================================

    # if step == "collect_name":
    #     logger.info(f"[BOT] Collecting name for {phone}: '{msg}'")
    #     await update_patient(phone, {"fullName": msg})
    #     # state["step"] = "collect_address"
    #     # return "Thanks! Please share your address."
    #     state["step"] = "city"
    #     logger.info(f"[BOT] Name saved for {phone}, moving to city step")
    #     return (
    #         "Your profile is set up successfully 🎉\n"
    #         "Please select your city:\n"
    #         "Options: Mumbai, Pune, Bangalore, Other"
    #     )

    if step == "collect_name":
        logger.info(f"[BOT] collect_name | state={state}")

        patient_id = state.get("patientId")
        if not patient_id:
            logger.error(f"[BOT] Missing patientId during collect_name for {phone}")
            return "Session expired. Please type 'Hi' to start again."

        await update_patient(
            patient_id=patient_id,
            payload={"fullName": msg}
        )

        state["step"] = "city"
        return (
            "Your profile is set up successfully 🎉\n"
            "Please select your city:\n"
            "Options: Mumbai, Pune, Bangalore, Other"
        )


    # ==================================================
    # STEP 3: CITY SELECTION
    # ==================================================
    if step == "city":
        if msg_lower not in SUPPORTED_CITIES:
            return (
                "Sorry, we currently support appointments only in Mumbai, Pune, and Bangalore.\n"
                "Please choose one of these cities."
            )

        state["city"] = msg_lower
        state["step"] = "date"
        return (
            "Please enter the date you want for the appointment in this format: dd/mm/yyyy\n"
            "Example: 06/12/2025"
        )

    # ==================================================
    # STEP 4: DATE SELECTION + AVAILABILITY CHECK
    # ==================================================
    if step == "date":
        try:
            datetime.strptime(msg, "%d/%m/%Y")
        except ValueError:
            return "Please enter the date in the correct format: dd/mm/yyyy"

        state["date"] = msg

        # Dummy time for now
        state["time"] = "10:00"
        availability_payload = {
            "centerId": "a54c765a-d811-4c37-aa87-3ba87b76af27",
            "therapistId": "3bb654a8-b66a-44d4-9a26-20e4cad78794",
            
            "date": msg,
            "time": state["time"],
        }

        availability = await check_availability(availability_payload)
        if not availability.get("available"):
            logger.warning(f"[BOT] Slot unavailable | reason={availability}")
            return (
                "Sorry, the selected date/time is not available.\n"
                "Please try another date."
            )

        state["step"] = "confirm"
        return (
            "Thank you. Here is your appointment summary:\n"
            f"City: {state['city'].title()}\n"
            f"Date: {state['date']}\n"
            f"Time: {state['time']}\n"
            "Would you like to confirm this appointment?\n"
            "Reply 1 to Confirm\n"
            "Reply 2 to Cancel"
        )

    # ==================================================
    # STEP 5: CONFIRM & BOOK
    # ==================================================
    if step == "confirm":
        if msg == "1":
            start_dt = datetime.strptime(state["time"], "%H:%M")
            end_dt = start_dt + timedelta(hours=1)

            payload = {
                "centerId": "a54c765a-d811-4c37-aa87-3ba87b76af27",
                "name": "Speech Therapy",
                "date": state["date"],
                "startTime": state["time"],
                "endTime": end_dt.strftime("%H:%M"),
                "therapistId": "3bb654a8-b66a-44d4-9a26-20e4cad78794",
                "patientId": state["patientId"],
                "groupId": "61a2edd9-1d66-41a6-9207-9c2369beb01c",
            }

            _, status = await book_appointment(payload)
            reset_state(phone)

            if status in (200, 201):
                return (
                    "Your appointment request has been submitted.\n"
                    "You will receive a confirmation message shortly.\n"
                    "Thank you for choosing us."
                )

            return "Could not book appointment. Please try again later."

        if msg == "2":
            reset_state(phone)
            return (
                "The appointment has not been booked.\n"
                "If you need anything else, please message me again."
            )

        return "Please reply 1 to Confirm or 2 to Cancel."

    # ==================================================
    # FALLBACK
    # ==================================================
    reset_state(phone)
    return "Say 'Hi' to start again."
