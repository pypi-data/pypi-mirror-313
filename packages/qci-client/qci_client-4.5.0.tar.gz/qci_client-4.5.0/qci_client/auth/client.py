# Copyright 2023-2024, Quantum Computing Incorporated
"""Client for QCi's auth API."""

from copy import deepcopy
from datetime import datetime, timezone
import os
from typing import Optional

import requests
from requests.compat import urljoin

from qci_client.auth import types
from qci_client.utilities import raise_for_status

TOKEN_EXPIRATION_MARGIN: float = 10 * 60.0  # seconds.


class AuthClient:
    """Used to authenticate to QCi applications."""

    def __init__(
        self,
        *,
        url: Optional[str] = None,
        api_token: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        """
        Handles authentication against QCi cloud APIs.

        :param url: url basepath to API endpoint, including scheme, if None, then falls
            back to QCI_API_URL environment variable
        :param api_token: refresh token for authenticating to API, if None, then falls
            back to QCI_TOKEN environment variable
        :param timeout: number of seconds before timing out requests, None waits
            indefinitely
        """
        if not url:
            self._url = os.getenv("QCI_API_URL", "")
        else:
            self._url = url

        if not self._url:
            raise ValueError(
                "must specify url argument or QCI_API_URL environment variable"
            )

        if self._url[-1] != "/":
            self._url = self._url + "/"

        if not api_token:
            self._refresh_token = os.getenv("QCI_TOKEN", "")
        else:
            self._refresh_token = api_token

        if not self._refresh_token:
            raise AssertionError(
                "must specify api_token argument or QCI_TOKEN environment variable"
            )

        self._timeout = timeout
        self._access_token_info: Optional[types.AccessTokensPostResponseBody] = None

    @property
    def url(self) -> str:
        """Return API URL."""
        return self._url

    @property
    def api_token(self) -> str:
        """Return API token."""
        return self._refresh_token

    @property
    def timeout(self) -> Optional[float]:
        """Return timeout setting."""
        return self._timeout

    @property
    def access_tokens_url(self) -> str:
        """URL used for obtaining access tokens."""
        return self.url + "auth/v1/access-tokens/"

    @property
    def access_token_info(self) -> types.AccessTokensPostResponseBody:
        """Return user's access token info, retrieving anew when absent or expired."""
        if self._access_token_info:
            # Authenticating with an expired token simply returns a 401: Status
            # Unauthorized, so proactively check here for expiration impending or
            # already happened. Expiration times look like "2023-07-15T08:16:59Z".
            expiration = datetime.strptime(
                self._access_token_info["expires_at_rfc3339"], "%Y-%m-%dT%H:%M:%SZ"
            ).replace(tzinfo=timezone.utc)
            seconds_to_expiration = (
                expiration - datetime.now(timezone.utc)
            ).total_seconds()

            # Renew access token if it has expired or expiration is impending.
            if seconds_to_expiration < TOKEN_EXPIRATION_MARGIN:
                self._access_token_info = None

        if not self._access_token_info:
            # Retrieve new access token info.
            self._access_token_info = self.post_access_tokens()

        return deepcopy(self._access_token_info)

    @property
    def access_token(self) -> str:
        """Return user's access token, refreshing if expired or near expiration."""
        return self.access_token_info["access_token"]

    @property
    def expires_at_rfc3339(self) -> str:
        """Return expiration of user's access token."""
        return self.access_token_info["expires_at_rfc3339"]

    @property
    def token_type(self) -> str:
        """Return type of user's access token."""
        return self.access_token_info["token_type"]

    @property
    def organization_id(self) -> str:
        """Return user's organization ID."""
        return self.access_token_info["organization_id"]

    @property
    def user_id(self) -> str:
        """Return user's user ID."""
        return self.access_token_info["user_id"]

    @property
    def headers_without_authorization(self) -> dict:
        """
        HTTP headers without bearer token in Authorization header, but with
        Content-Type, Connection, and optional X-Request-Timeout-Nano headers.
        """
        headers = {
            "Content-Type": "application/json",
            # Simple, sessionless requests, so close connection proactively.
            "Connection": "close",
        }

        if self.timeout is not None:
            # Tell server when client will stop waiting for response.
            headers["X-Request-Timeout-Nano"] = str(int(10**9 * self.timeout))

        return headers

    @property
    def headers(self) -> dict:
        """HTTP headers with bearer token in Authorization header."""
        headers = self.headers_without_authorization
        headers["Authorization"] = f"Bearer {self.access_token}"

        return headers

    @property
    def headers_without_connection_close(self):
        """Headers with cached bearer token, but without connection closing."""
        headers = self.headers
        headers.pop("Connection", None)

        return headers

    def get_access_tokens_health(self) -> types.AccessTokensHealthGetResponseBody:
        """GET health."""
        response = requests.get(
            urljoin(self.access_tokens_url, "health"),
            headers=self.headers_without_authorization,
            timeout=self.timeout,
        )
        raise_for_status(response=response)

        return response.json()

    def get_access_tokens_version(self) -> types.AccessTokensVersionGetResponseBody:
        """GET version."""
        response = requests.get(
            urljoin(self.access_tokens_url, "version"),
            headers=self.headers_without_authorization,
            timeout=self.timeout,
        )
        raise_for_status(response=response)

        return response.json()

    def post_access_tokens(self) -> types.AccessTokensPostResponseBody:
        """
        Authorize user via refresh token used to retrieve finite-lived access_token.
        """
        json: types.AccessTokensPostRequestBody = {"refresh_token": self._refresh_token}
        response = requests.post(
            self.access_tokens_url,
            headers=self.headers_without_authorization,
            json=json,
            timeout=self.timeout,
        )
        raise_for_status(response=response)

        return response.json()
