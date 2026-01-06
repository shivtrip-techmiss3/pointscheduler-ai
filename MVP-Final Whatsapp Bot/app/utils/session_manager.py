# user_sessions = {}

# #optional
# def get_user_session(user):
#     return user_sessions.get(user, {"step": 0})

# def update_user_session(user, data):
#     user_sessions[user] = data

# Simple in-memory state store
# Example: user_states["+919811223344"] = "waiting_name"

'''
⚠️ This is in-memory. For real prod across multiple instances, switch to Redis or DB later.

'''
user_states: dict[str, str] = {}


def set_state(user_phone: str, state: str) -> None:
    user_states[user_phone] = state


def get_state(user_phone: str) -> str | None:
    return user_states.get(user_phone)


def clear_state(user_phone: str) -> None:
    user_states.pop(user_phone, None)


def is_waiting_for_name(user_phone: str) -> bool:
    return get_state(user_phone) == "waiting_name"


def is_waiting_for_address(user_phone: str) -> bool:
    return get_state(user_phone) == "waiting_address"
