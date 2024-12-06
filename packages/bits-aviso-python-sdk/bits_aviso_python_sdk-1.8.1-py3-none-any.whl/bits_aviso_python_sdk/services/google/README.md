# google
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

# bigquery
This module provides a class to interact with Google BigQuery. Currently, it only supports executing queries.
If no service account credentials are provided, the SDK will attempt to use the default credentials.

## Usage
The following is an example of how to execute a query in BigQuery:

```python

from bits_aviso_python_sdk.services.google.bigquery import BigQuery

# initialize BigQuery client
bigquery_client = BigQuery()

# query
query = "SELECT * FROM `your_project_id.your_dataset_id.your_table_id`"

# execute query
result = bigquery_client.query(query)
```

---

# pubsub
This module provides a class to interact with Google Cloud Pub/Sub.
If no service account credentials are provided, the SDK will attempt to use the default credentials.

## Usage
The following is an example of how to send a message to a Pub/Sub topic:

```python
from bits_aviso_python_sdk.services.google.pubsub import Pubsub

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

# Initialize Pub/Sub client
pubsub_client = Pubsub(service_account_credentials=service_account)

# pubsub message contents
message = {
    "message": "Hello, World!"
}
# Send a message to a Pub/Sub topic
pubsub_client.send("project_id", "your_topic_name", message)
```

---

# secretmanager
This module provides a class to interact with Google Cloud Secret Manager.
If no service account credentials are provided, the SDK will attempt to use the default credentials.

## Usage
The following is an example of how to access a secret from Secret Manager:

```python
from bits_aviso_python_sdk.services.google.secretmanager import SecretManager

# initialize Secret Manager client
secret_manager_client = SecretManager()

# get secret
secret = secret_manager_client.get_secret("project_id", "your_secret_name")
print(secret)
```

---

# sheets
This module provides a class to interact with Google Sheets.
Service account credentials are required to authenticate with Google Sheets.

## Usage
The following is an example of how to add a new sheet to an existing spreadsheet:

```python
from bits_aviso_python_sdk.services.google.sheets import Sheets

# initialize Sheets client
sheets_client = Sheets("your_service_account_credentials")

# create a new sheet
sheets_client.create_new_sheet("your_spreadsheet_id", "new_sheet_name")
```

---

# storage
This module provides a class to interact with Google Cloud Storage.
If no service account credentials are provided, the SDK will attempt to use the default credentials.

## Usage
The following is an example of how to upload a file to Google Cloud Storage:

```python
from bits_aviso_python_sdk.services.google.storage import Storage

# initialize Storage client
storage_client = Storage()

# file to upload
file_to_upload = "path/to/your/file.txt"

# upload a file
storage_client.upload("your_bucket_name", "prefix", "file.txt", file_to_upload)
```

---
