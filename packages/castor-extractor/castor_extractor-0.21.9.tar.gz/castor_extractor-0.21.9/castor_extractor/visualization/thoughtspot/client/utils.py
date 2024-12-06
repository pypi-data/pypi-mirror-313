import csv
from io import StringIO
from typing import Iterator


def usage_liveboard_reader(usage_liveboard_csv: str) -> Iterator[dict]:
    """
    Converts a CSV string into an iterator of dictionaries after
    ignoring the first 6 lines, using the 7th line as the header.
    First 6 lines looks like the following:

        "Data extract produced by Castor on 09/19/2024 06:54"
        "Filters applied on data :"
        "User Action IN [pinboard_embed_view,pinboard_tspublic_no_runtime_filter,pinboard_tspublic_runtime_filter,pinboard_view]"
        "Pinboard NOT IN [mlm - availability pinboard,null]"
        "Timestamp >= 20240820 00:00:00 < 20240919 00:00:00"
        "Timestamp >= 20240919 00:00:00 < 20240920 00:00:00"

    """
    csv_file = StringIO(usage_liveboard_csv)

    for _ in range(7):
        next(csv_file)

    yield from csv.DictReader(csv_file)
