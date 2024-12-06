"""
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
"""
import requests
import urllib3
from bits_aviso_python_sdk.helpers import convert_xml_to_dict, resolve_dns
from bits_aviso_python_sdk.services.sap.payloads import *

urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)


class SAP:
    def __init__(self, username, password, url, dns_resolve=False, dns_server=None):
        """Initializes the SAP class.

        Args:
            username (str): The username to authenticate with.
            password (str): The password to authenticate with.
            url (str): The base URL of the SAP server. Must include the protocol.
            dns_resolve (bool, optional): Whether to resolve the DNS. Defaults to False.
            dns_server (str, optional): The DNS server to use. Defaults to None.
        """
        self.username = username
        self.password = password
        self.url = url
        self.dns_resolve = dns_resolve
        self.dns_server = dns_server
        self.headers = {'Content-Type': 'text/xml; charset=utf-8'}

    def api_handler(self, endpoint, payload):
        """Handles the API call to the SAP server.

        Args:
            endpoint (str): The endpoint to call.
            payload (str): The payload to send to the SAP server.

        Returns:
            dict, dict: The response data and the error payload.
        """
        # check if the url needs to be resolved
        if self.dns_resolve:
            ip = resolve_dns(self.url, dns_server=self.dns_server)
            if not ip:
                raise ValueError(f'Unable to resolve the DNS for {self.url} with DNS server {self.dns_server}.')

            base_url = f'https://{ip}:8005'
            ssl_verify = False  # disable SSL verification when using IP address

        else:
            base_url = self.url
            ssl_verify = True

        # create the url
        url = f'{base_url}{endpoint}'

        try:
            # call the api
            response = requests.post(url, headers=self.headers, auth=(self.username, self.password), data=payload,
                                     verify=ssl_verify)

            # check the response
            if response.status_code != 200:
                raise TimeoutError(f'Unable to call the API. | Error Code {response.status_code}:'
                                   f' {response.reason}')

            else:
                # convert the xml response to json
                sap_data = convert_xml_to_dict(response.content.decode('utf-8'))
                return sap_data, {}

        except (requests.exceptions.RequestException, requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout, TimeoutError, ValueError) as e:
            return {}, {'Error': f'Unable to call the API. | {e}'}

    def get_quote_details(self, quote_number):
        """Gets the quote details from the SAP server.

        Args:
            quote_number (str): The quote number.

        Returns:
            list[dict], dict: The quote data and the error payload.
        """
        # create the payload
        xml_str = payloads.get_quote_details(quote_number)

        # call the api
        endpoint = '/sap/bc/srt/rfc/sap/zapisdquotedetailsv3/100/zapisdquotedetailsv3service/zapisdquotedetailsv3binding'
        quote_details, quote_details_error = self.api_handler(endpoint, xml_str)

        # check the response
        if quote_details_error:  # add function name to the error payload
            quote_details_error['Function'] = 'get_quote_details'
            return [], quote_details_error

        else:
            try:
                # parse the quote details
                quote_data = quote_details['soap-env:Envelope']['soap-env:Body']['n0:ZBAPISDQUOTEDETAILSV3Response']
                quote_data.pop('@xmlns:n0', None)  # remove the namespace
                # move items up one level in the dict
                quote_data = self._move_up_one_level(quote_data, nested_key='item')
                return quote_data, {}

            except KeyError as e:
                quote_details_error['Function'] = 'get_quote_details'
                quote_details_error['Error'] = f'Unable to parse the quote details from the response. | {e}'
                return [], quote_details_error

    def list_all_quotes(self, sales_org):
        """Lists all the quotes from a given sales org in the SAP server.

        Args:
            sales_org (str): The sales organization to list quotes for.

        Returns:
            list[dict], dict: The quote data and the error payload.
        """
        # create the payload
        xml_str = payloads.list_quotes(sales_org)

        # call the api
        endpoint = '/sap/bc/srt/rfc/sap/zapisdactivequotes/100/zapisdactivequotesservice/zapisdactivequotesbinding'
        quotes, quotes_error = self.api_handler(endpoint, xml_str)

        # check the response
        if quotes_error:
            quotes_error['Function'] = 'list_all_quotes'
            return [], quotes_error

        else:
            try:
                # parse the quotes
                quotes_data = quotes['soap-env:Envelope']['soap-env:Body']['n0:ZbapisdactivequotesResponse'][
                    'Newquotationlistd']['item']
                return quotes_data, {}

            except KeyError as e:
                quotes_error['Function'] = 'list_all_quotes'
                quotes_error['Error'] = f'Unable to parse the quotes from the response. | {e}'
                return [], quotes_error

    @staticmethod
    def _move_up_one_level(data, nested_key='item'):
        """Moves the nested data up one level in the dictionary.

        Args:
            data (dict): The data to consolidate.
            nested_key (str, optional): The key to use as the dictionary key. Defaults to 'item'.

        Returns:
            list[dict]: The refactored data.
        """
        for key, value in data.items():
            if isinstance(value, list) or isinstance(value, dict):
                if nested_key in value:
                    data[key] = data[key].pop(nested_key)

        return data
