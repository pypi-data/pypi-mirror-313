from bits_aviso_python_sdk.services.sap import SAP
from bits_aviso_python_sdk.helpers.files import write_json


def test():
    """Test the SAP class."""
    sap = SAP('', '')
    write_json(sap.get_quote_details('')[0], 'quote_details.json')


if __name__ == '__main__':
    test()
