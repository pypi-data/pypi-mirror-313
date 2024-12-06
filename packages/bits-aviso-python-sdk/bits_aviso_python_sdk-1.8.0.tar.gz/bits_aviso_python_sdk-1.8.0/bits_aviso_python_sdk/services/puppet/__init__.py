"""
The `puppet` module provides a set of tools to interact with Puppet servers and manage configurations
using the pypuppetdb library.

---

## Installation

To install the `puppet` module, use `pip`:

```sh
pip install bits_aviso_python_sdk
```

---

## Usage

### Initialization

To use the `puppet` module, you need to initialize the `Puppet` class with the necessary parameters:

```python
from bits_aviso_python_sdk.services.puppet import Puppet

puppet = Puppet(server='puppet_server', username='username', password='password')
```

### Examples

---

#### Get All Nodes

Retrieve all nodes managed by the Puppet server:

```python
all_nodes, errors = puppet.get_all_nodes()
print(all_nodes)
print(errors)
```

---

#### Get Node Details

Retrieve details for a specific node:

```python
node_details, error = puppet.get_node_details('node_name')
print(node_details)
print(error)
```

---

#### Update Node Configuration

Update the configuration for a specific node:

```python
updated_node, error = puppet.update_node_configuration('node_name', configuration_data)
print(updated_node)
print(error)
```

## Error Handling

The `puppet` module handles errors by logging each error encountered during the execution of methods. Methods will
return None every time an error occurs.

---
"""
import datetime
import logging
import pypuppetdb
import requests
import ssl


