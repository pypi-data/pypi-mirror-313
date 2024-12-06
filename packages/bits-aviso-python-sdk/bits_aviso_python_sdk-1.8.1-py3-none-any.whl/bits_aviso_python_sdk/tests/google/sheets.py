from bits_aviso_python_sdk.helpers import initialize_logger
from bits_aviso_python_sdk.services.google.secretmanager import SecretManager
from bits_aviso_python_sdk.services.google.sheets import Sheets


def test():
    """Tests the BigQuery class."""
    logger = initialize_logger()
    sm = SecretManager()
    svc_acc = sm.get_secret('', '')
    ss_id = sm.get_secret('', '')
    s = Sheets(svc_acc)
    spreadsheet_id = s.create_spreadsheet("test-spreadsheet-three")
    print(spreadsheet_id)


if __name__ == '__main__':
    test()
