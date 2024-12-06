"""
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
"""
import logging
from bits_aviso_python_sdk.services.google import authenticate_google_service_account
from googleapiclient import discovery
from googleapiclient.errors import HttpError


class Sheets:
    """Sheets class to interface with Google's Sheets API."""

    def __init__(self, service_account_credentials):
        """Initializes the Sheets class using the provided service account credentials. It also initializes a google
        drive client to manage permissions.

        Args:
            service_account_credentials (dict, str, optional): The service account credentials in json format
            or the path to the credentials file.
        """
        credentials = authenticate_google_service_account(service_account_credentials)
        self.service = discovery.build('sheets', 'v4', credentials=credentials)
        self.drive_service = discovery.build('drive', 'v3', credentials=credentials)

    def create_spreadsheet(self, name):
        """Creates a new spreadsheet with the given name.

        Args:
            name (str): The name of the new spreadsheet.

        Returns:
            string: The response from the API.

        Raises:
            ValueError: If unable to create a new spreadsheet.
        """
        spreadsheet = {
            'properties': {
                'title': name
            }
        }

        try:
            spreadsheet = self.service.spreadsheets().create(body=spreadsheet).execute()
            return spreadsheet['spreadsheetId']

        except (HttpError, KeyError) as e:
            err_msg = f"Unable to create spreadsheet. {e}"
            logging.error(err_msg)
            raise ValueError(err_msg)

    def create_new_sheet(self, spreadsheet_id, sheet_name):
        """Creates a new sheet in the given spreadsheet.

        Args:
            spreadsheet_id (str): The ID of the spreadsheet.
            sheet_name (str): The name of the new sheet.

        Returns:
            dict: The response from the API.

        Raises:
            ValueError: If unable to create a new sheet.

        Example Response Body:
        ```json
        {
            'spreadsheetId': '1bnye4789SFDkofwnfbHFGdB4x2-_0-XKxfgGHJKLaMig3mraqQ',
            'replies': [{
                'addSheet': {
                    'properties': {
                        'sheetId': 1234567890,
                        'title': 'test-sheet',
                        'index': 1,
                        'sheetType': 'GRID',
                        'gridProperties': {
                            'rowCount': 1000,
                            'columnCount': 10
                        }
                    }
                }
            }]
        }
        ```
        """
        body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': sheet_name
                    }
                }
            }]
        }

        try:
            response = self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=body
            ).execute()

            return response

        except HttpError as e:
            err_msg = f"Unable to create new sheet. {e}"
            logging.error(err_msg)
            raise ValueError(err_msg)

    def grant_permission(self, file_id, email, role='writer'):
        """Grants permission to the specified user for the given google drive file.

        Args:
            file_id (str): The ID of the file.
            email (str): The email address of the user.
            role (str): The role to grant. Defaults to 'writer'. Possible values are 'reader', 'writer', 'owner.

        Returns:
            dict: The response from the API.

        Raises:
            ValueError: If unable to grant permission.
        """
        if role not in ['reader', 'writer', 'owner']:
            logging.error("Invalid role. Role must be one of 'reader', 'writer', 'owner'.")
            return

        permission = {
            'type': 'user',
            'role': role,
            'emailAddress': email
        }

        try:
            if role == 'owner':  # if role is owner, transfer ownership flag is needed
                response = self.drive_service.permissions().create(
                    fileId=file_id,
                    body=permission,
                    transferOwnership=True,
                    fields='id'
                ).execute()
                return response

            else:
                response = self.drive_service.permissions().create(
                    fileId=file_id,
                    body=permission,
                    fields='id'
                ).execute()
                return response

        except HttpError as e:
            err_msg = f"Unable to grant permission. {e}"
            logging.error(err_msg)
            raise ValueError(err_msg)
