"""Stuff"""
import os
import sys

import dotenv  # pylint: disable=import-error

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from utils.utils import \
    read_from_file  # pylint: disable=no-name-in-module,wrong-import-position


def _get_config():
    config = dotenv.dotenv_values(".env")
    _csv_directory = config["CSV_DIR"]

    return _csv_directory


def main():
    """
    Process CSV data
    Store data somewhere
    """

    _colummns = read_from_file("columns.json")
    print(_colummns)



    print("processed")


if __name__ == "__main__":
    main()
