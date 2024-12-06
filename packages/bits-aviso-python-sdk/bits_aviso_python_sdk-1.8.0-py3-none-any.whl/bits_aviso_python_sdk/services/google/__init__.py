"""
The google module submodules to interact with the various Google services.

---

## Usage
The following example demonstrates how to use the function to authenticate using a Google service account:
```python
from bits_aviso_python_sdk.services.google import authenticate_google_service_account

# service account credentials
service_account = {
    "type": "service_account",
    "project_id": "your_project_id",
    "private_key_id": "your_private_key_id",
    "private_key": "-----BEGIN PRIVATE KEY-----\nyour_private_key\n-----END PRIVATE KEY-----\n",
    "client_email": "your_service_account_email",
    "client_id": "your_client_id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your_service_account_email"
}

# Authenticate using a service account
credentials = authenticate_google_service_account(service_account)
```

---
"""

import logging
from google.oauth2 import service_account


def authenticate_google_service_account(service_account_credentials, scopes=None):
    """Authenticates the service account given.

    Args:
        service_account_credentials (dict, str): The service account credentials.
        scopes (list[str], optional): The scopes for the service account. Defaults to None.

    Returns:
        google.auth.credentials.Credentials: The authenticated service account credentials.
    """
    try:
        if isinstance(service_account_credentials, dict):  # If credentials are provided as a dict
            if scopes:  # If scopes are provided, use them
                credentials = service_account.Credentials.from_service_account_info(service_account_credentials,
                                                                                    scopes=scopes)
            else:
                credentials = service_account.Credentials.from_service_account_info(service_account_credentials)

        elif isinstance(service_account_credentials, str):  # If credentials are provided as a file path
            if scopes:  # If scopes are provided, use them
                credentials = service_account.Credentials.from_service_account_file(service_account_credentials,
                                                                                    scopes=scopes)
            else:
                credentials = service_account.Credentials.from_service_account_file(service_account_credentials)

        else:  # If credentials are not provided as a dict or file path
            raise ValueError("Service account credentials must be provided as a dict or file path.")

        return credentials  # Return the authenticated service account credentials

    except (AttributeError, ValueError) as e:
        logging.error(f"Unable to authenticate service account. {e}")
        return
