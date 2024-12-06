import http.server
import json
import os
import random
import urllib.parse
import webbrowser
from pathlib import Path
from threading import Timer
from typing import Any, cast
from urllib.parse import urlparse

import ee
import google.auth
import google.oauth2.credentials
from google.auth import compute_engine
from google.auth.exceptions import DefaultCredentialsError
from google.auth.transport.requests import Request
from gotrue import Session
from gotrue.errors import AuthApiError
from loguru import logger

from earthscale.constants import GOOGLE_AUTH_SCOPES
from earthscale.utils import is_google_drive_url, running_on_cloud_run
from supabase import Client, ClientOptions

_SUPABASE_URL = "https://mvkmibwhbplfmurjawlk.supabase.co"
_SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im12a21pYndoYnBsZm11cmphd2xrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTg4MTcyMjEsImV4cCI6MjAzNDM5MzIyMX0.7Vp3C__qs9Cdb0HD1Zx0uqD5DOem70_k6NDkzbMutyQ"  # noqa: E501
_CREDENTIALS_FILE = Path().home() / ".earthscale" / "credentials.json"
_GCP_BILLING_ENVIRONMENT_VARIABLE = "EARTHSCALE_GCP_BILLING_PROJECT"

_SUCCESSFUL_LOGIN_HTML = b"""
    <html>
        <head>
            <style>
                body {
                    background-color: #f0f0f0;
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    color: #333;
                }
                .message {
                    text-align: center;
                    border-radius: 15px;
                    padding: 50px;
                    background-color: #fff;
                    box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.1);
                }
                h1 {
                    margin-bottom: 20px;
                    font-size: 24px;
                }
                p {
                    font-size: 18px;
                }
            </style>
        </head>
        <body>
            <div class="message">
                <h1>You have successfully logged in to Earthscale!</h1>
                <p>You can now close this tab.</p>
            </div>
        </body>
    </html>
"""


class ExpiredSessionError(Exception):
    """Raised when the authentication session has expired"""


class MissingAuthHeaderError(Exception):
    """Raised when the Supabase auth credentials are missing"""


def _save_session_to_file(
    session: Session,
    credentials_file: Path,
    event_name: str | None = None,
) -> None:
    if event_name is not None and event_name != "TOKEN_REFRESHED":
        return

    with credentials_file.open("w") as f:
        credentials = {
            "user_id": session.user.id,
            "user_email": session.user.email,
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "expires_in": session.expires_in,
            "expires_at": session.expires_at,
        }
        json.dump(credentials, f, indent=2)
    logger.debug(f"Credentials saved to {credentials_file}")


def authenticate() -> None:
    client = Client(
        _SUPABASE_URL,
        _SUPABASE_ANON_KEY,
        options=ClientOptions(
            # Setting the flow type here is crucial. Without, the redirect will contain
            # "#access_token=..." instead of "?code=..." which is not passed on as part
            # of a 302 redirect
            # E.g. like here: https://community.auth0.com/t/the-redirect-response-does-not-send-the-hash-fragment-tokens-to-the-server-side/6180
            #
            # This is somewhat undocumented in the Supabase Python SDK, but the
            # changes in https://github.com/supabase-community/auth-py/issues/339
            # point to how it works
            flow_type="pkce",
            # Without this the SDK will hang and never exit
            auto_refresh_token=False,
        ),
    )
    random_port = random.randint(1024, 49151)
    oauth_response = client.auth.sign_in_with_oauth(
        {
            "provider": "google",
            "options": {
                "redirect_to": f"http://localhost:{random_port}/auth/callback",
                "query_params": {
                    "response_type": "code",
                },
            },
        },
    )

    # For some browsers, webbrowser.open() is blocking, so we need
    # to open the browser in a separate thread
    # e.g. https://stackoverflow.com/questions/69239280/run-a-webbrowser-and-continue-script-without-close-the-browser
    def open_browser() -> None:
        webbrowser.open(oauth_response.url)

    Timer(1, open_browser).start()

    class CodeHandler(http.server.BaseHTTPRequestHandler):
        code: str | None = None

        def log_message(self, format: Any, *args: Any) -> None:
            # Silence logging
            return

        def do_GET(self) -> None:
            # parse the "code" query parameter
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            code = params.get("code", [None])[0]

            if code is None:
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(
                    b"Authentication failed! Did you use the right account?"
                )
                self.server.server_close()
                return

            session = client.auth.exchange_code_for_session(
                {
                    "auth_code": code,
                    "redirect_to": "http://localhost:3000",
                }
            ).session
            _CREDENTIALS_FILE.parent.mkdir(exist_ok=True, parents=True)
            _save_session_to_file(session, _CREDENTIALS_FILE)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(_SUCCESSFUL_LOGIN_HTML)
            self.server.server_close()

    server = http.server.HTTPServer(("localhost", random_port), CodeHandler)
    server.handle_request()


