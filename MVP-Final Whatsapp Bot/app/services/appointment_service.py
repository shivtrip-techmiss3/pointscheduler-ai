import os
import httpx

API_BASE_URL = os.getenv("BACKEND_API_BASE_URL")
API_TOKEN = os.getenv("BACKEND_API_TOKEN")

from app.core.logger import get_logger

logger = get_logger("chatbot")

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}


async def check_availability(payload: dict):
    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.post(
            f"{API_BASE_URL}/api/appointments/check",
            json=payload,
            headers=HEADERS,
        )
        #return res.json()
        # Log everything
    logger.info(
        f"[API] check_availability | status={res.status_code} | body='{res.text}'"
    )

    # Non-success HTTP
    if res.status_code != 200:
        return {
            "available": False,
            "error": f"Backend returned {res.status_code}"
        }

    # Empty response
    if not res.text or not res.text.strip():
        return {
            "available": False,
            "error": "Empty response from backend"
        }

    # Safe JSON parse
    try:
        return res.json()
    except ValueError:
        return {
            "available": False,
            "error": "Invalid JSON response from backend"
        }

async def book_appointment(payload: dict):
    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.post(
            f"{API_BASE_URL}/api/appointments/createAppointment",
            json=payload,
            headers=HEADERS,
        )
        return res.json(), res.status_code
