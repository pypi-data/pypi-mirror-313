from .lineage import LineageLinks
from .test_constants import (
    CLOSER_DATE,
    OLDER_DATE,
)


def test_LineageLinks_add():
    links = LineageLinks()
    timestamped_link = ("parent", "child", None)
    expected_key = ("parent", "child")

    links.add(timestamped_link)

    assert expected_key in links.lineage
    assert links.lineage[expected_key] is None

    # we replace None by an actual timestamp
    timestamped_link = ("parent", "child", OLDER_DATE)
    links.add(timestamped_link)
    assert expected_key in links.lineage
    assert links.lineage[expected_key] == OLDER_DATE

    # we update with the more recent timestamp
    timestamped_link = ("parent", "child", CLOSER_DATE)
    links.add(timestamped_link)
    assert expected_key in links.lineage
    assert links.lineage[expected_key] == CLOSER_DATE

    # we keep the more recent timestamp
    timestamped_link = ("parent", "child", OLDER_DATE)
    links.add(timestamped_link)
    assert expected_key in links.lineage
    assert links.lineage[expected_key] == CLOSER_DATE
