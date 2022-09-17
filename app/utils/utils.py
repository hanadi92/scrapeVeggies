import json


def read_from_file(_filename):
    """Read headers from JSON"""
    with open(_filename, encoding="utf-8", mode="r") as _file:
        if _filename.endswith('.json'):
            return json.load(_file)
        return _file.read()
