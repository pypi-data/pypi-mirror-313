"""
This module provides helper functions that assist in common operations that are related to BigQuery.

---

## Usage
You can import the functions from the BigQuery helper module as follows:

```python
from bits_aviso_python_sdk.helpers.bigquery import normalize_data_for_bigquery
```

---
"""

import datetime
import json
import logging


def normalize_data_for_bigquery(data):
    """Normalizes the data for BigQuery by:
        - fixing invalid keys in the data.
        - Converting the data to newline delimited json.

    Args:
        data (dict, list[dict]): The data to normalize.

    Returns:
        dict, list[dict]: The normalized data.

    Raises:
        TypeError: If the data is not a dictionary or a list of dictionaries.
    """
    logging.info("Normalizing data for BigQuery...")

    # fix invalid keys in the data
    clean_data = replace_invalid_keys(data)

    # convert to newline delimited json
    bq_data = parse_to_nldjson(clean_data, upload_date=True)

    return bq_data


def replace_invalid_keys(data):
    """Replaces invalid characters in the keys of the given data dict or list of dicts.

    Args:
        data (dict, list[dict]): The data to convert.

    Returns:
        dict, list[dict]: The data with invalid characters replaced in the keys.

    Raises:
        TypeError: If the data is not a dictionary or a list of dictionaries.
    """
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if key == "":
                key = "empty_key"
            new_key = key.replace('.', '_').replace(' ', '_').replace('/', '>').replace('@', '#')

            if isinstance(value, (dict, list)):
                new_data[new_key] = replace_invalid_keys(value)

            else:
                new_data[new_key] = value

        return new_data

    elif isinstance(data, list):
        new_data = []
        for item in data:
            if isinstance(item, (dict, list)):
                new_data.append(replace_invalid_keys(item))

            else:
                new_data.append(item)

        return new_data

    else:
        raise TypeError("Data must be a dictionary or a list of dictionaries.")


def parse_to_nldjson(data_to_parse, upload_date=True):
    """Parses the given data into newline delimited json.
    Adds the upload date to the payload and ensures the columns do not have invalid characters.

    Args:
        data_to_parse (dict, list[dict]): The data to be parsed.
        upload_date (bool, optional): Whether to add the upload date to the payload. Defaults to True.

    Returns:
        str: The newline delimited json.
    """
    # check if the data is valid
    if isinstance(data_to_parse, str):
        raise TypeError("Data to parse must be a dictionary or a list of dictionaries.")

    # string to store nldjson
    nld_json = ""

    # convert dict to list if there's only one item
    if isinstance(data_to_parse, dict):
        data_to_parse = [data_to_parse]

    # check if the data is able to be parsed
    if not isinstance(data_to_parse, list):
        raise TypeError("Data must be a dictionary or a list of dictionaries.")

    # convert to newline delimited json
    if upload_date:  # add upload date to the payload
        logging.info("Adding upload date and converting data to nldjson...")
        for item in data_to_parse:
            item["upload_date"] = datetime.date.today().isoformat()
            nld_json += json.dumps(item) + "\n"

    else:  # upload date is not required
        logging.info("Converting data to nldjson...")
        for item in data_to_parse:
            nld_json += json.dumps(item) + "\n"

    return nld_json
