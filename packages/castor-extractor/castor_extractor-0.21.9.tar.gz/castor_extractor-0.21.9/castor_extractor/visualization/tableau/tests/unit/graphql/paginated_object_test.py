import os
import unittest
from unittest import mock

import requests_mock  # type: ignore
import tableauserverclient as TSC  # type: ignore

from .....tableau import TableauAsset
from ....client import ApiClient, get_paginated_objects
from ....constants import TABLEAU_SERVER_VERSION
from ..utils import KEYS

TEST_ASSET_DIR = os.path.join(
    os.path.dirname(__file__),
    "../assets/graphql/metadata",
)

METADATA_1 = os.path.join(TEST_ASSET_DIR, "metadata_1_get.json")
METADATA_2 = os.path.join(TEST_ASSET_DIR, "metadata_2_get.json")


EXPECTED_PAGINATED = [
    {"id": "0039e5d5-25fa-196b-c66e-c0675839e0b0"},
    {"id": "00b191ce-6055-aff5-e275-c26610c8c4d6"},
]


class PaginatedObjectTests(unittest.TestCase):
    @mock.patch.dict(os.environ, KEYS)
    def setUp(self):
        self._client = ApiClient()
        self._client._server = TSC.Server("http://test")

        # Fake signin
        self._client._server._site_id = "dad65087-b08b-4603-af4e-2887b8aafc67"
        self._client._server._auth_token = "j80k54ll2lfMZ0tv97mlPvvSCRyD0DOM"
        self._client._server.version = TABLEAU_SERVER_VERSION

        self.baseurl = self._client._server.metadata.baseurl

    def test_paginated_object_with_datasources(self):
        with open(METADATA_1, "rb") as f:
            response_1_json = f.read().decode()

        with open(METADATA_2, "rb") as f:
            response_2_json = f.read().decode()

        with requests_mock.mock() as m:
            m.post(
                self.baseurl,
                [
                    {"text": response_1_json, "status_code": 200},
                    {"text": response_2_json, "status_code": 200},
                ],
            )

            results = get_paginated_objects(
                self._client._server,
                TableauAsset.DATASOURCE,
                self._client._page_size,
            )

        self.assertEqual(results, EXPECTED_PAGINATED)
