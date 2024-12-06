import os
import unittest
from unittest import mock

import requests_mock  # type: ignore
import tableauserverclient as TSC  # type: ignore

from ....client import ApiClient
from ..utils import KEYS

TEST_ASSET_DIR = os.path.join(os.path.dirname(__file__), "../assets/rest_api/")

GET_XML = os.path.join(TEST_ASSET_DIR, "view_get_usage.xml")

EXPECTED = [
    {
        "workbook_id": "3cc6cd06-89ce-4fdc-b935-5294135d6d42",
        "view_counts": 11,
    },
    {
        "workbook_id": "6d13b0ca-043d-4d42-8c9d-3f3313ea3a00",
        "view_counts": 13,
    },
]


class UsageTests(unittest.TestCase):
    @mock.patch.dict(os.environ, KEYS)
    def setUp(self):
        self._client = ApiClient()
        self._client._server = TSC.Server("http://test_usage")

        # Fake signin
        self._client._server._site_id = "dad65087-b08b-4603-af4e-2887b8aafc67"
        self._client._server._auth_token = "j80k54ll2lfMZ0tv97mlPvvSCRyD0DOM"

        self.baseurl = self._client._server.views.baseurl

    def test_fetch_usages(self):
        with open(GET_XML, "rb") as f:
            response_xml = f.read().decode("utf-8")
        with requests_mock.mock() as m:
            m.get(
                self.baseurl + "?includeUsageStatistics=true",
                text=response_xml,
            )
            results = self._client._fetch_usages(False)

            self.assertEqual(results, EXPECTED)
