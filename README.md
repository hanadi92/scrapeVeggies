Packages

pip freeze > requirements.txt
pip install -r requirements.txt
pip install --upgrade -r requirements.txt


## TODO
- Make request with decoded form-data, change content-type.
    ```
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    ```
    ```
    _form_data = _read_from_file("form_data.json")
    _form_data['TxtFdate'] = _fr
    _form_data['TxtTdate'] = _to
    _res = _post_request(_uri, _headers, _form_data)
    ```
