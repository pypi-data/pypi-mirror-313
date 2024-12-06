"""
The EIP module provides a way to interact with EIP products.
The main service is SolidServer. It leverages the SolidServer API to perform various operations against it.

---

## Dependencies

**External Python Packages:**

- re

---

## Installation

To install the `eip` module you must install `bits-aviso-python-sdk`, use `pip`:

```sh
pip install bits_aviso_python_sdk
```

---
"""
import re


def convert_class_parameters(param_dict):
    """Converts the class parameters from a dict to a string format.

    Args:
        param_dict (dict): The parameters to convert to a string format.

    Returns:
        string: The parameters in a string format.
    """
    param_str = ""
    # iterate through the dict to build the string
    for param in param_dict:
        param_str += f"{param}={param_dict[param]}&"

    # remove the last '&'
    param_str = param_str[:-1]

    return param_str


def regex_check(regex_pattern, string_to_check):
    """Helper function that handles regex checking.

    Args:
        regex_pattern (string): The regex string to check another string against.
        string_to_check (string): The string to check the validity of.

    Returns:
        bool: True if valid, False if not.

    """
    re_check = re.compile(regex_pattern)
    if re_check.search(string_to_check):
        return True
    else:
        return False