def get_supabase_client() -> Client:
    credentials_file = Path(os.getenv("EARTHSCALE_CREDENTIALS_FILE", _CREDENTIALS_FILE))
    if not credentials_file.exists():
        logger.debug("Could not find credentials file, authenticating")
        authenticate()
    with open(credentials_file) as f:
        credentials = json.load(f)
    client = Client(
        credentials.get("supabase_url", _SUPABASE_URL),
        credentials.get("supabase_anon_key", _SUPABASE_ANON_KEY),
        options=ClientOptions(
            # Without this the SDK will hang and never exit
            auto_refresh_token=False,
        ),
    )
    # Make sure that if a new session is returned, we save it to the credentials file
    client.auth.on_auth_state_change(
        lambda event_name, session: _save_session_to_file(
            session,
            credentials_file,
            event_name,
        )
    )
    if "access_token" in credentials and "refresh_token" in credentials:
        try:
            client.auth.set_session(
                credentials["access_token"],
                credentials["refresh_token"],
            )
        except AuthApiError as e:
            if (
                ("Session from session_id" in e.message)
                or ("Session Expired" in e.message)
                or ("Invalid Refresh Token" in e.message)
            ):
                # Try logging in again and see if it works afterwards
                logger.info(
                    "It seems like you're not authenticated, re-authenticating " "now"
                )
                authenticate()
                with open(credentials_file) as f:
                    credentials = json.load(f)
                client.auth.set_session(
                    credentials["access_token"],
                    credentials["refresh_token"],
                )
            else:
                raise e
    elif "email" in credentials and "password" in credentials:
        client.auth.sign_in_with_password(
            {
                "email": credentials["email"],
                "password": credentials["password"],
            }
        )
    else:
        raise ValueError(
            f"A credentials file should either contain 'access_token' and "
            f"'refresh_token' or 'email' and 'password' fields, but "
            f"{credentials_file} did not contain either combination."
        )
    return client


def get_gcp_billing_project() -> str | None:
    """Returns the billing project to be used for GCP billing

    On the client this would be set to a cloud project the client has access to. On our
     infrastructure, this should point to the project we're running in.

    """
    try:
        _, project_id = google.auth.default()  # type: ignore[no-untyped-call]
    except DefaultCredentialsError:
        return None
    return cast(str | None, project_id)


def get_google_credentials() -> (
    tuple[
        google.oauth2.credentials.Credentials | google.auth.compute_engine.Credentials,
        str,
    ]
):
    """Returns the Google credentials and the project ID

    Credentials will have a valid token if the credentials are expired.

    """
    if running_on_cloud_run():
        # On Cloud Run, we don't have access to the default credentials for some reason
        # and `credentials.token` will always be None. That's why we're using the
        # `compute_engine.Credentials` here.
        _, project_id = google.auth.default(scopes=GOOGLE_AUTH_SCOPES)  # type: ignore[no-untyped-call]
        credentials = compute_engine.Credentials()  # type: ignore
        credentials.refresh(Request())  # type: ignore
    else:
        credentials, project_id = google.auth.default(scopes=GOOGLE_AUTH_SCOPES)  # type: ignore[no-untyped-call]
        if credentials.expired and credentials.refresh_token:  # type: ignore
            credentials.refresh(Request())  # type: ignore

    token = credentials.token
    if token is None:
        raise ValueError("No token found in credentials")
    return credentials, project_id


def initialize_earth_engine() -> None:
    """Initializes the Earth Engine Python API

    This function is required to be called before using the Earth Engine Python API.
    """
    credentials, project_id = google.auth.default(scopes=GOOGLE_AUTH_SCOPES)  # type: ignore[no-untyped-call]
    if project_id is None:
        raise ValueError("No project ID found in credentials")
    ee.Initialize(credentials=credentials, project=project_id)


def get_fsspec_storage_options(url: str) -> dict[str, Any]:
    scheme = urllib.parse.urlparse(url).scheme

    storage_options: dict[str, Any] = {}
    if scheme in ["gs", "s3"]:
        # At the moment, we're paying the bills when we're accessing storage
        storage_options["requester_pays"] = True

    gcp_billing_project = get_gcp_billing_project()
    if scheme == "gs" and gcp_billing_project is not None:
        logger.debug(
            f"Accessing google cloud storage using the GCP project "
            f"{gcp_billing_project} for billing"
        )
        storage_options.update(
            {
                "project": get_gcp_billing_project(),
            }
        )

    if scheme == "https":
        credentials, project_id = get_google_credentials()
        headers = {
            "Authorization": f"Bearer {credentials.token}",
            "x-goog-user-project": project_id,
        }
        client_options = {
            "headers": headers,
        }
        storage_options["client_kwargs"] = client_options

    return storage_options


def get_gdal_options_for_url(url: str) -> dict[str, str]:
    scheme = urlparse(url).scheme

    gdal_options = {}
    if scheme == "s3":
        gdal_options["AWS_REQUEST_PAYER"] = "requester"

    if scheme == "gs":
        gcp_billing_project = get_gcp_billing_project()
        if gcp_billing_project is not None:
            gdal_options["GS_USER_PROJECT"] = gcp_billing_project

    if scheme == "https" and is_google_drive_url(url):
        credentials, project_id = get_google_credentials()
        headers = (
            f"Authorization: Bearer {credentials.token},"
            f"x-goog-user-project: {project_id}"
        )
        gdal_options["GDAL_HTTP_HEADERS"] = headers
    return gdal_options
