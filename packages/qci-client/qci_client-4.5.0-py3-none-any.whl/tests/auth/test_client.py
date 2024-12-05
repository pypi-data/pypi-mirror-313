# Copyright 2023-2024, Quantum Computing Incorporated
"""Test QCi authentication API client."""

import unittest

from qci_client.auth.client import AuthClient


class TestClient(unittest.TestCase):
    """Test suite for auth client."""

    def test_access_token(self):
        """Test access token management."""
        # This should initialize with unset access token info.
        client = AuthClient()
        # Have to check that underlying psuedo-private property is not set.
        self.assertIsNone(client._access_token_info)  # pylint: disable=protected-access

        # Calling this should set access token info, including setting expiration.
        access_token_info = client.access_token_info
        self.assertNotEqual(access_token_info, {})

        # Getting access token should not reset access token info.
        access_token = client.access_token
        self.assertEqual(access_token, access_token_info["access_token"])

        # Double-check that direct call also does not reset info.
        access_token_info_recalled = client.access_token_info
        self.assertDictEqual(access_token_info_recalled, access_token_info)
