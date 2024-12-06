import os.path
import unittest
from unittest import mock

import requests_mock  # type: ignore

from ....client import ApiClient
from ..utils import KEYS

TEST_ASSET_DIR = os.path.join(os.path.dirname(__file__), "../assets/rest_api/")

AUTH_XML = os.path.join(TEST_ASSET_DIR, "auth.xml")


class AuthTests(unittest.TestCase):
    @mock.patch.dict(os.environ, KEYS)
    def setUp(self):
        self._client = ApiClient()
        self.baseurl = self._client._server.auth.baseurl

    def test_auth(self):
        with open(AUTH_XML, "rb") as f:
            response_xml = f.read().decode("utf-8")
        with requests_mock.mock() as m:
            m.post(self.baseurl + "/signin", text=response_xml)
            self._client.login()

        self.assertEqual(
            "eIX6mvFsqyansa4KqEI1UwOpS8ggRs2l",
            self._client._server.auth_token,
        )
        self.assertEqual(
            "6b7179ba-b82b-4f0f-91ed-812074ac5da6",
            self._client._server.site_id,
        )
        self.assertEqual(
            "1a96d216-e9b8-497b-a82a-0b899a965e01",
            self._client._server.user_id,
        )
