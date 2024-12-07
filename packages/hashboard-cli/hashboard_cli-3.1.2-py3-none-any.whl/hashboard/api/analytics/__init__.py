from typing import Optional
from hashboard.session import get_current_session

from hashboard.constants import HASHBOARD_BASE_URI


def track(event: str, value: dict, duration: Optional[int] = None):
    """Send an analytics event to the app server. If a session exists,
    it'll be used to send this event so that the event is attributed
    to the current user.

    Args:
        event (str): Event name.
        value (dict): Dict including information about the event.
        duration (Optional[int]): Duration of the event in seconds. Defaults to None.
    """
    try:
        get_current_session().post(
            f"{HASHBOARD_BASE_URI}/services/analytics/cli_track",
            headers={},
            json={
                "event": event,
                "value": value,
                "duration": duration,
            },
            timeout=0.5,
        )
    except:
        pass
