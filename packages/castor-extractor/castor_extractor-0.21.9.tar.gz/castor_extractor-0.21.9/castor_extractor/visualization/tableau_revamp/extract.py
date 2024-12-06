import logging
from typing import Iterable, Tuple

from ...utils import (
    OUTPUT_DIR,
    current_timestamp,
    deep_serialize,
    from_env,
    get_output_filename,
    write_json,
    write_summary,
)
from .assets import TableauRevampAsset
from .client import TableauRevampClient, TableauRevampCredentials

logger = logging.getLogger(__name__)


def iterate_all_data(
    client: TableauRevampClient,
) -> Iterable[Tuple[TableauRevampAsset, list]]:
    """Iterate over the extracted Data from Tableau"""

    for asset in TableauRevampAsset:
        data = client.fetch(asset)
        yield asset, deep_serialize(data)


def extract_all(**kwargs) -> None:
    """
    Extract Data From tableau and store it locally in files under the
    output_directory
    """
    output_directory = kwargs.get("output") or from_env(OUTPUT_DIR)
    with_pulse = kwargs.get("with_pulse") or False
    timestamp = current_timestamp()

    credentials = TableauRevampCredentials(**kwargs)
    client = TableauRevampClient(credentials, with_pulse=with_pulse)
    client.login()

    for key, data in iterate_all_data(client):
        filename = get_output_filename(key.value, output_directory, timestamp)
        write_json(filename, data)

    write_summary(
        output_directory,
        timestamp,
        base_url=client.base_url,
        client_name=client.name,
    )
