"""
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
"""
import logging
import requests
from datetime import datetime, timezone, timedelta


class SentinelOne:
	"""A class to interact with the SentinelOne API."""
	def __init__(self, domain, token, version='v2.1', alerting=(False, None)):
		"""Initializes the SentinelOne class. Authenticates by generating a token based on the username and password.
		A new token is generated every time the class is called.

		Args:
			domain (str): The basee url for the SentinelOne API.
			token (str): The token to authenticate with.
			version (str, optional): The version of the SentinelOne API to use. Defaults to 'v2.1'.
			alerting (tuple, optional): A tuple containing a boolean indicating whether to alert and Slack object if
			true. Defaults to (False, None).
		"""
		self.domain = domain
		self.version = version
		self.token = token
		self.headers = {
			'Authorization': f'ApiToken {self.token}',
			'Content-Type': 'application/json'
		}
		# check if alerting is enabled
		if alerting[0]:
			self.alerts = alerting[0]  # set alerting flag
			self.slack = alerting[1]  # set slack object

		else:
			self.alerts = alerting[0]

		# check the token's expiration date
		self.check_token_expiration()

	def check_token_expiration(self):
		"""Checks the token's expiration date. If the token is set to expire in a week, it will send an alert if
		alerting is enabled.
		"""
		expiration = self.get_token_expiration()
		if not expiration:
			logging.error('Unable to retrieve token information.')
			return

		# datetime objects
		exp_date = datetime.strptime(expiration, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
		now = datetime.now(timezone.utc)

		# timedelta objects
		limit = timedelta(days=7)  # refresh if its 7 days until expiration
		delta = exp_date - now  # difference in time

		# pretty string of the time remaining
		remaining = str(delta).split(",")[0]

		if delta < limit:  # if there is less than 15 days remaining, refresh
			message = (f"API authentication token expires in {remaining}. Please regenerate and update the token "
					   f"beforehand to prevent later issues.")
			logging.warning(message)
			if self.alerts:
				try:
					self.slack.post_basic_alert({
						"project": __name__,
						"service_name": "SentinelOne",
						"logging_level": "WARNING",
						"message": message
					})
				except ValueError as e:
					logging.error(f'Error sending alert: {e}')

		else:
			logging.info(f'API authentication token expires in {remaining}.')

	def get_token_expiration(self):
		"""Gets the token expiration date from the SentinelOne API."""
		url = f'{self.domain}/web/api/{self.version}/users/api-token-details'

		try:
			payload = {
				"data": {
					"apiToken": self.token
				}
			}
			response = requests.post(url, headers=self.headers, json=payload)
			response.raise_for_status()
			expiration = response.json()['data']['expiresAt']
			return expiration

		except (requests.exceptions.RequestException, KeyError) as e:
			logging.error(f'Error checking token expiration: {e}')
			return

	def list_agents(self, limit=1000):
		"""Lists the agents in SentinelOne based on the given limit.

		Args:
			limit (int, optional): The number of agents to return. Defaults to 1000.

		Returns:
			list(dict): A list of agents in SentinelOne.
		"""
		url = f'{self.domain}/web/api/{self.version}/agents?limit={limit}'
		agents = []

		try:  # initial call in order to get_bucket the cursor
			response = requests.get(url, headers=self.headers)
			response.raise_for_status()  # raise an exception if the status code is not 200
			data = response.json()  # json data
			agents.extend(data['data'])  # add the initial agents to the list
			total = data['pagination']['totalItems']  # total number of agents
			logging.info(f"Retrieving agents from SentinelOne... {len(agents)}/{total}.")

			# if there are more agents to retrieve
			while 'nextCursor' in data['pagination'] and data['pagination']['nextCursor']:
				cursor = data['pagination']['nextCursor']  # get_bucket the cursor
				next_page_url = f'{url}&cursor={cursor}'  # add the cursor to the url
				response = requests.get(next_page_url, headers=self.headers)
				response.raise_for_status()  # raise an exception if the status code is not 200
				data = response.json()  # json data
				agents.extend(data['data'])  # add the agents to the list
				logging.info(f"Retrieving agents from SentinelOne... {len(agents)}/{total}.")

			# return the list of agents
			return agents

		except requests.exceptions.RequestException as e:
			logging.error(f'Error retrieving SentinelOne agents: {e}')
			return

		except (KeyError, AttributeError) as e:  # in case cursor is broken or something
			logging.error(f'Error retrieving cursor for S1 agents: {e}')
			return
