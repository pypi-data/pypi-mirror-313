"""
The `SolidServer` class provides a way to interact with the SolidServer API.

---

## Usage

To use the `EIP` module, you need to initialize the `SolidServer` class and provide the necessary parameters:

```python
from bits_aviso_python_sdk.services.eip.solidserver import SolidServer

ss = SolidServer('ddi.exampledomain.com', 'username', 'password')
```

---

## Dependencies

**External Python Packages:**

- ipaddress
- json
- logging
- math
- requests

**Internal Modules:**

- bits_aviso_python_sdk.helpers

---
"""
import ipaddress
import json
import logging
import math
import requests
from bits_aviso_python_sdk.helpers import auth_basic
from bits_aviso_python_sdk.helpers.aesthetics import progress_bar_search_loop, progress_bar_eta
from bits_aviso_python_sdk.services.eip import payloads, regex_check


class SolidServer:
    """SolidServer class"""

    def __init__(self, url, username, password, populate_data=False, progress_gui=False):
        """Constructor for the SolidServer class

        Args:
            url (str): The base API url for SolidServer. Must include the protocol (http/https).
            username (str): The username to authenticate with.
            password (str): The password to authenticate with.
            populate_data (bool, optional): Whether to populate subnet and ip data from the API. Defaults to False.
            progress_gui (bool, optional): Whether to use a progress bar GUI. Defaults to False.
        """
        self.url = url
        self.domain = url.split('.')[1] + '.' + url.split('.')[2]  # get the domain from the url
        token = auth_basic(username, password)
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {token}"
        }
        self.progress_gui = progress_gui

        if populate_data:
            self.subnets = self.list_subnets()
            self.ip_addresses = self.list_ip_addresses()
        else:
            self.subnets = []
            self.ip_addresses = []

    def check_mac_address(self, mac_address):
        """Check if a MAC address is in use.

        Args:
            mac_address (str): The MAC address to check.

        Returns:
            bool: True if the MAC address is in use, False otherwise.

        Raises:
            ValueError: If no subnet data is provided or stored.
        """
        if self.ip_addresses:  # stored ip data
            logging.info(f"Checking MAC address {mac_address} against stored IP Address data.")
            for ip_chunk in self.ip_addresses:
                for ip in ip_chunk:
                    try:
                        if ip["mac_addr"] == mac_address:
                            logging.info(f"MAC address {mac_address} is in use.")
                            return True

                    except KeyError:
                        continue

            logging.info(f"MAC address {mac_address} is not in use.")
            return False

        else:  # no subnet data
            message = "No IP address data stored in the object. Unable to check MAC address."
            logging.error(message)
            raise ValueError(message)

    def create_host_vm(self, vm_data, subnet_prefix, pxe_server):
        """Create a VM host in SolidServer. `vm_data` should be a dictionary containing the following keys:

        ```json
        vm_data = {
            "name": "hostname",
            "ip": "10.0.0.1"
            "mac_address": "00:00:00:00:00:00",
            "os": "RHEL 8.9",
            "department": "Department Name",
            "purpose": "purpose of creating this vm",
            "assigned_users": ["user1", "user2"],
            "incident": "INC123456"
        }
        ```

        Args:
            vm_data (dict): The data for the VM.
            subnet_prefix (str): The subnet prefix to use for the VM.
            pxe_server (str): The PXE server to use for the VM.

        Returns:
            dict: The payload returned upon successful host creation.

        Raises:
            ValueError: If the subnet is not found.
        """
        # get the subnet data
        subnet = self.get_subnet_data(subnet_prefix)

        if not subnet:  # mission abort
            message = f"Unable to find subnet with prefix {subnet_prefix}. Cannot create VM host."
            logging.error(message)
            raise ValueError(message)

        # get the site id
        site_id = subnet["site_id"]

        # build the payload
        payload = payloads.create_host_vm(vm_data, self.domain, site_id, pxe_server)

        # create the host
        url = f'{self.url}/rest/ip_add'
        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code != 201:
            message = f"Unable to create host. | Error Code {response.status_code}: {response.reason}"
            logging.error(message)
            raise ValueError(message)

        else:
            logging.info(f"Successfully created host {vm_data['name']} with the IP {vm_data['ip']} and MAC address "
                         f"{vm_data['mac_address']} in {self.url}")
            return response.json()

    def ensure_stored_subnet_data(self):
        """Ensures that the subnet data is stored in the object."""
        if not self.subnets:
            self.subnets = self.list_subnets(name_id_only=False)

    def get_ip_address_by_id(self, ip_id, ensure_single_result=True):
        """Gets the IP address data by the IP's SolidServer ID.

        Args:
            ip_id (string): The ID of the IP address to get the data of.
            ensure_single_result (bool, optional): Whether to ensure only a single result is returned. Defaults to True.

        Returns:
            dict: The IP address data.

        Raises:
            ValueError: If no data is found for the IP address with the given ID.
        """
        url = f'{self.url}/rest/ip_address_info?ip_id={ip_id}'
        logging.info(f'Getting data for IP address with the ID {ip_id}...')
        try:
            response = requests.get(url, headers=self.headers)
            response_data = response.json()

            # check if multiple results are found
            if len(response_data) > 1:
                if ensure_single_result:
                    logging.warning(f'Multiple results found for IP address ID {ip_id}. Returning the first result.')
                    return response_data[0]
                else:
                    logging.warning(f'Multiple results found for IP address ID {ip_id}. Returning all results.')
                    return response_data
            else:
                return response_data[0]

        except (json.JSONDecodeError, IndexError, TypeError) as e:
            message = f'No data found for IP address ID {ip_id}. | {e}'
            logging.error(message)
            raise ValueError(message)

    def get_ip_address_data(self, ip_address):
        """Gets the data for the given IP address. It will search through the stored IP data if available.

        Args:
            ip_address (string): The IP address to get the data of.

        Returns:
            dict: The IP address data.

        Raises:
            ValueError: If unable to get IP address data.
        """
        if self.ip_addresses:  # no stored data
            ip_addresses = self.ip_addresses

        else:
            ip_addresses = self.list_ip_addresses(ips_only=False, err_log=False)

        if self.progress_gui:  # use the progress bar
            ip_data = progress_bar_search_loop(ip_address, 'IP Address', 'hostaddr', ip_addresses)
            if not ip_data:  # no data found
                message = f'No data found for IP address {ip_address}.'
                logging.error(message)
                raise ValueError(message)
            # return the data
            return ip_data

        else:  # no progress bar
            # search for the IP address
            for ip_chunk in ip_addresses:
                for ip in ip_chunk:
                    if ip['hostaddr'] == ip_address:
                        return ip

            # no data found
            message = f'No data found for IP address {ip_address}.'
            logging.error(message)
            raise ValueError(message)

    def get_next_free_ip(self, subnet_prefix, ips_only=True, num_addr=1, num_addr_skip=11, pool_name=None,
                         start_addr=None):
        """Gets the next free IP address in the given subnet. Defaults to only returning one address.

        Args:
            subnet_prefix (string): The subnet prefix to get the next free IP from.
            ips_only (bool, optional): Whether to return only the IP addresses or not. Defaults to True.
            num_addr (int, optional): The number of addresses to get. Defaults to 1.
            num_addr_skip (int, optional): The number of addresses to skip. Defaults to 11.
            pool_name (string, optional): The name of the network pool search for the IP address in. Defaults to None.
            start_addr (string, optional): The address to start from. Defaults to None.

        Returns:
            list: The list of free IP addresses.

        Raises:
            ValueError: If unable to get the next free IP address.
        """
        # build the url
        url = f"{self.url}/rpc/ip_find_free_address"

        # get subnet data
        subnet_data = self.get_subnet_data(subnet_prefix)
        if not subnet_data:
            message = 'Unable to get the next free IP address. No subnet data found.'
            logging.error(message)
            raise ValueError(message)

        parameters = {
            "subnet_id": subnet_data['subnet_id'],
            "max_find": str(num_addr),  # cast to string
        }

        # if a pool name is provided, use it
        if pool_name:
            parameters["WHERE"] = f"pool_name='{pool_name}'"

        else:  # if no pool name, just get the next free address
            parameters["WHERE"] = "pool_name is NULL"

        # if a start address is provided, use it
        if start_addr:
            parameters["begin_addr"] = str(ipaddress.IPv4Address(start_addr))

        else:  # if no start address is provided, skip the first 10 addresses
            parameters["begin_addr"] = str(ipaddress.IPv4Address(
                subnet_data['start_hostaddr']) + num_addr_skip)

        try:
            response = requests.request("OPTIONS", url, params=parameters, headers=self.headers)

            # check if only names are needed
            if ips_only:
                ips = []
                for ip in response.json():
                    ips.append(ip['hostaddr'])
                return ips

            # if not just return the response
            return response.json()

        except (json.JSONDecodeError, IndexError, TypeError) as e:
            message = f'Unable to get the next free address(es) in {subnet_prefix} at {self.url} | {e}'
            logging.error(message)
            raise ValueError(message)

    def get_subnet_data(self, subnet_prefix, progress_gui=None):
        """Retrieves the given subnet's information. Subnet prefix must be in the format of x.x.x.x./xx

        Args:
            subnet_prefix (string): The subnet address of the subnet to get the data of.
            progress_gui (bool, optional): Whether to use a progress bar GUI. If no bool is passed the object's
            attribute is used. Defaults to None.

        Returns:
            dict: The subnet's data.
        """
        # make sure there's subnet data to reference
        self.ensure_stored_subnet_data()

        if not progress_gui:  # use the object's progress_gui attribute
            progress_gui = self.progress_gui

        # lets wrangle some strings
        subnet_pattern = r"(\d{1,3}\.){3}\d{1,3}/\d{1,2}"
        if not regex_check(subnet_pattern, subnet_prefix):
            message = f'Invalid subnet address {subnet_prefix}. Must be in the format of "x.x.x.x/xx".'
            logging.error(message)
            raise ValueError(message)

        subnet_data = {}
        if progress_gui:  # use the progress bar
            subnet_data = progress_bar_search_loop(subnet_prefix, 'subnet', 'addr_prefix', self.subnets)

        else:  # no progress bar
            logging.info(f'Getting data for subnet {subnet_prefix}...')
            for subnet in self.subnets:
                if subnet['addr_prefix'] == subnet_prefix:
                    subnet_data = subnet
                    break

        if not subnet_data:
            message = f'No data found for subnet {subnet_prefix}.'
            logging.error(message)
            raise ValueError(message)

        return subnet_data

    def get_subnet_id(self, subnet_prefix, progress_gui=None):
        """Retrieves the given subnet's ID in solidserver. Subnet prefix must be in the format of x.x.x.x./xx

        Args:
            subnet_prefix (string): The address/prefix of the subnet to get the data of.
            progress_gui (bool, optional): Whether to use a progress bar GUI. If no bool is passed the object's
            attribute is used. Defaults to None.

        Returns:
            dict: The subnet's ID.
        """
        # make sure there's subnet data to reference
        self.ensure_stored_subnet_data()

        if not progress_gui:  # use the object's progress_gui attribute
            progress_gui = self.progress_gui

        # lets wrangle some strings
        subnet_pattern = r"(\d{1,3}\.){3}\d{1,3}/\d{1,2}"
        if not regex_check(subnet_pattern, subnet_prefix):
            message = f'Invalid subnet address {subnet_prefix}. Must be in the format of "x.x.x.x/xx".'
            logging.error(message)
            raise ValueError(message)

        subnet_data = {}
        if progress_gui:  # use the progress bar
            subnet_data = progress_bar_search_loop(subnet_prefix, 'subnet', 'addr_prefix', self.subnets)

        else:  # no progress bar
            logging.info(f'Getting ID for subnet {subnet_prefix}...')
            for subnet_data in self.subnets:
                if subnet_data['addr_prefix'] == subnet_prefix:
                    return subnet_data['subnet_id']

        if not subnet_data:
            message = f'No data found for subnet {subnet_prefix}.'
            logging.error(message)
            raise ValueError(message)

        return subnet_data['subnet_id']

    def list_ip_addresses(self, ips_only=True, err_log=True, progress_gui=None):
        """Lists the all the IP addresses in solidserver. It loops through all the subnets and retrieves the IP
        addresses in each one.

        If ips_only is set to False, all the data associated with the IP is returned.
        If err_log is set to False, errors are not logged.

        Args:
            ips_only (bool, optional): A flag to denote if only the IPs are needed. Defaults to True.
            err_log (bool, optional): A flag to denote if errors should be logged. Defaults to True.
            progress_gui (bool, optional): A flag to denote if a progress bar GUI should be used. If no bool is passed

        Returns:
            list: The list of IP addresses.
        """
        # make sure there's subnet data to reference
        self.ensure_stored_subnet_data()

        # init variables
        ip_addresses = []  # home for the ips
        if not progress_gui:  # use the object's progress_gui attribute
            progress_gui = self.progress_gui

        # build the url
        url = f"{self.url}/rest/ip_address_list"

        logging.info('Retrieving all IP addresses...')

        if progress_gui:  # use the progress bar
            bar = progress_bar_eta(len(self.subnets))
            i = 0  # counter for progress bar

        for subnet in self.subnets:
            call_url = url + f'?WHERE=subnet_id={subnet["subnet_id"]}'

            try:
                response = requests.get(call_url, headers=self.headers)
                if ips_only:  # check if ips only
                    for ip in response.json():
                        ip_addresses.append(ip['hostaddr'])

                else:  # return all the data
                    ip_addresses.append(response.json())

                if progress_gui:  # update the progress bar
                    i += 1
                    bar.update(i)

            except (json.JSONDecodeError, IndexError, TypeError) as e:
                if err_log:
                    logging.error(f'Unable to list the IP addresses in {subnet["subnet_prefix"]} at'
                                  f' {self.url}. | {e}')
                else:
                    continue

                if progress_gui:  # update the progress bar
                    i += 1
                    bar.update(i)

        if progress_gui:  # cleanse the bar
            bar.finish()
            print()

        return ip_addresses

    def list_ip_addresses_from_subnet(self, subnet_prefix, ips_only=True):
        """Lists the IP addresses in the given subnet. If ips_only is set to False, it will return all the data
        associated with the IP. Subnet prefix must be in the format of x.x.x.x./xx

        Args:
            subnet_prefix (string): The prefix of the subnet to list the IP addresses from.
            ips_only (bool, optional): A flag to denote if only the IPs are needed. Defaults to True.

        Returns:
            list: The list of IP addresses.

        Raises:
            ValueError: If unable to list the IP addresses in the given subnet.
        """
        # init variables
        ip_addresses = []

        # build url
        url = f"{self.url}/rest/ip_address_list?WHERE=subnet_id={self.get_subnet_id(subnet_prefix)}"

        logging.info(f'Retrieving IP addresses in {subnet_prefix}...')

        try:
            response = requests.get(url, headers=self.headers)

            # check if ips only
            if ips_only:
                for ip in response.json():  # type: ignore
                    ip_addresses.append(ip['hostaddr'])

                return ip_addresses

            else:  # return all the data
                return response.json()  # type: ignore

        except (json.JSONDecodeError, IndexError, TypeError) as e:
            logging.error(f'Unable to list the IP addresses in {subnet_prefix} in {self.url}. | {e}')
            raise ValueError

    def list_subnets(self, name_id_only=True):
        """Lists the subnets in SolidServer. If name_id_only is set to False, all the data associated with the subnet
        will be returned.

        It also manually calculates the cidr for each subnet and adds it to the data along with the subnet address
        prefix. This skips the subnets without a subnet size.

        Args:
            name_id_only (bool, optional): A flag to denote if only the names and IDs are needed. Defaults to True.

        Returns:
            list: The list of subnets.
        """
        url = f"{self.url}/rest/ip_block_subnet_list"
        logging.info('Retrieving all subnet data...')

        try:
            response = requests.get(url, headers=self.headers)
            # calculate the cidr and add it to the dict
            subnet_data = []
            for subnet in response.json():  # type: ignore
                subnet_size = int(subnet['subnet_size'])
                if subnet_size > 0:  # skip the ones without a subnet size
                    # calculate cidr and compile the address prefix
                    subnet['cidr'] = int(32 - math.log2(subnet_size))
                    subnet['addr_prefix'] = subnet['start_hostaddr'] + '/' + str(subnet['cidr'])

                    # check if only names and id are needed
                    if name_id_only:
                        subnet_names = [{
                            "subnet_prefix": subnet['subnet_prefix'],
                            "subnet_id": subnet['subnet_id'],
                            "subnet_addr_prefix": subnet['start_hostaddr'] + '/' + str(subnet['cidr'])
                        }]
                        return subnet_names

                    subnet_data.append(subnet)

                else:
                    continue

            # if not return it all
            return subnet_data

        except (json.JSONDecodeError, IndexError, TypeError) as e:
            logging.error(
                f'Unable to retrieve the subnet data in {self.url}. | {e} | Exiting...')
            exit()

    def refresh_all_data(self):
        """Refreshes the stored subnet and ip address data in the SolidServer object."""
        logging.info('Refreshing all data...')
        self.subnets = self.list_subnets(name_id_only=False)
        self.ip_addresses = self.list_ip_addresses(ips_only=False, err_log=False)

    def refresh_ip_data(self):
        """Refreshes the IP data stored in the SolidServer object."""
        logging.info('Refreshing IP data...')
        self.ip_addresses = self.list_ip_addresses(ips_only=False, err_log=False)

    def refresh_subnet_data(self):
        """Refreshes the subnet data stored in the Solidserver object."""
        logging.info('Refreshing subnet data...')
        self.subnets = self.list_subnets(name_id_only=False)

    def update_dhcp_options_by_host(self, ip_id, dhcp_options):
        """Updates the DHCP options for the given host.

        Args:
            ip_id (string): The SolidServer IP ID of the host to update the DHCP options for.
            dhcp_options (dict): The DHCP options to update.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        # get the host data
        host_data = self.get_ip_address_by_id(ip_id)
        if not host_data:
            return

        # set host data variables
        dhcphost_id = host_data['dhcphost_id']
        ip = host_data['hostaddr']
        hostname = host_data['name'].split('.')[0]

        # build the payload
        parameters = {
            "dhcphost_id": dhcphost_id,
            "dhcphost_name": hostname,
            "dhcpoption_type": "host",
            "hostaddr": ip,
        }
        logging.info(f'Updating the DHCP options for the host {hostname}...')

        # build the url
        url = f"{self.url}/rest/dhcp_option_add"

        for name, value in dhcp_options.items():
            parameters["dhcpoption_name"] = f'option server.{name}'
            parameters["dhcpoption_value"] = value

            response = requests.post(url, headers=self.headers, data=parameters)
            if response.status_code != 201:  # type: ignore
                logging.error(f'Unable to update DHCP option [{name}: {value}] for {ip}.'
                              f'| {response.status_code}: {response.text}')  # type: ignore
                return False

            else:
                logging.info(
                    f'Updated DHCP option [{name}: {value}] for {ip}.')

        return True
