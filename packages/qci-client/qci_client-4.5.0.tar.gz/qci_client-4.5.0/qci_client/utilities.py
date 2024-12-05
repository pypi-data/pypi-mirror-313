# Copyright 2023-2024, Quantum Computing Incorporated
"""Package-wide utilities."""

from datetime import datetime, timezone

import requests


def raise_for_status(*, response: requests.Response) -> None:
    """
    Wrap requests method of same name to include response text in exception message.

    :param response: a response from any API call using the requests package
    """
    try:
        # The requests package does special handling here, so build off of this.
        response.raise_for_status()
    except requests.HTTPError as err:
        # Include response body in exception message to aid user understanding.
        raise requests.HTTPError(
            str(err) + f" with response body: {response.text}"
        ) from err


def log_to_console(*, log: str, verbose: bool = True) -> None:
    """If verbose is true, then print log with timestamp prefix."""

    if verbose:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {log}")


def now_utc_ms() -> str:
    """Get current time in UTC with microsecond (i.e., maximum) precision."""

    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
