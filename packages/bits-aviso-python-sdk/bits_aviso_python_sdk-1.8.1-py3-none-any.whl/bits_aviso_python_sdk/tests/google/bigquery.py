from bits_aviso_python_sdk.helpers import initialize_logger
from bits_aviso_python_sdk.services.google.bigquery import BigQuery


def test():
    """Tests the BigQuery class."""
    logger = initialize_logger()
    bq = BigQuery()
    query = bq.query("")
    print(query)


if __name__ == '__main__':
    test()
