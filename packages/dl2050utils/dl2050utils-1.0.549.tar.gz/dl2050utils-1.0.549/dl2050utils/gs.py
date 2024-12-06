"""
Google Storage (GS)
https://cloud.google.com/storage/docs/samples/storage-generate-signed-url-v4#storage_generate_signed_url_v4-python
"""

import os
import datetime
import re
import pickle
import mimetypes
from google.cloud import storage
from dl2050utils.core import oget
from dl2050utils.env import config_load
from dl2050utils.fs import json_save


class GS:
    """
    Google Cloud Storage helper class to manage buckets, files, and URLs.
    This class is a simplfied drive to interact with Google Storage, providing an abstraction
    to isolate the application level code from the underlying storage provider.
    If facilitates operations such as creating/deleting buckets, uploading/downloading files,
    generating signed URLs for blob uploads/downloads, and managing files in-memory or on disk.
    Attributes:
    default_location (str): Default location for creating GCS buckets.
    gc (storage.Client): Google Cloud storage client instance.
    """

    def __init__(self, service, default_location="europe-west1"):
        """
        Initializes the GS class with the specified Google Cloud service and location.
        Args:
            service (str): The Google Cloud service name.
            default_location (str): Default location for bucket creation. Defaults to "europe-west1".
        """
        cfg = config_load(service)
        # Create credentials file from config yml
        key_dict = oget(cfg, ["gcloud", "gs_key"])
        assert key_dict["type"] == "service_account"
        credentials_p = "./gs-keyfile.json"
        json_save(credentials_p, key_dict)
        # Set the GOOGLE_APPLICATION_CREDENTIALS env var to use the credentials file
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_p
        # Connect
        self.default_location = default_location
        self.gc = storage.Client()

    # ####################################################################################################
    # Admin
    # ####################################################################################################

    def create_bucket(self, bucket_name):
        """
        Creates a new bucket in Google Cloud Storage.
        Args:
            bucket_name (str): The name of the bucket to create.
        Returns:
            int: 0 if the bucket was created successfully, 1 otherwise.
        """
        try:
            bucket = self.gc.bucket(bucket_name)
            bucket.storage_class = "STANDARD"
            new_bucket = self.gc.create_bucket(bucket, location=self.default_location)
            print(
                f"Bucket {new_bucket.name} created in {new_bucket.location}, storage class {new_bucket.storage_class}"
            )
            return 0
        except Exception as exc:
            print(f"create_bucket EXCEPTION: {str(exc)}")
            return 1

    def remove_bucket(self, bucket_name, force_delete=False):
        """
        Deletes a bucket from Google Cloud Storage.
        Args:
            bucket_name (str): The name of the bucket to delete.
            force_delete (bool, optional): If True, deletes all objects in the bucket. Defaults to False.
        Returns:
            int: 0 if the bucket was deleted successfully, 1 otherwise.
        """
        try:
            bucket = self.gc.bucket(bucket_name)
            if force_delete:
                # Delete all objects in the bucket
                blobs = bucket.list_blobs()
                for blob in blobs:
                    blob.delete()
                print(f"All objects in bucket '{bucket_name}' have been deleted.")
            bucket.delete()
            print(f"Bucket '{bucket_name}' has been deleted.")
            return 0
        except Exception as exc:
            print(f"remove_bucket EXCEPTION: {str(exc)}")
            return 1

    def delete_object(self, bucket_name, blob_name):
        """
        Deletes a single object from the bucket, with exact match.
        Args:
            bucket_name (str): Name of the GCS bucket.
            blob_name (str): Name of the blob (object) to delete.
        Returns:
            int: False if the object was deleted successfully, True otherwise.
        """
        try:
            bucket = self.gc.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.delete()
            print(f"Deleted object '{blob_name}' from bucket '{bucket_name}'.")
            return 0
        except Exception as exc:
            print(f"delete_object EXCEPTION: {str(exc)}")
            return 1

    def delete_objects(self, bucket_name, pattern=None, prefix=None, suffix=None):
        """
        Deletes multiple objects from a bucket matching a pattern.
        Args:
            bucket_name (str): Name of the GCS bucket.
            pattern (str, optional): Regular expression pattern to match blob names.
            prefix (str, optional): Prefix string that blob names should start with.
            suffix (str, optional): Suffix string that blob names should end with.
        Returns:
            int: The number of objects deleted.
        """
        try:
            bucket = self.gc.bucket(bucket_name)
            # Decide which blobs to list based on prefix
            blobs = bucket.list_blobs(prefix=prefix) if prefix else bucket.list_blobs()
            deleted_count = 0
            pattern_compiled = re.compile(pattern) if pattern else None
            for blob in blobs:
                blob_name = blob.name
                match = True
                if pattern_compiled:
                    if not pattern_compiled.search(blob_name):
                        match = False
                if prefix:
                    if not blob_name.startswith(prefix):
                        match = False
                if suffix:
                    if not blob_name.endswith(suffix):
                        match = False
                if match:
                    blob.delete()
                    # print(f"Deleted object '{blob_name}' from bucket '{bucket_name}'.")
                    deleted_count += 1
            print(f"Deleted {deleted_count} objects from bucket '{bucket_name}'.")
            return deleted_count
        except Exception as exc:
            print(f"delete_objects EXCEPTION: {str(exc)}")
            return 0

    def list(self, bucket_name, subdir=""):
        """
        Lists all files in a specified subdirectory of a bucket.
        Args:
            bucket_name (str): Name of the GCS bucket.
            subdir (str, optional): Subdirectory path within the bucket. Defaults to '' (root).
        Returns:
            list: List of blob names in the specified subdirectory.
        """
        try:
            bucket = self.gc.bucket(bucket_name)
            blobs = bucket.list_blobs(prefix=subdir)
            file_list = [blob.name for blob in blobs if not blob.name.endswith("/")]
            print(f"Files in {bucket_name}/{subdir}: {file_list}")
            return file_list
        except Exception as exc:
            print(f"list_files EXCEPTION: {str(exc)}")
            return []

    # ###################################################################################################################
    # Memmory Download, Upload
    # ###################################################################################################################

    def upload_mem(self, bucket_name, blob_name, data, content_type="application/octet-stream", use_pickle=True):
        """
        Uploads data from memory to a specified bucket and blob.
        Args:
            bucket_name (str): Name of the GCS bucket.
            blob_name (str): Name of the blob to upload.
            data (str or bytes): Data to upload. Can be a string or bytes.
            content_type (str, optional): MIME type of the data. Defaults to 'application/octet-stream'.
            use_pickle (bool, optional): If True, serializes the data using pickle before uploading. Defaults to False.
        Returns:
            int: 0 if upload is successful, 1 otherwise.
        Examples:
            gs.upload_mem(bucket_name, blob_name, data="Hello, world!", content_type='text/plain')
            gs.upload_mem(bucket_name, blob_name, data=b'\x89PNG\r\n\x1a...', content_type='image/png')
        """
        try:
            if use_pickle:
                data = pickle.dumps(data)
            elif isinstance(data, str):
                data = data.encode("utf-8")
            bucket = self.gc.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.upload_from_string(data, content_type=content_type)
            print(f"Uploaded data to {bucket_name}/{blob_name}")
            return 0
        except Exception as exc:
            print(f"upload_mem EXCEPTION: {str(exc)}")
            return 1

    def download_mem(self, bucket_name, blob_name, as_string=False, encoding="utf-8", use_pickle=True):
        """
        Downloads a blob from the bucket into memory.
        Args:
            bucket_name (str): Name of the GCS bucket.
            blob_name (str): Name of the blob to download.
            as_string (bool, optional): If True, decodes the data using the specified encoding.
                                        Ignored if use_pickle is True. Defaults to False.
            encoding (str, optional): The encoding to use when decoding bytes to string. Defaults to 'utf-8'.
            use_pickle (bool, optional): If True, deserializes the data using pickle after downloading.
                                        Defaults to False.
        Returns:
            Any: The data from the blob, possibly decoded or deserialized.
        """
        try:
            bucket = self.gc.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            data = blob.download_as_bytes()
            if use_pickle:
                # Deserialize the data using pickle
                data = pickle.loads(data)
            elif as_string:
                # Decode the data using the specified encoding
                data = data.decode(encoding)
            # If neither use_pickle nor as_string is True, return the raw bytes
            return data
        except Exception as exc:
            print(f"download_mem EXCEPTION: {str(exc)}")
            return None

    # ###################################################################################################################
    # File Download, Upload
    # ###################################################################################################################

    def upload_file(
        self,
        bucket_name,
        blob_name,
        local_file_path,
        content_type="application/octet-stream",
    ):
        """
        Uploads a local file to a specified bucket and blob.
        Args:
            bucket_name (str): Name of the GCS bucket.
            blob_name (str): Name of the blob to upload.
            local_file_path (str): Local path of the file to upload.
            content_type (str, optional): MIME type of the data. Defaults to 'application/octet-stream'.
        Returns:
            int: 0 if upload is successful, 1 otherwise.
        """
        try:
            bucket = self.gc.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.upload_from_filename(local_file_path, content_type=content_type)
            print(f"Uploaded {local_file_path} to {bucket_name}/{blob_name}")
            return 0
        except Exception as exc:
            print(f"upload_file EXCEPTION: {str(exc)}")
            return 1

    def download_file(self, bucket_name, blob_name, local_file_path):
        """
        Downloads a blob from the bucket to a local file.
        Args:
            bucket_name (str): Name of the GCS bucket.
            blob_name (str): Name of the blob to download.
            local_file_path (str): Local path to save the downloaded file.
        Returns:
            int: 0 if upload is successful, 1 otherwise.
        """
        try:
            bucket = self.gc.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.download_to_filename(local_file_path)
            print(f"Downloaded {bucket_name}/{blob_name} to {local_file_path}")
            return 0
        except Exception as exc:
            print(f"download_file EXCEPTION: {str(exc)}")
            return 1

    # ####################################################################################################
    # download_folder, upload_folder
    # ####################################################################################################

    def upload_folder(self, bucket_name, blob_name, local_folder_path):
        """
        Recursively uploads a local folder to the remote storage, preserving the directory structure.
        Args:
            bucket_name (str): Name of the remote bucket.
            blob_name (str, optional): Remote folder path within the bucket. Defaults to ''.
            local_folder_path (str): Path to the local folder to upload.
        """
        try:
            for root, dirs, files in os.walk(local_folder_path):
                for file in files:
                    # Full local file path
                    local_file_path = os.path.join(root, file)
                    # Compute relative path to maintain directory structure
                    relative_path = os.path.relpath(local_file_path, local_folder_path)
                    relative_path = relative_path.replace(
                        os.sep, "/"
                    )  # Ensure UNIX-style path separators
                    # Construct remote file path
                    remote_file_path = os.path.join(blob_name, relative_path).replace(
                        os.sep, "/"
                    )
                    # Upload the file
                    content_type, _ = mimetypes.guess_type(local_file_path)
                    if content_type is None:
                        content_type = "application/octet-stream"
                    not_success = self.upload_file(
                        bucket_name,
                        remote_file_path,
                        local_file_path,
                        content_type=content_type,
                    )
                    if not_success:
                        print(f"Failed to upload {local_file_path}")
            print(
                f"Uploaded folder '{local_folder_path}' to '{bucket_name}/{blob_name}'"
            )
        except Exception as exc:
            print(f"upload_folder EXCEPTION: {str(exc)}")

    def download_folder(self, bucket_name, blob_name, local_folder_path):
        """
        Recursively downloads a folder from the remote storage to a local directory, preserving the directory structure.
        Args:
            bucket_name (str): Name of the remote bucket.
            blob_name (str): Remote folder path within the bucket.
            local_folder_path (str): Local path where the folder will be downloaded.
        """
        try:
            bucket = self.gc.bucket(bucket_name)
            blobs = bucket.list_blobs(prefix=blob_name)
            for blob in blobs:
                # Skip if the blob is a directory placeholder
                if blob.name.endswith("/"):
                    continue
                # Compute relative path to maintain directory structure
                relative_path = os.path.relpath(blob.name, blob_name)
                relative_path = relative_path.replace(os.sep, "/")
                # Construct local file path
                local_file_path = os.path.join(local_folder_path, relative_path)
                # Ensure local directories exist
                local_dir = os.path.dirname(local_file_path)
                if not os.path.exists(local_dir):
                    os.makedirs(local_dir)
                # Download the file
                result = self.download_file(bucket_name, blob.name, local_file_path)
                if result != 0:
                    print(f"Failed to download {blob.name}")
            print(
                f"Downloaded folder '{bucket_name}/{blob_name}' to '{local_folder_path}'"
            )
        except Exception as exc:
            print(f"download_folder EXCEPTION: {str(exc)}")

    # ####################################################################################################
    # Signed urls
    # ####################################################################################################

    def upload_url(self, bucket_name, blob_name, timeout=15 * 60, size=None):
        """
        Generates a signed URL for uploading a blob.
        Args:
            bucket_name (str): Name of the GCS bucket.
            blob_name (str): Name of the blob to upload.
            timeout (int, optional): URL expiration time in seconds. Defaults to 15 minutes.
            size (int, optional): Maximum allowed size of the upload in bytes.
        Returns:
            str or None: Signed URL for uploading or None if an error occurs.
        """
        try:
            bucket = self.gc.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            query_parameters = (
                None if size is None else {"x-goog-content-length-range": f"0,{size}"}
            )
            url = blob.generate_signed_url(
                version="v4",
                expiration=datetime.timedelta(seconds=timeout),
                method="PUT",
                content_type="application/octet-stream",
                query_parameters=query_parameters,
            )
            return url
        except Exception as exc:
            print(f"upload_url EXCEPTION: {str(exc)}")
            return None

    def download_url(self, bucket_name, blob_name, timeout=24 * 3600):
        """
        Generates a signed URL for downloading a blob.
        Args:
            bucket_name (str): Name of the GCS bucket.
            blob_name (str): Name of the blob to download.
            timeout (int, optional): URL expiration time in seconds. Defaults to 24 hours.
        Returns:
            str or None: Signed URL for downloading or None if an error occurs.
        """
        try:
            bucket = self.gc.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            url = blob.generate_signed_url(
                version="v4",
                expiration=datetime.timedelta(seconds=timeout),
                method="GET",
            )
            # Append the blob_name for the download client to be able to recover the file name
            # url = f'{url}&filename={blob_name}'
            return url
        except Exception as exc:
            print(f"download_url EXCEPTION: {str(exc)}")
            return None

    def urls(self, bucket_name, blob_name, timeout=24 * 3600, size=None):
        """
        Generates both upload and download signed URLs for a blob.
        Args:
            bucket_name (str): Name of the GCS bucket.
            blob_name (str): Name of the blob.
            timeout (int, optional): URL expiration time in seconds. Defaults to 24 hours.
            size (int, optional): Maximum allowed size of the upload in bytes.
        Returns:
            tuple: (upload_url, download_url)
        """
        return self.upload_url(
            bucket_name, blob_name, timeout=timeout, size=size
        ), self.download_url(bucket_name, blob_name, timeout=timeout)
