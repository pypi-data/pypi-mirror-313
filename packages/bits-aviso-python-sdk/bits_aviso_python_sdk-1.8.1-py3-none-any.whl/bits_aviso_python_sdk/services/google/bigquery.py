"""
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
"""
import google.auth.exceptions
import logging
from google.api_core import exceptions
from google.cloud import bigquery
from bits_aviso_python_sdk.services.google import authenticate_google_service_account


class BigQuery:
    def __init__(self, project_id=None, service_account_credentials=None):
        """Initializes the BigQuery class. If service account credentials are not provided,
        the credentials will be inferred from the environment.

        Args:
            project_id (str, optional): The project id. Defaults to None.
            service_account_credentials (dict, str, optional): The service account credentials in json format or the
                path to the credentials file. Defaults to None.
        """
        if service_account_credentials:
            credentials = authenticate_google_service_account(service_account_credentials)
            if project_id:
                self.client = bigquery.Client(credentials=credentials, project=project_id)
            else:
                self.client = bigquery.Client(credentials=credentials)
        else:
            try:
                if project_id:
                    self.client = bigquery.Client(project=project_id)
                else:
                    self.client = bigquery.Client()
            except google.auth.exceptions.DefaultCredentialsError as e:
                logging.error(f"Unable to authenticate service account. {e}")
                self.client = None

    def query(self, query):
        """Executes a query on BigQuery.

        Args:
            query (str): The query to execute.

        Returns:
            list[dict]: The results of the query in a list of dictionaries.

        Raises:
            ValueError: If the query is invalid or returns no results.
        """
        try:
            query_job = self.client.query(query)
            results = query_job.result()

            if isinstance(results, bigquery.table._EmptyRowIterator):
                raise ValueError(f'QUERY: {query}')

            # return results as list of dictionaries
            return [dict(row) for row in results]

        except exceptions.BadRequest as e:
            err_msg = f"Unable to execute query. {e}"
            logging.error(err_msg)
            raise ValueError(err_msg)

        except ValueError as e:
            err_msg = f"Query returned no results. {e}"
            logging.error(err_msg)
            raise ValueError(err_msg)
