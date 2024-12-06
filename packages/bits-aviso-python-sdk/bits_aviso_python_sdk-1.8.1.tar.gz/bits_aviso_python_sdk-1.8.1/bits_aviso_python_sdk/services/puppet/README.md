# puppet

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
