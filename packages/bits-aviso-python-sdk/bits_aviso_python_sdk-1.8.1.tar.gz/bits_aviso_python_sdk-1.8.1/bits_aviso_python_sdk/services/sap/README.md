# SAP

This module provides tools to interact with the SAP server. It includes methods to get quote details and list quotes from a given sales organization.

---

## Installation

To install the SAP module, use `pip`:

```sh
pip install bits_aviso_python_sdk
```

---

## Usage

### Initialization

To initialize the SAP class, you need to provide a username and password for authentication.
Optionally, you can provide the URL of the SAP server.

```python
from bits_aviso_python_sdk.services.sap import SAP

sap = SAP(username='your_username', password='your_password', url='http://sap.broadinstitute.org:8085')
```

### Examples

---

#### Get Quote Details

To get the details of a specific quote, use the `get_quote_details` method:

```python
quote_number = '12345'
quote_details, error = sap.get_quote_details(quote_number)

if error:
    print(f"Error: {error}")
else:
    print(f"Quote Details: {quote_details}")
```

---

#### List All Quotes

To list all quotes from a given sales organization, use the `list_all_quotes` method:

```python
sales_org = '1000'
quotes, error = sap.list_all_quotes(sales_org)

if error:
  print(f"Error: {error}")
else:
  print(f"Quotes: {quotes}")
```

---

## Error Handling

If an error occurs during the execution of a method,
the method will return a tuple containing `None` for the data and an error payload.

```json
{
    "Error": "An error message will be here",
    "Function": "The function that caused the error"
}
```

---

# payloads

This module contains the data structures used for requests and responses in the SDK. It defines the payloads
that are sent to and received from the various services.

---
