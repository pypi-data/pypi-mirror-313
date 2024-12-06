import os
import unittest
from unittest import mock

import requests_mock  # type: ignore
import tableauserverclient as TSC  # type: ignore

from ....client import ApiClient
from ..utils import KEYS

TEST_ASSET_DIR = os.path.join(os.path.dirname(__file__), "../assets/rest_api/")

GET_XML = os.path.join(TEST_ASSET_DIR, "project_get.xml")

EXPECTED = [
    {
        "id": "ee8c6e70-43b6-11e6-af4f-f7b0d8e20760",
        "name": "default",
        "description": "The default project that was automatically created by Tableau.",
        "parent_id": None,
        "folder_path": "/default",
    },
    {
        "id": "1d0304cd-3796-429f-b815-7258370b9b74",
        "name": "Tableau",
        "description": None,
        "parent_id": None,
        "folder_path": "/Tableau",
    },
    {
        "id": "4cc52973-5e3a-4d1f-a4fb-5b5f73796edf",
        "name": "Tableau/Child_1",
        "description": None,
        "parent_id": "1d0304cd-3796-429f-b815-7258370b9b74",
        "folder_path": "/Tableau/Tableau/Child_1",
    },
]


class ProjectTests(unittest.TestCase):
    @mock.patch.dict(os.environ, KEYS)
    def setUp(self):
        self._client = ApiClient()
        self._client._server = TSC.Server("http://test")

        # Fake signin
        self._client._server._site_id = "dad65087-b08b-4603-af4e-2887b8aafc67"
        self._client._server._auth_token = "j80k54ll2lfMZ0tv97mlPvvSCRyD0DOM"

        self.baseurl = self._client._server.projects.baseurl

    def test_fetch_projects(self):
        with open(GET_XML, "rb") as f:
            response_xml = f.read().decode("utf-8")
        with requests_mock.mock() as m:
            m.get(self.baseurl, text=response_xml)
            results = self._client._fetch_projects()

        self.assertEqual(results, EXPECTED)
