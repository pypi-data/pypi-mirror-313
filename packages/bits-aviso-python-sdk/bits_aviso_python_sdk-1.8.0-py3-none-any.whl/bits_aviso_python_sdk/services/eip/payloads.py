"""
The `payloads` module is used to build the payload that will be sent to the SolidServer API.
This helps to keep the code clean and allows for easy customization of the payload, along with maintaining consistency with the payload format.

---

## Dependencies

**External Python Packages:**

- ipaddress

**Internal Modules**

- bits_aviso_python_sdk.services.eip

---
"""
import ipaddress
from bits_aviso_python_sdk.services.eip import convert_class_parameters


def create_host_vm(vm_data, domain, site_id, pxe_server):
    """Builds the payload to create a vm host using the SolidServer API.
    Args:
        vm_data (dict): The data for the VM.
        domain (str): The domain to use for the VM.
        site_id (int): The site ID to use for the VM.
        pxe_server (str): The PXE server to use for the VM.

    Returns:
        dict: The payload needed to create a vm host.
    """
    # parse the vm data
    try:
        name = vm_data['name']
        ip = vm_data['ip']
        mac_address = vm_data['mac_address']
        os = vm_data['os']
        department = vm_data['department']
        purpose = vm_data['purpose']
        assigned_users = vm_data['assigned_users']
        incident = vm_data['incident']

    except KeyError as e:
        raise ValueError(f'VM data missing required key: {e}. Unable to create host.')

    # get the os string for the mhl entry
    rhel_os = f'rhel{os.split(" ")[-1].split(".")[0]}'

    # build the notes
    if incident:
        notes = f"{purpose}, {assigned_users}, ({incident})"
    else:
        notes = f"{purpose}, {assigned_users}"

    # build the payload
    payload = {

        "hostaddr": str(ipaddress.IPv4Address(ip)),
        "site_id": site_id,
        "name": f"{name}.{domain}",
        "mac_addr": mac_address,
        "ip_class_parameters": convert_class_parameters({  # convert it to a stringy string string cos the api is weird
            "bi_mhl_tag": f"runaround|linux|redhat|{rhel_os}|x86_64|1ss|pxe_server={pxe_server}|pxe=pxelinux.0",
            "bi_device_type": "unix_svr",
            "bi_notes": notes,
            "bi_department_lab": department,
            "hostname": name,
            "domain:": domain,
            "dhcp_static": "1",
            "persistent_dns_rr": "1",
            "update_dns": "1",
            "use_ipam_name": "1",
        })
    }

    return payload
