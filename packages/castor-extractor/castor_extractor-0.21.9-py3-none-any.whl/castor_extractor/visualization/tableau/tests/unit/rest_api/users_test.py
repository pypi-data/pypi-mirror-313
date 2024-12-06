import os
import unittest
from unittest import mock

import requests_mock  # type: ignore
import tableauserverclient as TSC  # type: ignore

from ....client import ApiClient
from ..utils import KEYS

TEST_ASSET_DIR = os.path.join(os.path.dirname(__file__), "../assets/rest_api/")

GET_XML = os.path.join(TEST_ASSET_DIR, "user_get.xml")

EXPECTED = [
    {
        "id": "dd2239f6-ddf1-4107-981a-4cf94e415794",
        "name": "alice",
        "email": "alicecook@test.com",
        "fullname": "alice cook",
        "site_role": "Publisher",
    },
    {
        "id": "2a47bbf8-8900-4ebb-b0a4-2723bd7c46c3",
        "name": "Bob",
        "email": "bob@test.com",
        "fullname": "Bob Smith",
        "site_role": "Interactor",
    },
]


class UserTests(unittest.TestCase):
    @mock.patch.dict(os.environ, KEYS)
    def setUp(self):
        self._client = ApiClient()
        self._client._server = TSC.Server("http://test")

        # Fake signin
        self._client._server._site_id = "dad65087-b08b-4603-af4e-2887b8aafc67"
        self._client._server._auth_token = "j80k54ll2lfMZ0tv97mlPvvSCRyD0DOM"

        self.baseurl = self._client._server.users.baseurl

    def test_fetch_users(self):
        with open(GET_XML, "rb") as f:
            response_xml = f.read().decode("utf-8")
        with requests_mock.mock() as m:
            m.get(self.baseurl + "?fields=_all_", text=response_xml)
            results = self._client._fetch_users()

        self.assertEqual(results, EXPECTED)
