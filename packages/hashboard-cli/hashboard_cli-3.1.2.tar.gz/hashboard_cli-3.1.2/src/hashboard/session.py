from typing import Optional
from requests import Session


current_session: Optional[Session] = None


def get_current_session() -> Session:
    """Gets or creates a new session for the current CLI client.
    It's helpful to have access to this globally for a few reasons:
    1. Ensure that only one session ever gets created and used.
    2. Let utilities (such as our analytics tracking logic) access
       the current session without having to plumb it everywhere.
    """
    global current_session
    if not current_session:
        current_session = Session()
    return current_session
