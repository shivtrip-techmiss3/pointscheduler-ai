from app.logic.chatbot_logic import handle_incoming_message


async def handle_message(message: str, phone: str) -> str:
    return await handle_incoming_message(message, phone)
