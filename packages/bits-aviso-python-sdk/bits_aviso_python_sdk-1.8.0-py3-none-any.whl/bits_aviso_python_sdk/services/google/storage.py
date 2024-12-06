"""
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
"""

import google.auth.exceptions
import logging
from google.api_core import exceptions
from google.cloud import storage, exceptions
from bits_aviso_python_sdk.helpers.bigquery import parse_to_nldjson
from bits_aviso_python_sdk.services.google import authenticate_google_service_account


class Storage:
    def __init__(self, service_account_credentials=None, project_id=None):
        """Initializes the Storage class. If service account credentials are not provided,
        the credentials will be inferred from the environment.

        Args:
            service_account_credentials (dict, str, optional): The service account credentials in json format
            or the path to the credentials file. Defaults to None.
            project_id (str, optional): The project id to use. Defaults to None.
        """
        if service_account_credentials:
            credentials = authenticate_google_service_account(service_account_credentials)
            if project_id:
                self.client = storage.Client(credentials=credentials, project=project_id)
            else:
                self.client = storage.Client(credentials=credentials)
        else:
            try:
                if project_id:
                    self.client = storage.Client(project=project_id)
                else:
                    self.client = storage.Client()
            except google.auth.exceptions.DefaultCredentialsError as e:
                logging.error(f"Unable to authenticate service account. {e}")
                self.client = None

    def download_blob_to_file(self, bucket_name, blob_name, file_path, prefix=None):
        """Downloads the specified blob to a file.

        Args:
            bucket_name (string): The name of the bucket.
            blob_name (string): The name of the blob.
            file_path (string): The path to save the downloaded file.
            prefix (string, optional): The prefix to use for the blob.

        Returns:
            string: The path to the downloaded file.

        Raises:
            ValueError: If the blob is not found in the bucket.
        """
        try:
            # get the blob
            blob = self.get_blob(bucket_name, blob_name, prefix)
            # download the blob to the file
            logging.info(f"Downloading [{blob_name}] from {bucket_name} to [{file_path}]...")
            blob.download_to_filename(file_path)
            logging.info(f"Downloaded [{blob_name}] from {bucket_name} to [{file_path}].")

            return file_path

        except exceptions.NotFound:
            message = f"Blob [{blob_name}] not found in {bucket_name}."
            logging.error(message)

            raise ValueError(message)

    @staticmethod
    def create_blob(bucket, prefix, blob_name):
        """Creates a blob in the specified bucket.

        Args:
            bucket (google.cloud.storage.bucket.Bucket): The bucket to create the blob in.
            prefix (string): The prefix to use for the blob. Typically, this is the name of the folder.
            blob_name (string): The name of the blob.

        Returns:
            google.cloud.storage.blob.Blob: The created blob.

        Raises:
            ValueError: If the bucket is not found.
        """
        try:
            # create the blob
            logging.info(f"Creating blob {prefix}/{blob_name} in bucket {bucket}...")
            blob = bucket.blob(f"{prefix}/{blob_name}")
            logging.info(f"Created blob {prefix}/{blob_name} in bucket {bucket}.")

            return blob  # return the blob

        except exceptions.NotFound:
            message = f"Bucket {bucket} not found. Cannot proceed with creating blob {prefix}/{blob_name}."
            logging.error(message)

            raise ValueError(message)

    def get_blob(self, bucket_name, blob_name, prefix=None):
        """Gets the specified blob. The blob_name refers to the equivalent of a "file" in a bucket.
        The prefix is used to specify the "folder" in which the blob is located.

        Args:
            bucket_name (string): The name of the bucket.
            blob_name (string): The name of the blob.
            prefix (string, optional): The prefix to use for the blob.


        Returns:
            google.cloud.storage.blob.Blob: The specified blob.

        Raises:
            ValueError: If the blob is not found in the bucket.
        """
        # check if the prefix is provided
        if prefix:
            if prefix.endswith("/"):
                blob_name = f"{prefix}{blob_name}"
            else:
                blob_name = f"{prefix}/{blob_name}"

        try:
            # get the bucket
            bucket = self.get_bucket(bucket_name)
            # get the blob from the bucket
            logging.info(f"Retrieving blob {blob_name} from {bucket_name}...")
            blob = bucket.blob(f"{blob_name}")

            return blob

        except exceptions.NotFound:
            message = f"Blob {blob_name} not found in {bucket_name}."
            logging.error(message)

            raise ValueError(message)

    def get_blob_dict(self, bucket_name, blob_name, prefix=None):
        """Gets the information for the specified blob and returns it as a dictionary.

        Args:
            bucket_name (string): The name of the bucket.
            blob_name (string): The name of the blob.
            prefix (string, optional): The prefix to use for the blob.

        Returns:
            dict: The metadata for the specified blob.
        """
        # get the blob
        blob = self.get_blob(bucket_name, blob_name, prefix)
        # parse the data for the blob
        blob_data = {
            "id": blob.id,
            "name": blob.name,
            "bucket": blob.bucket.name,
            "cache_control": blob.cache_control,
            "chunk_size": blob.chunk_size,
            "client": blob.client,
            "component_count": blob.component_count,
            "content_disposition": blob.content_disposition,
            "content_encoding": blob.content_encoding,
            "content_language": blob.content_language,
            "content_type": blob.content_type,
            "crc32c": blob.crc32c,
            "custom_time": blob.custom_time,
            "etag": blob.etag,
            "event_based_hold": blob.event_based_hold,
            "generation": blob.generation,
            "hard_delete_time": blob.hard_delete_time,
            "md5_hash": blob.md5_hash,
            "media_link": blob.media_link,
            "metadata": blob.metadata,
            "metageneration": blob.metageneration,
            "owner": blob.owner,
            "path": blob.path,
            "public_url": blob.public_url,
            "retention_mode": blob.retention,
            "retention_expiration_time": blob.retention_expiration_time,
            "self_link": blob.self_link,
            "size": blob.size,
            "soft_delete_time": blob.soft_delete_time,
            "storage_class": blob.storage_class,
            "temporary_hold": blob.temporary_hold,
            "time_created": blob.time_created,
            "time_deleted": blob.time_deleted,
            "updated": blob.updated,
            "user_project": blob.user_project
        }

        return blob_data

    def get_bucket(self, bucket_name):
        """Gets the specified bucket.

        Args:
            bucket_name (string): The name of the bucket.

        Returns:
            google.cloud.storage.bucket.Bucket: The specified bucket.

        Raises:
            ValueError: If the bucket is not found.
        """
        try:
            # get_bucket the bucket
            logging.info(f"Retrieving bucket {bucket_name}...")
            bucket = self.client.get_bucket(bucket_name)
            logging.info(f"Retrieved bucket {bucket_name}.")

            return bucket

        except exceptions.NotFound:
            message = f"Bucket {bucket_name} not found."
            logging.error(message)

            raise ValueError(message)

    def get_bucket_dict(self, bucket_name=None, bucket_obj=None):
        """Gets the data for the specified bucket based on the bucket name or object and returns it as a dictionary.

        Args:
            bucket_name (string, optional): The name of the bucket. Defaults to None.
            bucket_obj (google.cloud.storage.bucket.Bucket, optional): The bucket object. Defaults to None.

        Returns:
            dict: The metadata for the specified bucket.
        """
        # check if the bucket object is provided
        if bucket_obj:
            bucket = bucket_obj

        elif bucket_name:
            bucket = self.get_bucket(bucket_name)

        else:
            message = "No bucket name or object provided."
            logging.error(message)
            raise ValueError(message)

        # parse the data for the bucket
        bucket_data = {
            "id": bucket.id,
            "name": bucket.name,
            "cors": bucket.cors,
            "etag": bucket.etag,
            "labels": bucket.labels,
            "lifecycle_rules": bucket.lifecycle_rules,
            "location": bucket.location,
            "location_type": bucket.location_type,
            "metageneration": bucket.metageneration,
            "object_retention_mode": bucket.object_retention_mode,
            "owner": bucket.owner,
            "path": bucket.path,
            "project_number": bucket.project_number,
            "requester_pays": bucket.requester_pays,
            "retention_period": bucket.retention_period,
            "retention_policy_effective_time": bucket.retention_policy_effective_time,
            "retention_policy_locked": bucket.retention_policy_locked,
            "self_link": bucket.self_link,
            "soft_delete_policy": bucket.soft_delete_policy,
            "size": self.get_bucket_size(bucket),
            "storage_class": bucket.storage_class,
            "time_created": bucket.time_created,
            "updated": bucket.updated,
            "user_project": bucket.user_project,
            "versioning_enabled": bucket.versioning_enabled
        }

        return bucket_data

    def get_bucket_size(self, bucket):
        """Gets the total size of the specified bucket.

        Args:
            bucket (string or google.cloud.storage.bucket.Bucket): The name of the bucket or the bucket object.

        Returns:
            int: The total size of the bucket in bytes.

        Raises:
            ValueError: If the bucket is not found.
        """
        try:
            # get the bucket
            if isinstance(bucket, str):
                bucket = self.get_bucket(bucket)

            # variables
            total_size = 0

            # iterate through all objects in the bucket and sum their sizes
            logging.info(f"Retrieving size for bucket {bucket.name}...")
            for blob in bucket.list_blobs():
                total_size += blob.size

            logging.info(f"Successfully retrieved size for bucket {bucket.name}. Total Size: {total_size} bytes.")
            return total_size

        except exceptions.NotFound:
            message = f"Bucket {bucket} not found."
            logging.error(message)
            raise ValueError(message)

        except exceptions.GoogleCloudError as e:
            message = f"Error retrieving size for given bucket argument [{bucket}]: {e}"
            logging.error(message)
            raise ValueError(message)

    def list_blobs(self, bucket_name, prefix=None, delimiter=None):
        """Lists all the blobs in the bucket that begin with the prefix.

        This can be used to list all blobs in a "folder", e.g. "public/".

        The delimiter argument can be used to restrict the results to only the
        "files" in the given "folder". Without the delimiter, the entire tree under
        the prefix is returned. For example, given these blobs:

            a/1.txt
            a/b/2.txt

        If you specify prefix ='a/', without a delimiter, you'll get back:

            a/1.txt
            a/b/2.txt

        However, if you specify prefix='a/' and delimiter='/', you'll get back
        only the file directly under 'a/':

            a/1.txt

        As part of the response, you'll also get back a blobs.prefixes entity
        that lists the "subfolders" under `a/`:

            a/b/

        Copied from Google Cloud Storage documentation.

        Args:
            bucket_name (string): The name of the bucket.
            prefix (string, optional): The prefix to use for the blob. Defaults to None.
            delimiter (string, optional): The delimiter to use to restrict the results. Defaults to None.

        Returns:
            list: A list of all the blobs in google object form in the bucket.
        """
        # list the blobs in the bucket
        logging.info(f"Listing blobs in [{bucket_name}] with prefix [{prefix}] and delimeter [{delimiter}]...")
        return [b for b in self.client.list_blobs(bucket_name, prefix=prefix, delimiter=delimiter)]

    def list_blobs_dict(self, bucket_name, prefix=None, delimiter=None):
        """Lists all the blobs in the specified bucket. If a prefix is provided, only the blobs with the prefix will be
        listed. If a delimiter is provided, the results will be restricted to the specified delimiter.

        Args:
            bucket_name (string): The name of the bucket.
            prefix (string, optional): The prefix to use for the blob. Defaults to None.
            delimiter (string, optional): The delimiter to use to restrict the results. Defaults to None.

        Returns:
            list: A list of dictionaries representing the blobs in the bucket.
        """
        logging.info(f"Getting blob dict data in [{bucket_name}] with prefix [{prefix}] and delimeter [{delimiter}]...")
        blobs = self.list_blobs(bucket_name, prefix=prefix, delimiter=delimiter)
        blobs_dict = []
        for b in blobs:
            blobs_dict.append(self.get_blob_dict(bucket_name, b.name, prefix))

        logging.info(f"Finished getting blob dict data in [{bucket_name}].")
        return blobs_dict

    def list_buckets(self):
        """Lists all the buckets in the project. Each item in the list is a google bucket object.

        Returns:
            list: A list of all the buckets in the project.
        """
        logging.info("Getting all bucket objects...")
        return [b for b in self.client.list_buckets()]

    def list_buckets_dict(self):
        """Lists all the buckets in the project. Each item in the list is a dictionary representing the bucket.

        Returns:
            list: The list of buckets in the project.
        """
        logging.info("Getting all bucket dict data...")
        buckets = self.client.list_buckets()
        buckets_dict = []
        for b in buckets:
            buckets_dict.append(self.get_bucket_dict(b.name, bucket_obj=b))

        logging.info("Finished getting all bucket dict data.")
        return buckets_dict

    def upload(self, bucket_name, prefix, blob_name, data, nldjson=False):
        """Uploads the data to the specified bucket.

        Args:
            bucket_name (string): The name of the bucket.
            prefix (string): The prefix to use for the blob. Typically, the name of the dataset folder.
            blob_name (string): The name of the blob.
            data (str, dict, list): The data to be uploaded to the bucket.
            nldjson (bool, optional): Whether to convert data to newline delimited json. Defaults to False.

        Raises:
            TypeError: If the data cannot be converted to newline delimited json.
            ValueError: If the data cannot be uploaded to the bucket.
        """
        try:
            # get_bucket the bucket
            bucket = self.get_bucket(bucket_name)
            # create the blob
            blob = self.create_blob(bucket, prefix, blob_name)

            # check if the data needs to be converted to newline delimited json
            if nldjson:
                try:
                    data = parse_to_nldjson(data)

                except TypeError as e:  # data is not a dictionary or a list of dictionaries, probably already converted
                    raise ValueError(f"Unable to convert data to newline delimited json. {e}")

            # upload the data
            logging.info(f"Uploading {prefix}/{blob_name} to {bucket_name}...")
            blob.upload_from_string(data)
            logging.info(f"Uploaded {prefix}/{blob_name} to {bucket_name}.")

        except ValueError as e:
            message = f"Unable to upload {blob_name} to {bucket_name}. {e}"
            logging.error(message)

            raise ValueError(message)  # raise an error with the message
