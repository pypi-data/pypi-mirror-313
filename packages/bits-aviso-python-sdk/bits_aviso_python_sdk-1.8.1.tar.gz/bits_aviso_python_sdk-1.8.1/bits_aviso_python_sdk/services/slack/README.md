# slack

The slack module allows you to send messages to a slack channel using a provided webhook url, or it can grab a webhook
from secret manager if a tuple containing the gcp project, secret name, and secret version is provided.

---

## Usage
Below is an example of how to use the slack module to send a cloud function error alert to a slack channel.

```python
from bits_aviso_python_sdk.services.slack import Slack
from bits_aviso_python_sdk.services.slack import payloads

# intializing the slack object with a webhook url
example_with_webhook_url = Slack(webhook_url="https://hooks.slack.com/services/XXXXX/XXXXX/XXXXX")

# initializing the slack object with a webhook stored in gcp's secret manager
slack = Slack(gcp_webhook=("gcp-project", "secret-name", "secret-version"))

# prep data dictionary for cloud function alerts
data = {
    "project_id": "google-project-name",
    "function_name": "cloud-function-name",
    "logging_level": "ERROR",
    "message": "this is a test alert message"
}

# build cloud function payload
payload = payloads.cloud_function(data)

# sending a message to the slack channel
slack.post(payload)
```

---

# payloads
The `payloads` module is used to build the payload that will be sent to the slack channel. This helps to keep the
code clean and allows for easy customization of the payload, along with maintaining consistency with the payload format.

---

### Basic Alert
The `basic_alert` function is used to build the payload for common alerts.
It takes in a dictionary containing the following keys: `project`, `service_name`, `logging_level`, and `message`.

- The `project` is the name of the project where the alert was triggered.
- The `service_name` is the name of the service that triggered the alert.
- The `logging_level` is the level of the log message for the alert.
- The `message` is the message that you would like to alert.

### Cloud Function Alert
The `cloud_function_alert` function is used to build the payload for cloud function alerts. It takes in a dictionary
containing the following keys: `project_id`, `function_name`, `logging_level`, and `message`.

- The `project_id` is the name of the project where the cloud function is deployed.
- The `function_name` is the name of the cloud function that triggered the alert.
- The `logging_level` is the level of the log message for the alert.
- The `message` is the message that you would like to alert.

---
