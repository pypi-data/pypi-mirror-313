"""
This module provides a class to interact with Google Cloud Pub/Sub.
If no service account credentials are provided, the SDK will attempt to use the default credentials.

## Usage
The following is an example of how to send a message to a Pub/Sub topic:

```python
from bits_aviso_python_sdk.services.google.pubsub import Pubsub

# service account credentials
service_account = {
    "type": "service_account",
    "project_id": "your_project_id",
    "private_key_id": "your_private_key_id",
    "private_key": "-----BEGIN PRIVATE KEY-----\nyour_private_key\n-----END PRIVATE KEY-----\n",
    "client_email": "your_service_account_email",
    "client_id": "your_client_id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your_service_account_email"
}

# Initialize Pub/Sub client
pubsub_client = Pubsub(service_account_credentials=service_account)

# pubsub message contents
message = {
    "message": "Hello, World!"
}
# Send a message to a Pub/Sub topic
pubsub_client.send("project_id", "your_topic_name", message)
```

---
"""

import json
import logging
import google.auth.exceptions
from google.cloud import pubsub
from bits_aviso_python_sdk.services.google import authenticate_google_service_account


class Pubsub:
	"""Pubsub class for sending messages to a given pubsub topic."""

	def __init__(self, service_account_credentials=None):
		"""Initializes the Pubsub class. If service account credentials are not provided,
		the credentials will be inferred from the environment.

		Args: service_account_credentials (dict, str, optional): The service account credentials in json format or the
		path to the credentials file. Defaults to None.
		"""
		if service_account_credentials:
			credentials = authenticate_google_service_account(service_account_credentials)
			self.publisher_client = pubsub.PublisherClient(credentials=credentials)
		else:
			try:
				self.publisher_client = pubsub.PublisherClient()
			except google.auth.exceptions.DefaultCredentialsError as e:
				logging.error(f"Unable to authenticate service account. {e}")
				self.publisher_client = None

	def send(self, project_id, topic_name, message):
		"""Publishes a message to a topic.

		Args:
			project_id (str): The project id of the pubsub topic.
			topic_name (str): The name of the pubsub topic.
			message (dict): The message body to post to the pubsub topic.
		"""
		try:
			topic_uri = self.publisher_client.topic_path(project_id, topic_name)
			logging.info(f"Attempting to publish message to {topic_name} in project {project_id}.")
			publish_future = self.publisher_client.publish(topic_uri, data=json.dumps(message, default=str).encode("utf-8"))
			publish_future.result()
			logging.info(f"Published message to {topic_name} in project {project_id}.")

		except AttributeError as e:
			logging.error(f"Unable to publish message to {topic_name} in project {project_id}. {e}")
