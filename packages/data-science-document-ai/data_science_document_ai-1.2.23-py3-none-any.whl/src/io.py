"""Manage API calls and IO procedures."""

import logging
import os
import sys
import tempfile
from pathlib import Path

from google.cloud import bigquery, storage

# Set standard output and standard error for the logs
logger = logging.getLogger("__name__")
logger.setLevel(logging.INFO)
logger.propagate = False

logger_format = "%(asctime)s [%(levelname)s] %(message)s"
formatter = logging.Formatter(logger_format)

h1 = logging.StreamHandler(sys.stdout)
h1.setLevel(logging.INFO)
h1.addFilter(lambda record: record.levelno <= logging.WARNING)
h1.setFormatter(formatter)

h2 = logging.StreamHandler(sys.stderr)
h2.setLevel(logging.ERROR)
h2.addFilter(lambda record: record.levelno == logging.ERROR)
h2.setFormatter(formatter)
logger.addHandler(h1)
logger.addHandler(h2)
from src.tms import download_document_api  # noqa


def setup_logging_with_excluded_endpoints(params: dict) -> None:
    """
    Set up logging to exclude specific endpoints.

    Args:
        params: A dictionary containing configuration parameters, including 'excluded_endpoints'.
    """

    class EndpointFilter(logging.Filter):
        """Filter class to exclude specific endpoints from log entries."""

        def __init__(self, excluded_endpoints: list[str]) -> None:
            """
            Initialize the EndpointFilter class.

            Args:
                excluded_endpoints: A list of endpoints to be excluded from log entries.
            """
            super().__init__()
            self.excluded_endpoints = excluded_endpoints

        def filter(self, record: logging.LogRecord) -> bool:
            """
            Filter out log entries for excluded endpoints.

            Args:
                record: The log record to be filtered.

            Returns:
                bool: True if the log entry should be included, False otherwise.
            """
            return (
                record.args
                and len(record.args) >= 3
                and record.args[2] not in self.excluded_endpoints
            )

    # Get excluded_endpoints from params
    excluded_endpoints = params.get("excluded_endpoints", [])

    # Add filter to the logger
    logging.getLogger("uvicorn.access").addFilter(EndpointFilter(excluded_endpoints))


def get_bq_client(params):
    """Get Google BigQuery client."""
    bq_client = bigquery.Client(project=params["bq_project_id"])
    job_config = bigquery.QueryJobConfig(
        allow_large_results=True,
        # flatten_results=True,
        labels={"project-name": params["project_name"]},
    )
    return bq_client, job_config


def query_dwh(params, query):
    """Query data from DWH."""
    client, job_config = get_bq_client(params)

    df = client.query(query=query, job_config=job_config).to_dataframe(
        progress_bar_type="tqdm"
    )
    return df


def upload_pdf_to_bucket(params, content, file_name):
    """Upload bytes content to GCS bucket.

    Args:
        params (dict): Parameters dictionary containing project ID and bucket name.
        content (bytes): Content of the file to be uploaded.
        file_name (str): Name of the file to be uploaded.
    """
    try:
        # Create a temporary file to store the content
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, file_name)

        # Write the content to the temporary file
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(content)

        # Upload the temporary file to the bucket
        client = storage.Client(project=params["g_ai_project_name"])
        bucket = client.bucket(params["doc_ai_bucket_batch_input"])

        blob = bucket.blob(file_name)
        blob.upload_from_filename(temp_file_path)

        # Delete the temporary file
        os.remove(temp_file_path)
        os.rmdir(temp_dir)

        return f"gs://{params['doc_ai_bucket_batch_input']}/{file_name}", client  # noqa

    except Exception as e:
        print(
            f"Error uploading {file_name} to bucket {params['doc_ai_bucket_batch_input']}: {e}"
        )
        return None, None


def delete_folder_from_bucket(bucket_name, folder_name):
    """Delete a folder (prefix) and its contents from a GCS bucket.

    Args:
        bucket_name (str): Name of the GCS bucket.
        folder_name (str): Name of the folder (prefix) to delete.
    """
    try:
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)

        # List all objects with the given prefix (folder name)
        blobs = bucket.list_blobs(prefix=folder_name)

        # Delete each object
        for blob in blobs:
            blob.delete()

    except Exception as e:
        logger.error(
            f"Error deleting folder {folder_name} from bucket {bucket_name}: {e}"
        )


def get_storage_client(params) -> storage.Client:
    """Get Google Storage client."""
    return storage.Client(project=params["g_ai_project_name"])


def download_dir_from_bucket(bucket, directory_cloud, directory_local) -> bool:
    """Download file from Google blob storage.

    Args:
        bucket: Google Storage bucket object
        directory_cloud: directory to download
        directory_local: directory where to download

    Returns:
        bool: True if folder is not exists and not empty
    """
    result = False
    blobs = bucket.list_blobs(prefix=directory_cloud)  # Get list of files
    for blob in blobs:
        result = True
        if blob.name.endswith("/"):
            continue
        file_split = blob.name.split("/")
        directory = "/".join(file_split[0:-1])
        directory = directory_local / Path(directory)
        Path(directory).mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(directory_local / Path(blob.name))
    return result
