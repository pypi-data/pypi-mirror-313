from __future__ import annotations

import secrets
from textwrap import dedent
from typing import Any, Dict
from urllib.parse import urlencode

import requests

from fused_batch._auth import (
    AUDIENCE,
    AUTHORIZATION,
    AUTHORIZE_URL,
    CLIENT_ID,
    CLIENT_SECRET,
    OAUTH_TOKEN_URL,
    SCOPES,
    Credentials,
    delete_token_from_disk,
    get_code_challenge,
)
from fused_batch._auth import logout as auth_logout
from fused_batch._global_api import get_api, reset_api
from fused_batch._options import options as OPTIONS

HOSTED_REDIRECT_URI = "https://www.fused.io/notebook_login_redirect"


class NotebookCredentials:
    """
    To use this credentials helper, run the following and it will guide you to create a FusedAPI object.

    ```py
    credentials = NotebookCredentials()
    ```
    """

    _code_verifier: str
    _api_kwargs: Dict[str, Any]
    _show_widget: bool
    url: str

    def __init__(
        self, *, api_kwargs: Dict[str, Any] | None = None, show_widget: bool = True
    ):
        self._code_verifier = secrets.token_urlsafe(48)
        self._api_kwargs = api_kwargs or {}
        self._show_widget = show_widget
        code_challenge = get_code_challenge(self._code_verifier)

        params = {
            "audience": AUDIENCE,
            "scope": " ".join(SCOPES),
            "response_type": "code",
            "client_id": CLIENT_ID,
            "redirect_uri": HOSTED_REDIRECT_URI,
            "code_challenge_method": "S256",
            "code_challenge": code_challenge,
        }
        self.url = f"{AUTHORIZE_URL}?{urlencode(params)}"
        if self._show_widget:
            from IPython.core.display import Markdown
            from IPython.display import display

            login_url_message = f"""
                Please open this link to authenticate with Fused:

                * [{self.url}]({self.url})

                Once you have logged in, that page will give you a code which you can paste into this notebook to finish logging in.
                """
            display(Markdown(dedent(login_url_message)))

    def finalize(self, code):
        token_data = {
            "client_id": CLIENT_ID,
            "grant_type": "authorization_code",
            "audience": AUDIENCE,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "redirect_uri": HOSTED_REDIRECT_URI,
            "code_verifier": self._code_verifier,
        }
        token_response = requests.post(
            OAUTH_TOKEN_URL, json=token_data, timeout=OPTIONS.request_timeout
        )
        token_response.raise_for_status()
        token_dict = token_response.json()

        credentials = Credentials.from_token_response(token_dict)
        AUTHORIZATION.set_credentials(credentials)

        if self._show_widget:
            from IPython.core.display import Markdown
            from IPython.display import display

            logged_in_message = "You are now logged in to Fused. :rocket:"
            display(Markdown(logged_in_message))

        return get_api()


def logout():
    """Log out the current user.

    This deletes the credentials saved to disk and resets the global Fused API.
    """
    delete_token_from_disk()
    auth_logout()
    reset_api()


def access_token() -> str:
    """Get an access token for the Fused service."""
    return AUTHORIZATION.credentials.access_token


def auth_scheme() -> str:
    return AUTHORIZATION.credentials.auth_scheme
