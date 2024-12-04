import logging

from clipstick import parse

from azure_board.cli import Main


def run():
    logging.basicConfig(level=logging.DEBUG)
    print(parse(Main)())
