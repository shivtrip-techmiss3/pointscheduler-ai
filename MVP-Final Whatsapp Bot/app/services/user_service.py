import os
import httpx

from app.core.logger import get_logger

logger = get_logger("user_service")

API_BASE_URL = os.getenv("BACKEND_API_BASE_URL")
API_TOKEN = os.getenv("BACKEND_API_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}


async def bot_login(phone: str) -> dict:
    logger.info(f"[API] bot_login called | phone={phone}")
    logger.info(f"[API] Using BASE_URL={API_BASE_URL}")
    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.post(
            #f"{API_BASE_URL}/api/patient/updatePatient",
            f"{API_BASE_URL}/api/patient/getOrCreatePatientByPhone",
            json={"phone": phone},
            headers=HEADERS,
        )
        logger.info(f"[API] Status={res.status_code} | Response={res.text}")
        return res.json()


async def update_patient(patient_id: str, payload: dict) -> dict:
    """
    Update patient details.

    Required:
    - patient_id (UUID)

    
    """

    request_body = {
        "patientId": patient_id,
        **payload
    }

    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.post(
            f"{API_BASE_URL}/api/patient/updatePatient",
            json=request_body,
            headers=HEADERS,
        )

    return res.json()