"""
The helpers module contains utility functions that are used throughout the SDK and can also be used independently.

---

## Usage
You can import the functions from the helpers module as follows:

```python
from bits_aviso_python_sdk.helpers import initialize_logger, convert_xml_to_dict, resolve_dns
```

---
"""

import base64
import datetime
import dns.resolver
import json
import logging
import os
import re
import xmltodict
from urllib.parse import urlparse


def auth_basic(username, password):
    """Authenticates the user and returns the token by encoding the username and password in base64.

    Args:
        username (str): The username to authenticate with.
        password (str): The password to authenticate with.
    """
    return base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")


def convert_xml_to_dict(xml_string, json_output=False):
    """Converts an XML string to a dictionary.

    Args:
        xml_string (str): The XML string to convert.
        json_output (bool, optional): Whether to output the dictionary as a JSON. Defaults to False.

    Returns:
        dict: The XML string converted to a dictionary.
    """
    if json_output:
        logging.debug("Converting XML to JSON object...")
        return json.dumps(xmltodict.parse(xml_string))

    else:
        logging.debug("Converting XML to dictionary...")
        return xmltodict.parse(xml_string)


def initialize_logger(logger_level="INFO", file_handler_path=None):
    """Initializes a logger with a stream handler and an optional file handler.

    Args:
        logger_level (str, optional): The level of the logger. Defaults to "INFO".
                                      Can be "DEBUG", "INFO", "WARNING", "ERROR", or "CRITICAL".
        file_handler_path (str, optional): The path to save the log file if a file handler is desired. Defaults to None.
    """
    # set up logger
    today = datetime.datetime.now().strftime("%Y_%m_%d")
    logger = logging.getLogger()  # root logger

    # Mapping of string levels to logging constants
    level_mapping = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    # check if there's any handlers already
    if not logger.handlers:
        # create file handler if path is provided
        if file_handler_path:
            # make sure the directory exists
            os.makedirs(file_handler_path, exist_ok=True)  # make sure directory exists

            # check if the path ends with a slash
            if file_handler_path.endswith('/'):
                file_handler = logging.FileHandler(f"{file_handler_path}{today}.log")

            else:
                file_handler = logging.FileHandler(f"{file_handler_path}/{today}.log")

            # set level for logger. if value is not found, default to DEBUG
            file_handler.setLevel(level_mapping.get(logger_level, logging.DEBUG))

            # set format
            file_handler.setFormatter(logging.Formatter(
                "%(module)s %(asctime)s [%(levelname)s]: %(message)s", "%I:%M:%S %p"))
            # add file handler to the logger
            logger.addHandler(file_handler)

        # Create stream handler and set level to ERROR
        stream_handler = logging.StreamHandler()
        # set level for logger. if value is not found, default to DEBUG
        stream_handler.setLevel(level_mapping.get(logger_level, logging.INFO))
        stream_handler.setFormatter(logging.Formatter(
            "%(module)s %(asctime)s [%(levelname)s]: %(message)s", "%I:%M:%S %p"))
        # add stream handler to the logger
        logger.addHandler(stream_handler)

    # Set the logger's level to the lowest level among all handlers
    logger.setLevel(logging.DEBUG)

    return logger


def is_ip_address(string_to_check):
    """Check if the given string is a valid IP address.

    Args:
        string_to_check (str): The string to check.

    Returns:
        bool: True if the string is a valid IP address, False otherwise.
    """
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    logging.debug(f"IP Pattern: {ip_pattern}")
    if ip_pattern.match(string_to_check):
        parts = string_to_check.split('.')
        logging.debug(f"IP to Check: {string_to_check} | IP Parts: {parts}")
        return all(0 <= int(part) <= 255 for part in parts)

    logging.debug(f"{string_to_check} does not match the IP pattern.")
    return False


def resolve_dns(domain, timeout=5, lifetime=15, dns_server=None, first_result_only=True, tcp=True):
    """Resolves the domain to an IP address. If no DNS server is provided, it will use the system's default DNS server.
    Timeout and lifetime are set to 5 and 15 seconds respectively by default.

    Args:
        domain (str): The domain to resolve.
        timeout (int, optional): The timeout for the DNS resolver. Defaults to 5.
        lifetime (int, optional): The lifetime for the DNS resolver. Defaults to 10.
        dns_server (str, optional): The DNS server to use. Defaults to None.
        first_result_only (bool, optional): Whether to return only the first result. Defaults to True.
        tcp (bool, optional): Whether to use TCP for the query. Defaults to True.

    Returns:
        str or list: The resolved IP address(es).
    """
    # Check if the domain is a URL and extract the hostname
    if domain.startswith("http"):
        logging.debug(f"Domain: {domain} is a URL. Extracting hostname...")
        domain = urlparse(domain).hostname
        logging.debug(f"Extracted hostname: {domain}")

    # Initialize the resolver
    resolver = dns.resolver.Resolver()
    resolver.timeout = timeout
    resolver.lifetime = lifetime
    logging.debug("Initialized DNS resolver.")

    # Set the DNS server if provided
    if dns_server:
        resolver.nameservers = [dns_server]
        logging.debug(f"DNS server set to [{dns_server}].")

    try:
        answer = resolver.resolve(domain, tcp=tcp)
        logging.debug(f"Resolved {domain} to {answer}")

        # return the first result only if specified
        if first_result_only:
            first_result = answer[0].to_text()
            # check if the result is an IP address
            if not is_ip_address(first_result):
                raise ValueError(f"Resolved {domain} to {first_result} which is not an IP address.")

            logging.debug(f"Returning first result only: {first_result}")
            return first_result

        # otherwise return all results
        results = [rdata.to_text() for rdata in answer]

        # check if the results are valid IP addresses
        valid_ips = []
        for ip in results:
            if not is_ip_address(ip):
                logging.error(f"Resolved {domain} to {ip} which is not an IP address. This result will be ignored.")
                continue
            else:
                valid_ips.append(ip)

        if valid_ips:
            logging.debug(f"Returning valid results: {valid_ips}")
            return valid_ips
        else:
            raise ValueError(f"Unable to resolve {domain} to any valid IP addresses.")

    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout, ValueError) as e:
        logging.error(f"Error resolving DNS: {e}")
        return
