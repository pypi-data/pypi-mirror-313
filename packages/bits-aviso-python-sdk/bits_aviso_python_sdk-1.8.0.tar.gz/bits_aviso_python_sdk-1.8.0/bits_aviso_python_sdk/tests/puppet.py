from bits_aviso_python_sdk.helpers import initialize_logger
from bits_aviso_python_sdk.helpers.files import write_json
from bits_aviso_python_sdk.services.puppet import Puppet
from bits_aviso_python_sdk.services.google.storage import Storage


def authenticate_puppet():
    st = Storage()
    bucket_name = ''
    key_path = '/tmp/key.pem'
    cert_path = '/tmp/crt.pem'
    ca_path = '/tmp/ca.pem'
    # st.download_blob_to_file(bucket_name, '', key_path)
    # st.download_blob_to_file(bucket_name, '', cert_path)
    # st.download_blob_to_file(bucket_name, '', ca_path)
    p = Puppet(ssl_cert=cert_path, ssl_key=key_path, ssl_verify=ca_path)
    return p


def list_all_facts(p):
    """Lists all the facts."""
    facts = p.list_all_facts()
    write_json(facts, 'all_facts.json')


def list_facts_for_bigquery(p):
    """Lists the facts for BigQuery."""
    facts = p.list_facts_for_bigquery()
    write_json(facts, 'bigquery_facts.json')


def list_hosts(p):
    """Lists all the hosts."""
    hosts = p.list_hosts()
    write_json(hosts, 'hosts.json')


def test():
    """Tests the Puppet class."""
    initialize_logger()
    p = authenticate_puppet()


if __name__ == '__main__':
    test()
