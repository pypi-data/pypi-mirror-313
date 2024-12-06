import json
import requests
import unittest
from unittest.mock import patch, MagicMock
from bits_aviso_python_sdk.services.slack import Slack


class TestSlack(unittest.TestCase):
    """Unit Tests for the Slack class"""

    def setUp(self):
        """Set up test fixtures."""
        self.webhook_url = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
        self.slack = Slack(webhook_url=self.webhook_url)
        self.payload = {
            "text": "Test message"
        }

    @patch('bits_aviso_python_sdk.services.slack.requests.post')
    def test_post_success(self, mock_post):
        """Test the post method for a successful request."""
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        result = self.slack.post(self.payload)
        self.assertTrue(result)
        mock_post.assert_called_once_with(
            self.webhook_url,
            data=json.dumps(self.payload),
            headers={'Content-Type': 'application/json'}
        )

    @patch('bits_aviso_python_sdk.services.slack.requests.post')
    def test_post_failure(self, mock_post):
        """Test the post method for a failed request."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Error")
        mock_post.return_value = mock_response

        result = self.slack.post(self.payload)
        self.assertFalse(result)
        mock_post.assert_called_once_with(
            self.webhook_url,
            data=json.dumps(self.payload),
            headers={'Content-Type': 'application/json'}
        )

    @patch('bits_aviso_python_sdk.services.slack.payload_builder.basic_alert')
    @patch('bits_aviso_python_sdk.services.slack.Slack.post')
    def test_post_basic_alert(self, mock_post, mock_basic_alert):
        """Test the post_basic_alert method."""
        data = {
            "project": "project-name",
            "service_name": "service-name",
            "logging_level": "logging-level",
            "message": "message"
        }
        mock_basic_alert.return_value = self.payload
        mock_post.return_value = True

        result = self.slack.post_basic_alert(data)
        self.assertTrue(result)
        mock_basic_alert.assert_called_once_with(data)
        mock_post.assert_called_once_with(self.payload)

    @patch('bits_aviso_python_sdk.services.slack.payload_builder.cloud_function')
    @patch('bits_aviso_python_sdk.services.slack.Slack.post')
    def test_post_cloud_function_alert(self, mock_post, mock_cloud_function):
        """Test the post_cloud_function_alert method."""
        data = {
            "project_id": "project_id",
            "function_name": "function_name",
            "logging_level": "logging_level",
            "message": "message"
        }
        mock_cloud_function.return_value = self.payload
        mock_post.return_value = True

        result = self.slack.post_cloud_function_alert(data)
        self.assertTrue(result)
        mock_cloud_function.assert_called_once_with(data)
        mock_post.assert_called_once_with(self.payload)


def test():
    gcp_project = ''
    secret_name = ''
    secret_version = ''
    slack = Slack(gcp_webhook=(gcp_project, secret_name, secret_version))
    data = {
        "project": "bits-aviso-python-sdk",
        "service_name": "slack",
        "logging_level": "ERROR",
        "message": "testing slack module"
    }
    result = slack.post_basic_alert(data)
    print(result)


if __name__ == '__main__':
    test()
