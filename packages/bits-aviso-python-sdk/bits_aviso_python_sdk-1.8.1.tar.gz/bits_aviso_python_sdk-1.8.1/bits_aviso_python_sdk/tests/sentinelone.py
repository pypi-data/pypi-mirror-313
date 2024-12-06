import os
from bits_aviso_python_sdk.helpers import initialize_logger
from bits_aviso_python_sdk.services.sentinelone import SentinelOne
from bits_aviso_python_sdk.services.slack import Slack


def test():
	"""Tests the SentinelOne class."""
	logger = initialize_logger()
	token = os.environ.get("SENTINELONE_TOKEN")
	webhook = os.environ.get("SLACK_WEBHOOK_URL")
	slack = Slack(webhook_url=webhook)
	s = SentinelOne(domain='', token=token, alerting=(True, slack))
	# s.get_token_expiration()
	# agents = s.list_agents()


if __name__ == '__main__':
	test()
