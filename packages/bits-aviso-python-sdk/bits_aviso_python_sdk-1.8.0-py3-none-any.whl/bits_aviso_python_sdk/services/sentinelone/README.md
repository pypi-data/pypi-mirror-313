# SentinelOne

The `sentinelone` module provides a set of tools to interact with SentinelOne services.

---

## Installation

To install the `sentinelone` module, use `pip`:

```sh
pip install bits_aviso_python_sdk
```

---

## Usage

### Initialization

To use the `sentinelone` module, you need to initialize the `SentinelOne` class with the necessary parameters:

```python
from bits_aviso_python_sdk.services.sentinelone import SentinelOne

sentinelone = SentinelOne(api_token='your_api_token', base_url='https://your.sentinelone.instance')
```

### Examples

---

#### Get All Agents

Retrieve all agents managed by the SentinelOne instance:

```python
all_agents, errors = sentinelone.get_all_agents()
print(all_agents)
print(errors)
```

---

#### Get Agent Details

Retrieve details for a specific agent:

```python
agent_id = 'agent_id'
agent_details, error = sentinelone.get_agent_details(agent_id)
print(agent_details)
print(error)
```

---

#### Update Agent Configuration

Update the configuration for a specific agent:

```python
agent_id = 'agent_id'
configuration_data = {'key': 'value'}
updated_agent, error = sentinelone.update_agent_configuration(agent_id, configuration_data)
print(updated_agent)
print(error)
```

---

## Error Handling

Each method logs errors as they occur and returns `None` instead of the expected data type.

---
