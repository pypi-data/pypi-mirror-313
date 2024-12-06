import os
import unittest
from unittest import mock

import requests_mock  # type: ignore
import tableauserverclient as TSC  # type: ignore

from ....client import ApiClient
from ..utils import KEYS

TEST_ASSET_DIR = os.path.join(os.path.dirname(__file__), "../assets/rest_api/")

GET_XML = os.path.join(TEST_ASSET_DIR, "workbook_get.xml")

EXPECTED = [
    {
        "id": "6d13b0ca-043d-4d42-8c9d-3f3313ea3a00",
        "name": "Superstore",
        "description": "description for Superstore",
        "tags": set(),
        "project_id": "ee8c6e70-43b6-11e6-af4f-f7b0d8e20760",
        "created_at": None,
        "updated_at": None,
        "owner_id": "5de011f8-5aa9-4d5b-b991-f462c8dd6bb7",
        "webpage_url": "http://tableauserver/#/workbooks/1/views",
    },
    {
        "id": "3cc6cd06-89ce-4fdc-b935-5294135d6d42",
        "name": "SafariSample",
        "description": "description for SafariSample",
        "tags": {"Sample", "Safari"},
        "project_id": "ee8c6e70-43b6-11e6-af4f-f7b0d8e20760",
        "created_at": None,
        "updated_at": None,
        "owner_id": "5de011f8-5aa9-4d5b-b991-f462c8dd6bb7",
        "webpage_url": "http://tableauserver/#/workbooks/2/views",
    },
]


class WorkbookTests(unittest.TestCase):
    @mock.patch.dict(os.environ, KEYS)
    def setUp(self):
        self._client = ApiClient(test=True)
        self._client._server = TSC.Server("http://test")

        # Fake signin
        self._client._server._site_id = "dad65087-b08b-4603-af4e-2887b8aafc67"
        self._client._server._auth_token = "j80k54ll2lfMZ0tv97mlPvvSCRyD0DOM"

        self.baseurl = self._client._server.workbooks.baseurl

    def test_fetch_workbooks(self):
        with open(GET_XML, "rb") as f:
            response_xml = f.read().decode("utf-8")
        with requests_mock.mock() as m:
            m.get(self.baseurl, text=response_xml)
            results = self._client._fetch_workbooks()

            self.assertEqual(results, EXPECTED)
