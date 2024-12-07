from dataclasses import dataclass

from requests import Session
from click.exceptions import ClickException

from hashboard.credentials import CliCredentials
from hashboard.api import login


def test_unauthorized():
    @dataclass
    class FakeResponse:
        status_code: int

    class FakeSession(Session):
        def __init__(self):
            pass

        def post(self, uri, data, **kwargs):
            return FakeResponse(status_code=401)

    try:
        login(FakeSession(), CliCredentials("", "", ""))
        assert False, "Expected exception to be thrown."
    except ClickException as e:
        assert e.message == "Your access key is invalid."
