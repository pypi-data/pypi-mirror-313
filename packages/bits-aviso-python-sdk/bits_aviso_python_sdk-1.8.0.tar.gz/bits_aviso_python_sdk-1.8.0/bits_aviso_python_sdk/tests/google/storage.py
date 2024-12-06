from bits_aviso_python_sdk.helpers import initialize_logger
from bits_aviso_python_sdk.services.google.storage import Storage


def test():
    """Tests the Pubsub class."""
    logger = initialize_logger()
    s = Storage()
    s.upload("", "", "", "")


if __name__ == '__main__':
    test()
