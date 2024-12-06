"""
This module provides a class to interact with Google Cloud Secret Manager. If no service account credentials are
provided, the SDK will attempt to use the default credentials.

## Usage
The following is an example of how to access a secret from Secret Manager:

```python
from bits_aviso_python_sdk.services.google.secretmanager import SecretManager

# initialize Secret Manager client
secret_manager_client = SecretManager()

# get secret
secret = secret_manager_client.get_secret("project_id", "your_secret_name")
print(secret)
```

---
"""

import json
import logging
import google.auth.exceptions
import google.api_core.exceptions
from google.cloud import secretmanager
from bits_aviso_python_sdk.services.google import authenticate_google_service_account


class SecretManager:
	"""SecretManager class to interface with Google's Secret Manager API."""

	def __init__(self, service_account_credentials=None):
		"""Initializes the SecretManager class. If service account credentials are not provided,
		the credentials will be inferred from the environment.

		Args:
			service_account_credentials (dict, str, optional): The service account credentials in json format
			or the path to the credentials file. Defaults to None.
		"""
		self.client = secretmanager.SecretManagerServiceClient()

		if service_account_credentials:
			credentials = authenticate_google_service_account(service_account_credentials)
			self.client = secretmanager.SecretManagerServiceClient(credentials=credentials)
		else:
			try:
				self.client = secretmanager.SecretManagerServiceClient()

			except google.auth.exceptions.DefaultCredentialsError as e:
				logging.error(f"Unable to authenticate service account. {e}")
				self.publisher_client = None

	def add_secret_version(self, project_id, secret_name, payload):
		"""Adds a new version to an existing secret.

		Args:
			project_id (string): The project id of the secret.
			secret_name (string): The name of the secret.
			payload (string): The secret data to add.

		Returns:
			str: The name of the new secret version.
		"""
		try:
			secret = self.client.secret_path(project_id, secret_name)
			payload = payload.encode("UTF-8")
			response = self.client.add_secret_version(parent=secret, payload={"data": payload})

			return response.name

		except (google.api_core.exceptions.NotFound, google.api_core.exceptions.InvalidArgument) as e:
			message = f'Unable to add a new version to the secret {secret_name}. {e} '
			logging.error(message)

	def get_secret(self, project_id, secret_name, secret_version="latest"):
		"""Gets the secret data from secret manager.

		Args:
			project_id (string): The project id of the secret.
			secret_name (string): The name of the secret.
			secret_version (string, optional): The version of the secret. Defaults to "latest".

		Returns:
			str, dict: The secret data from secret manager.
		"""
		try:
			secret = self.client.secret_version_path(project_id, secret_name, secret_version)
			response = self.client.access_secret_version(request={"name": secret})

			try:  # try to parse the secret data as json
				secret_data = json.loads(response.payload.data.decode("UTF-8"))

			except json.JSONDecodeError:  # if it fails, return the data as is
				secret_data = response.payload.data.decode("UTF-8")

			return secret_data

		except (google.api_core.exceptions.NotFound, google.api_core.exceptions.InvalidArgument) as e:
			message = f'Unable to get the secret {secret_name} from secret manager. {e} '
			logging.error(message)  # logging message

			raise ValueError(message)  # raise an error with the message
