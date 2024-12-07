import click
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Callable
from urllib.parse import urlparse, parse_qs, urlencode
import webbrowser

from hashboard.constants import HASHBOARD_DEBUG

# A handler for query params consumed a dict of processed query params
# and returns a redirect URL.
QueryParamsHandler = Callable[[dict], str]


def auth_and_handle_query_params(
    handle_get_query_params: QueryParamsHandler,
    base_url: str,
    query_params_dict: dict,
):
    """Opens a browser page where the user can sign up or login at the specified
    `base_url` with the given `query_params_dict` encoded. When signup or login
    finishes, Hashboard's app server creates a new access key for the user (as
    well as an account and project if the user is signing up).

    To receive information back from this browser page about the newly created
    access key (and potentially account and project), this function spins up a
    local HTTP server that listens for GET requests. In addition to the
    `query_params_dict` passed to this function, we also append a
    `cli-auth-server-host` param specifying a redirect URL at the server that
    this function spins up. Hashboard's app server makes a GET request to this URL
    using query params to pass information about the created access key back to the
    CLI client. `handle_get_query_params` is a callback that consumes the received
    query params as a dictionary and returns a final redirect URL to send the user's
    browser page to.

    Args:
        handle_get_query_params (QueryParamsHandler): Callback that consumes query params dict and returns a redirect URL.
        base_url (str): Base URL to send the user to that should enable either signup or login.
        query_params_dict (dict): Dict of query params to append to `base_url`. This function internally handles adding
          the `cli-auth-server-host` param, so consumers need not worry about this.
    """
    # `0` instructs Python to find any available port.
    server_address = ("localhost", 0)
    # HTTPServer requires a class, so we create a class object with
    # the passed `handle_get_query_params` injected.
    CustomCallbackHandler = type(
        "CustomCallbackHandler",
        (CallbackHandler,),
        # Python calls this function as if it's a class member, so we
        # wrap `handle_get_query_params` in a function that consumes `self`.
        {"handle_get_query_params": lambda self, qp: handle_get_query_params(qp)},
    )
    httpd = HTTPServer(server_address, CustomCallbackHandler)

    redirect_url = f"http://localhost:{httpd.server_port}"
    query_params_dict["cli-auth-server-host"] = redirect_url
    auth_url = f"{base_url}?{urlencode(query_params_dict)}"

    click.echo("🚀 Launching login page in your browser...")
    click.echo(
        "If this isn't showing up, copy and paste the following URL into your browser:"
    )
    click.echo()
    click.echo(auth_url)
    click.echo()

    # Open auth URL in browser.
    webbrowser.open_new(auth_url)

    # Wait for our server to handle redirect.
    httpd.handle_request()


class CallbackHandler(BaseHTTPRequestHandler):
    """Class that handles requests to the local HTTP server that
    `login_and_handle_query_params` spins up.
    """

    def __init__(
        self, *args, handle_get_query_params: QueryParamsHandler = None, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.handle_get_query_params = handle_get_query_params

    def do_GET(self):
        """Parses query params, hands them off to `handle_get_query_params`,
        and redirects to the returned URL.
        """
        query = urlparse(self.path).query
        query_params_dict = {key: value[0] for key, value in parse_qs(query).items()}
        redirect_url = self.handle_get_query_params(query_params_dict)
        self.send_response(302)
        self.send_header("Location", redirect_url)
        self.end_headers()
        return

    def log_message(self, *args):
        """Disables logging in the CLI, which we don't want to expose to the user
        unless in debug mode.
        """
        if HASHBOARD_DEBUG:
            super().log_message(*args)