class Puppet:
    """The Puppet class."""
    def __init__(self, hostname, port=8081, ssl_cert=None, ssl_key=None, ssl_verify=None):
        """Initializes the Puppet class. Uses ssl certs for authentication.

        Args:
            hostname (str): The hostname of the PuppetDB server.
            port (int, optional): The port of the PuppetDB server. Defaults to 8081.
            ssl_cert (str, optional): The path to the SSL certificate. Defaults to None.
            ssl_key (str, optional): The path to the SSL key. Defaults to None.
            ssl_verify (str, optional): The path to the SSL verify. Defaults to None.
        """
        self.database = pypuppetdb.connect(
            host=hostname,
            port=port,
            ssl_key=ssl_key,
            ssl_cert=ssl_cert,
            ssl_verify=ssl_verify
        )
        ssl.SSLContext.hostname_checks_common_name = True

    @staticmethod
    def _convert_nested_dicts_to_list(nested_dict, nested_key_name='name'):
        """Converts nested dictionaries to a list of dictionaries.

        Args:
            nested_dict (dict): The nested dictionary to convert.
            nested_key_name (str, optional): The name of the key for the nested dictionary. Defaults to 'name'.

        Returns:
            list(dict): A list of dictionaries.
        """
        try:
            list_data = []
            for key, values in nested_dict.items():
                key_data = {nested_key_name: key}
                try:
                    key_data.update(values)

                except TypeError:
                    key_data.update({key: values})

                list_data.append(key_data)

            return list_data

        except AttributeError as e:
            logging.error(f"Unable to convert nested dictionaries to a list of dictionaries: {e}")
            return

    def list_all_facts(self):
        """Lists all the facts in PuppetDB for every host.

        Returns:
            list(dict): A list of dictionaries with node names as keys and their facts as values.
        """
        facts_data = []
        try:
            node_facts = {}
            logging.info('Listing all facts for all the hosts in PuppetDB...')
            for fact in self.database.facts():
                if fact.node not in node_facts:  # if we havent seen this node before
                    node_facts[fact.node] = {}  # create a new dictionary for the node

                node_facts[fact.node][fact.name] = fact.value  # add the fact to the node's data

            for node, facts in node_facts.items():  # add the node data to the list
                facts_data.append(facts)

            logging.info(f'Found facts for {len(facts_data)} hosts.')
            return facts_data

        except (AttributeError, KeyError, IndexError) as e:
            logging.error(f"Unable to list all the facts: {e}")
            return

        except requests.exceptions.ConnectTimeout as e:
            logging.error(f"Connection to PuppetDB timed out: {e}")
            return

    def list_facts_for_bigquery(self, desired_facts=None):
        """Lists all the facts in PuppetDB for every host except its specific data we want for bigquery.

        Args:
            desired_facts (list, optional): The list of facts to return. Defaults to None.

        Returns:
            list(dict): A list of dictionaries containing facts.
        """
        # set default facts
        if desired_facts is None:
            desired_facts = ['disks', 'fips_enabled', 'is_virtual' 'kernel', 'kernelmajversion', 'kernelrelease',
                             'kernelversion', 'load_averages', 'memory', 'mountpoints', 'networking', 'os', 'partitions',
                             'ssh', 'timezone', 'virtual']

        facts_data = []
        try:
            node_facts = {}
            logging.info('Listing all facts for all the hosts in PuppetDB...')
            for fact in self.database.facts():
                if fact.node not in node_facts:  # if we havent seen this node before
                    node_facts[fact.node] = {}  # create a new dictionary for the node
                    node_facts[fact.node]['node'] = fact.node  # add the node name to the data

                if fact.name not in desired_facts:  # skip
                    continue

                elif fact.name == 'networking':
                    networking_data = self._refactor_networking_fact(fact.value)
                    node_facts[fact.node][fact.name] = networking_data

                elif fact.name == 'os':
                    node_facts[fact.node][fact.name] = fact.value

                elif isinstance(fact.value, dict):  # if the fact value is a dictionary
                    new_value = self._convert_nested_dicts_to_list(fact.value)  # convert the nested dict to a list
                    node_facts[fact.node][fact.name] = new_value  # add the fact to the node's data

                else:
                    node_facts[fact.node][fact.name] = fact.value  # add the fact to the node's data

            for node, facts in node_facts.items():  # add the node data to the list
                facts_data.append(facts)

            logging.info(f'Found facts for {len(facts_data)} hosts.')
            return facts_data

        except (AttributeError, KeyError, IndexError) as e:
            logging.error(f"Unable to list all the facts: {e}")
            return

        except requests.exceptions.ConnectTimeout as e:
            logging.error(f"Connection to PuppetDB timed out: {e}")
            return

    def list_hosts(self):
        """Lists all the hosts in PuppetDB.

        Returns:
            list(str): A list of host names.
        """
        try:
            logging.info('Listing all hosts in PuppetDB...')
            hosts = []
            for host in self.database.nodes():
                host_dict = {}
                for key, value in host.__dict__.items():
                    if isinstance(value, datetime.datetime):
                        host_dict[key] = value.isoformat()

                    elif key == '_Node__api':
                        continue

                    else:
                        host_dict[key] = value

                hosts.append(host_dict)

            logging.info(f'Found {len(hosts)} hosts.')

            return hosts

        except (AttributeError, KeyError, IndexError) as e:
            logging.error(f"Unable to list hosts: {e}")
            return

        except requests.exceptions.ConnectTimeout as e:
            logging.error(f"Connection to PuppetDB timed out: {e}")
            return

    def _refactor_networking_fact(self, networking_facter):
        """Refactors the networking facter data from a multi-level dictionary to a list of dictionaries.

        Args:
            networking_facter (dict): The networking facter data.

        Returns:
            list(dict): A list of dictionaries containing networking data.
        """
        try:
            refactored_data = {}
            for key, value in networking_facter.items():
                if key == 'interfaces':  # refactor interfaces into a list of dicts
                    interfaces = self._convert_nested_dicts_to_list(value)
                    refactored_data[key] = interfaces

                else:  # business as usual
                    refactored_data[key] = value

                # add the refactored data to the list

            return [refactored_data]

        except AttributeError as e:
            logging.error(f"Unable to refactor networking facter data: {e}")
            return
