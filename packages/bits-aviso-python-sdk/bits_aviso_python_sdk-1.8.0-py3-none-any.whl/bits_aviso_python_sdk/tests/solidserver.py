import os
from bits_aviso_python_sdk.services.eip.solidserver import SolidServer
from bits_aviso_python_sdk.helpers.files import write_json


def test():
    """Test the SAP class."""
    username = os.environ.get('SS_USERNAME')
    password = os.environ.get('SS_PASSWORD')
    ss = SolidServer('https://ddi.broadinstitute.org', username, password)
    #ss.subnets = ss.list_subnets(name_id_only=False)
    #write_json(ss.subnets, 'subnets.json')
    #ss.ip_addresses = ss.list_ip_addresses(ips_only=False, progress_gui=True, err_log=False)
    #print(ss.check_mac_address('00:50:56:90:03:19'))
    #print(ss.get_next_free_ip('10.200.0.0/16', num_addr_skip=0, pool_name='1SS-SERVERS'))
    print(ss.list_ip_addresses_from_subnet('10.200.0.0/16'))


if __name__ == '__main__':
    test()
