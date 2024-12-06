# EIP
The EIP module provides a way to interact with EIP products.
The main service is SolidServer. It leverages the SolidServer API to perform various operations against it.

---

## Dependencies

**External Python Packages:**

- re

---

## Installation

To install the `eip` module you must install `bits-aviso-python-sdk`, use `pip`:

```sh
pip install bits_aviso_python_sdk
```

---

## SolidServer

The `SolidServer` class provides a way to interact with the SolidServer API.

---

## Usage

To use the `EIP` module, you need to initialize the `SolidServer` class and provide the necessary parameters:

```python
from bits_aviso_python_sdk.services.eip.solidserver import SolidServer

ss = SolidServer('ddi.exampledomain.com', 'username', 'password')
```

---

## Dependencies

**External Python Packages:**

- ipaddress
- json
- logging
- math
- requests

**Internal Modules:**

- bits_aviso_python_sdk.helpers

---

# Payloads

The `payloads` module is used to build the payload that will be sent to the SolidServer API.
This helps to keep the code clean and allows for easy customization of the payload, along with maintaining consistency with the payload format.

---

## Dependencies

**External Python Packages:**

- ipaddress

**Internal Modules**

- bits_aviso_python_sdk.services.eip

---
