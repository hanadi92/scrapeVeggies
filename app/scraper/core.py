"""Stuff"""
import datetime
import os
import sys

import dotenv  # pylint: disable=import-error
import requests
from bs4 import BeautifulSoup

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from utils.utils import \
    read_from_file  # pylint: disable=no-name-in-module,wrong-import-position


def _get_config():
    config = dotenv.dotenv_values(".env")
    _dir = config["DATA_DIR"]

    _uri = config["REQ_URL"]
    _csv_dir = config["CSV_DIR"]

    return _uri, _dir, _csv_dir


def _get_range():
    """Get dates of 5 days range"""
    # start from today go back to 5 days
    # loop for 30 days

    _now = datetime.date.today() - datetime.timedelta(days=4)
    for _x in range(0, 30, 5):
        _begin = _now - datetime.timedelta(days=_x)
        _end = _begin + datetime.timedelta(days=4)
        _begin_tup = (
            _begin.strftime("%d"),
            _begin.strftime("%m"),
            _begin.strftime("%Y"))
        _end_tup = (
            _end.strftime("%d"),
            _end.strftime("%m"),
            _end.strftime("%Y"))
        yield _begin_tup, _end_tup


def _post_request(_uri, _headers, _form_data):
    """Send post requests and get data back"""
    _session = requests.Session()
    _response = _session.post(_uri, headers=_headers, data=_form_data)
    return _response


def _get_request(_uri):
    _response = requests.get(_uri)
    return _response


def _replace_dates(_data, _dates):
    # replace {%sday}{%smonth}{%syear} respectively
    (_fr, _to) = _dates
    _data = _data.replace("{%sday}", _fr[0], 1)
    _data = _data.replace("{%smonth}", _fr[1], 1)
    _data = _data.replace("{%syear}", _fr[2], 1)

    _data = _data.replace("{%sday}", _to[0], 1)
    _data = _data.replace("{%smonth}", _to[1], 1)
    _data = _data.replace("{%syear}", _to[2], 1)

    return _data


def scrape(_uri, _headers, _raw_data, _dir, _data):
    """Scraping"""
    for tup in _data:
        _raw_data_with_dates = _replace_dates(
            _raw_data, (tup[0], tup[1]))
        _res = _post_request(_uri, _headers, _raw_data_with_dates)

        _filename = f'{tup[0][0]}-{tup[0][1]}-{tup[0][2]}.html'
        _file_path = os.sep.join([_dir, _filename])

        with open(_file_path, encoding="utf-8", mode="w+") as _file:
            _file.write(_res.text)
        _file.close()


def create_csv(_directory, _csv_directory):
    """Creating CSV data out of the HTML table"""
    for _filename in os.listdir(_directory):
        _file = os.path.join(_directory, _filename)
        _csv_filename = _filename.replace("html", "csv")
        _csv_file = os.path.join(_csv_directory, _csv_filename)

        with open(_file, mode="r", encoding="utf-8") as _html:
            _soup = BeautifulSoup(_html.read(), 'html.parser')
            _rows = _soup.find(id="GV_prices").find_all("tr", class_="")

            with open(_csv_file, encoding="utf-8", mode="w+") as _csv:
                for _row in _rows:
                    _csv.write(_row.get_text(",", strip=True) + '\n')


def main():
    """
    Scrape API for 5 days for the past 30 days
    Process HTML and save data in file
    """

    _headers = read_from_file("headers.json")
    _raw_data = read_from_file("raw_data.txt")
    _uri, _dir, _csv_dir = _get_config()
    _dates_tuple = _get_range()
    scrape(_uri, _headers, _raw_data, _dir, _dates_tuple)
    create_csv(_dir, _csv_dir)

    print("scraped")


if __name__ == "__main__":
    main()
