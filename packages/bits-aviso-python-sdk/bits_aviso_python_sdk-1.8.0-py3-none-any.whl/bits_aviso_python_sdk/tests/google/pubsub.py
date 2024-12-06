from bits_aviso_python_sdk.helpers import initialize_logger
from bits_aviso_python_sdk.services.google.pubsub import Pubsub


def test():
	"""Tests the Pubsub class."""
	logger = initialize_logger()
	p = Pubsub("")
	p.send("", "", {})


if __name__ == '__main__':
	test()
