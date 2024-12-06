import logging
from argparse import ArgumentParser

from castor_extractor.utils import parse_filled_arguments  # type: ignore
from castor_extractor.visualization import tableau_revamp  # type: ignore

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def main():
    parser = ArgumentParser()

    user_group = parser.add_mutually_exclusive_group(required=False)
    user_group.add_argument("-u", "--user", help="Tableau user")
    user_group.add_argument("-n", "--token-name", help="Tableau token name")

    password_group = parser.add_mutually_exclusive_group(required=False)
    password_group.add_argument("-p", "--password", help="Tableau password")
    password_group.add_argument("-t", "--token", help="Tableau token")

    parser.add_argument("-b", "--server-url", help="Tableau server url")
    parser.add_argument("-i", "--site-id", help="Tableau site ID")

    parser.add_argument(
        "--with-pulse",
        dest="with_pulse",
        action="store_true",
        help="Extract Tableau Pulse assets: Metrics and Subscriptions",
    )

    parser.add_argument("-o", "--output", help="Directory to write to")

    tableau_revamp.extract_all(**parse_filled_arguments(parser))
