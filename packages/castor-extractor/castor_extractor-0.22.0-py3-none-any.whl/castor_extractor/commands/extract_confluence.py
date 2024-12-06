import logging
from argparse import ArgumentParser

from castor_extractor.knowledge import confluence  # type: ignore
from castor_extractor.utils import parse_filled_arguments  # type: ignore

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def main():
    parser = ArgumentParser()

    parser.add_argument("-a", "--account_id", help="Confluence account id")
    parser.add_argument("-b", "--base_url", help="Confluence account base url")
    parser.add_argument("-o", "--output", help="Directory to write to")
    parser.add_argument("-p", "--password", help="Confluence password")
    parser.add_argument("-u", "--username", help="Confluence username")

    confluence.extract_all(**parse_filled_arguments(parser))
