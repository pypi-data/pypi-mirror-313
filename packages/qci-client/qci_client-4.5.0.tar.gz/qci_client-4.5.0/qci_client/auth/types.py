# Copyright 2023-2024, Quantum Computing Incorporated
"""Types for QCi auth."""

from typing import TypedDict


class AccessTokensHealthGetResponseBody(TypedDict):
    """Health GET response body."""

    message: str


class AccessTokensVersionGetResponseBody(TypedDict):
    """Version GET response body."""

    application_name: str
    version: str


class AccessTokensPostRequestBody(TypedDict):
    """Typed dictionary for access-tokens root POST requests."""

    refresh_token: str


class AccessTokensPostResponseBody(TypedDict):
    """Typed dictionary for access-tokens root POST responses."""

    access_token: str
    expires_at_rfc3339: str
    token_type: str
    organization_id: str
    user_id: str
