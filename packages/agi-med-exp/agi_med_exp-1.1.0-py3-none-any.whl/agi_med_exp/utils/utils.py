from datetime import datetime


def make_session_id() -> str:
    return f"{datetime.now():%y%m%d%H%M%S}"
