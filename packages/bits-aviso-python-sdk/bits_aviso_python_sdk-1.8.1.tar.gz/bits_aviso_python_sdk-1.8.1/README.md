# bits-aviso-python-sdk
Repository containing python wrappers to various services Team AVISO develops against.

[Link to Documentation](https://legendary-adventure-kgmn2m7.pages.github.io/)

---

## Installation
To install the SDK, you can use pip:
```bash
pip install bits-aviso-python-sdk
```

---
## Usage
Here is a simple example of how to use the SDK:
```python
from bits_aviso_python_sdk import ServiceName

service = ServiceName(username='username', password='password')  # Initialize the service
response = service.some_method()
print(response)
```
However, please refer to the documentation for each service for more specific parameters and methods.

---

## Sub Modules
There are three upper-level modules in this SDK:

### helpers
> Helpers are utility functions that assist with various tasks within the SDK.
They can also be used independently of the services. Functions that are commonly used will be included here.

Please see the documentation under `bits-aviso-python-sdk.helpers` for more information.

### services
> Services are the main components of the SDK. Each service corresponds to a specific functionality leveraged by
Team AVISO.

Please see the documentation under `bits-aviso-python-sdk.services` for more information.

### tests
> Tests are included to ensure the functionality of the SDK.
They can be run to verify that the SDK is working as expected.
>
> However, these are not proper unit tests and are a work in progress.

Please see the documentation under `bits-aviso-python-sdk.tests` for more information.

---
