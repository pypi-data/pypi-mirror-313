# Copyright 2023-2024, Quantum Computing Incorporated
"""Test package-wide utilities."""

from datetime import datetime, timezone
import unittest

import pytest
import requests

from qci_client.utilities import raise_for_status, now_utc_ms


@pytest.mark.offline
class TestUtilities(unittest.TestCase):
    """Utilities-related test suite."""

    def test_raise_for_status_ok(self):
        """Test test_raise_for_status utility."""
        response_bytes = '{"success": true}'.encode("utf-8")
        response = requests.Response()
        response.url = "https://example.com"
        response.status_code = requests.codes.ok  # pylint: disable=no-member
        response.reason = "OK"
        response._content = response_bytes  # pylint: disable=protected-access
        # This should not raise.
        raise_for_status(response=response)

    def test_raise_for_status_not_ok(self):
        """Test test_raise_for_status utility."""
        response_bytes = '{"message": "Field is missing"}'.encode("utf-8")
        response = requests.Response()
        response.url = "https://example.com"
        response.status_code = requests.codes.bad_request  # pylint: disable=no-member
        response.reason = "Bad Request"
        response._content = response_bytes  # pylint: disable=protected-access

        with self.assertRaises(requests.HTTPError) as context:
            raise_for_status(response=response)

        self.assertEqual(
            str(context.exception),
            "400 Client Error: Bad Request for url: https://example.com with response "
            'body: {"message": "Field is missing"}',
        )

    def test_now_utc_ms(self):
        """
        Test getting current time in UTC with microsecond (i.e., maximum) precision.
        """
        # Time conversion from string should not raise.
        now = datetime.strptime(now_utc_ms(), "%Y-%m-%dT%H:%M:%S.%fZ")
        # 30s buffer should be enough for testing in CI.
        self.assertLessEqual(
            (
                now.replace(tzinfo=timezone.utc) - datetime.now(timezone.utc)
            ).total_seconds(),
            30,
        )
