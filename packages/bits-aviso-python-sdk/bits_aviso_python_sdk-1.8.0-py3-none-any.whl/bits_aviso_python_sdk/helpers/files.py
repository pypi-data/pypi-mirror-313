"""
This module provides helper functions that assist in common operations that are related to file handling.

---

## Usage
You can import the functions from the file helper module as follows:

```python
from bits_aviso_python_sdk.helpers.files import read_csv, write_csv, read_json, write_json, read_yaml, write_yaml
```

---
"""

import csv
import json
import logging
import os
import yaml


def read_csv(file_path):
    """Reads the CSV file and returns its content as a list of dictionaries.

    Args:
        file_path (str): The path to the CSV file to read.

    Returns:
        list: A list of dictionaries representing the rows in the CSV file.
    """
    rows = []
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                rows.append(row)

    except FileNotFoundError:
        print(f"File not found: {file_path}")

    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")

    return rows


def read_json(file_path):
    """Reads a .json file and returns its contents as a dictionary.

    Args:
        file_path (str): The path to the .json file.

    Returns:
        dict: The contents of the JSON file as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist at the given path.
        json.JSONDecodeError: If there is an error parsing the JSON file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r') as file:
        try:
            data = json.load(file)

        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error parsing JSON file: {e}")

    return data


def read_yaml(file_path):
    """Reads a .yaml file and returns its contents as a dictionary.

    Args:
        file_path (str): The path to the .yaml file.

    Returns:
        dict: The contents of the YAML file as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist at the given path.
        yaml.YAMLError: If there is an error parsing the YAML file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r') as file:
        try:
            data = yaml.safe_load(file)

        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file: {e}")

    return data


def write_csv(data, file_path):
    """Writes the data to a CSV file with error handling.

    Args:
        data (list[dict]): The data to be exported.
        file_path (str): The path to save the file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    # Check if the file path ends with .csv
    if not file_path.endswith(".csv"):
        logging.info("Adding .csv to the file path...")
        file_path += ".csv"  # Add .csv to the file path

    try:
        # Write the data to a CSV file
        with open(file_path, mode='w', newline='') as file:
            if data:
                # Create a CSV DictWriter
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
                logging.info(f"Data exported successfully to {file_path}.")

            else:
                logging.warning("No data provided to write to CSV.")

    except IOError as e:
        logging.error(f"Error writing to file {file_path}: {e}")
        raise


def write_json(data, file_path, ensure_ascii=False, indent=4):
    """Writes the data to a JSON file with error handling.

    Args:
        data (list[dict]): The data to be exported.
        file_path (str): The path to save the file.
        ensure_ascii (bool, optional): Whether to ensure the output is ASCII. Defaults to False.
        indent (int, optional): The number of spaces to indent the output. Defaults to 4.

    Raises:
        TypeError: If the data is not serializable to JSON.
        IOError: If there is an error writing to the file.
    """
    # Check if the file path ends with .json
    if not file_path.endswith(".json"):
        logging.info("Adding .json to the file path...")
        file_path += ".json"  # Add .json to the file path

    try:
        # Write the data to a JSON file
        with open(file_path, "w") as file:
            logging.info(f"Exporting data to {file_path}...")
            json.dump(data, file, ensure_ascii=ensure_ascii, indent=indent)
            logging.info("Data exported successfully.")

    except TypeError as e:
        logging.error(f"Data is not serializable to JSON: {e}")
        raise

    except IOError as e:
        logging.error(f"Error writing to file {file_path}: {e}")
        raise


def write_yaml(data, file_path):
    """Writes the data to a YAML file with error handling.

    Args:
        data (dict): The data to be exported.
        file_path (str): The path to save the file.

    Raises:
        IOError: If there is an error writing to the file.
        yaml.YAMLError: If there is an error serializing the data to YAML.
    """
    # Check if the file path ends with .yaml
    if not file_path.endswith(".yaml") or not file_path.endswith(".yml"):
        logging.info("Adding .yaml to the file path...")
        file_path += ".yaml"  # Add .yaml to the file path

    try:
        # Write the data to a YAML file
        with open(file_path, "w") as file:
            logging.info(f"Exporting data to {file_path}...")
            yaml.safe_dump(data, file)
            logging.info("Data exported successfully.")

    except yaml.YAMLError as e:
        logging.error(f"Error serializing data to YAML: {e}")
        raise

    except IOError as e:
        logging.error(f"Error writing to file {file_path}: {e}")
        raise


def validate_csv_headers(file_path, required_headers):
    """Validates the CSV file to ensure it has the correct headers.

    Args:
        file_path (str): The path to the CSV file to validate.
        required_headers (list): The list of required headers in the CSV file.

    Returns:
        bool: True if the CSV file is valid, False otherwise.
    """
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames

            if not all(header in headers for header in required_headers):
                raise ValueError(f"CSV file must contain the following headers: {', '.join(required_headers)}")

            logging.info("CSV file validation passed.")
            return True

    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return False

    except ValueError as e:
        logging.error(f"CSV file validation error: {e}")
        return False
