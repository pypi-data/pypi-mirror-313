from datetime import datetime
from .chat_item import OuterContextItem


def make_session_id() -> str:
    return f"{datetime.now():%y%m%d%H%M%S}"


def make_name(outer_context: OuterContextItem, dirty=True, short=False) -> str:
    if short:
        return f"{outer_context.user_id}_{outer_context.session_id}_{outer_context.client_id}"
    long: str = f"user_{outer_context.user_id}_session_{outer_context.session_id}_client_{outer_context.client_id}"
    if dirty:
        return f"{long}.json"
    return f"{long}_clean.json"
