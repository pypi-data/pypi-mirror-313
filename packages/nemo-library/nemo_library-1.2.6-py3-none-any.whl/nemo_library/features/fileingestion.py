import gzip
import logging
import shutil
import os
import time
import json
import requests
import boto3
from botocore.exceptions import NoCredentialsError
import pandas as pd

from nemo_library.features.config import Config
from nemo_library.features.projects import getProjectID
from nemo_library.utils.utils import log_error


def ReUploadFile(
    config: Config,
    projectname: str,
    filename: str,
    update_project_settings: bool = True,
    datasource_ids: list[dict] = None,
    global_fields_mapping: list[dict] = None,
    version: int = 2,
    trigger_only: bool = False,
) -> None:
    """
    Re-uploads a file to a specified project in the NEMO system and triggers data ingestion.

    Args:
        config (Config): Configuration object containing connection details and headers.
        projectname (str): The name of the project to which the file will be uploaded.
        filename (str): The path to the file to upload.
        update_project_settings (bool, optional): Whether to trigger the "analyze_table" task after ingestion (version 2 only). Defaults to True.
        datasource_ids (list[dict], optional): Data source identifiers for version 3 ingestion. Defaults to None.
        global_fields_mapping (list[dict], optional): Field mappings for version 3 ingestion. Defaults to None.
        version (int, optional): The ingestion version (2 or 3). Defaults to 2.
        trigger_only (bool, optional): If True, skips waiting for task completion. Defaults to False.

    Returns:
        None

    Raises:
        Exception: If any step of the file upload, data ingestion, or subsequent tasks fails.

    Notes:
        - Compresses the file into gzip format before uploading.
        - Retrieves temporary AWS S3 credentials from NEMO's Token Vendor and uploads the file to S3.
        - Sends a request to ingest the uploaded data and optionally waits for task completion.
        - Triggers "analyze_table" task if version 2 and `update_project_settings` is True.
        - Logs and raises exceptions for any errors encountered during the process.
    """

    project_id = None
    headers = None
    project_id = None
    
    try:
        project_id = getProjectID(config, projectname)

        headers = config.connection_get_headers()

        logging.info(f"Upload of file '{filename}' into project '{projectname}' initiated...")

        # Zip the file before uploading
        gzipped_filename = filename + ".gz"
        with open(filename, "rb") as f_in:
            with gzip.open(gzipped_filename, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        logging.info(f"File {filename} has been compressed to {gzipped_filename}")

        # Retrieve temporary credentials from NEMO TVM
        response = requests.get(
            config.config_get_nemo_url()
            + "/api/nemo-tokenvendor/InternalTokenVendor/sts/s3_policy",
            headers=headers,
        )

        if response.status_code != 200:
            raise Exception(
                f"Request failed. Status: {response.status_code}, error: {response.text}"
            )

        aws_credentials = json.loads(response.text)

        aws_access_key_id = aws_credentials["accessKeyId"]
        aws_secret_access_key = aws_credentials["secretAccessKey"]
        aws_session_token = aws_credentials["sessionToken"]

        # Create an S3 client
        s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
        )

        try:
            # Upload the file
            s3filename = (
                config.config_get_tenant()
                + f"/ingestv{version}/"
                + os.path.basename(gzipped_filename)
            )
            s3.upload_file(
                gzipped_filename,
                "nemoinfrastructurestack-nemouploadbucketa98fe899-1s2ocvunlg3vs",
                s3filename,
            )
            logging.info(f"File {filename} uploaded successfully to s3 ({s3filename})")
        except FileNotFoundError:
            log_error(f"The file {filename} was not found.",FileNotFoundError)
        except NoCredentialsError:
            log_error(f"The file {filename} was not found.",NoCredentialsError)

        # Prepare data for ingestion
        data = {
            "project_id": project_id,
            "s3_filepath": f"s3://nemoinfrastructurestack-nemouploadbucketa98fe899-1s2ocvunlg3vs/{s3filename}",
        }

        if version == 3:
            if datasource_ids is not None:
                data["data_source_identifiers"] = datasource_ids
            if global_fields_mapping is not None:
                data["global_fields_mappings"] = global_fields_mapping

        endpoint_url = (
            "/api/nemo-queue/ingest_data_kubernetes_v3"
            if version == 3
            else "/api/nemo-queue/ingest_data_kubernetes_v2"
        )

        response = requests.post(
            config.config_get_nemo_url() + endpoint_url,
            headers=headers,
            json=data,
        )
        if response.status_code != 200:
            raise Exception(
                f"Request failed. Status: {response.status_code}, error: {response.text}"
            )
        logging.info("Ingestion successful")

        # Wait for task to be completed if not trigger_only
        if version == 2 or not trigger_only:
            taskid = response.text.replace('"', "")
            while True:
                data = {
                    "sort_by": "submit_at",
                    "is_sort_ascending": "False",
                    "page": 1,
                    "page_size": 20,
                }
                response = requests.get(
                    config.config_get_nemo_url() + "/api/nemo-queue/task_runs",
                    headers=headers,
                    json=data,
                )
                resultjs = json.loads(response.text)
                df = pd.json_normalize(resultjs["records"])
                df_filtered = df[df["id"] == taskid]
                if len(df_filtered) != 1:
                    raise Exception(
                        f"Data ingestion request failed, task ID not found in tasks list"
                    )
                status = df_filtered["status"].iloc[0]
                logging.info(f"Status: {status}")
                if status == "failed":
                    log_error("Data ingestion request failed, status: FAILED")
                if status == "finished":
                    if version == 2:
                        records = df_filtered["records"].iloc[0]
                        logging.info(f"Ingestion finished. {records} records loaded")
                    else:
                        logging.info("Ingestion finished.")
                    break
                time.sleep(1 if version == 2 else 5)

        # Trigger Analyze Table Task for version 2 if required
        if version == 2 and update_project_settings:
            data = {
                "project_id": project_id,
            }
            response = requests.post(
                config.config_get_nemo_url()
                + "/api/nemo-queue/analyze_table_kubernetes",
                headers=headers,
                json=data,
            )
            if response.status_code != 200:
                raise Exception(
                    f"Request failed. Status: {response.status_code}, error: {response.text}"
                )
            logging.info("Analyze_table triggered")

            # Wait for task to be completed
            taskid = response.text.replace('"', "")
            while True:
                data = {
                    "sort_by": "submit_at",
                    "is_sort_ascending": "False",
                    "page": 1,
                    "page_size": 20,
                }
                response = requests.get(
                    config.config_get_nemo_url() + "/api/nemo-queue/task_runs",
                    headers=headers,
                    json=data,
                )
                resultjs = json.loads(response.text)
                df = pd.json_normalize(resultjs["records"])
                df_filtered = df[df["id"] == taskid]
                if len(df_filtered) != 1:
                    raise Exception(
                        f"Analyze_table request failed, task ID not found in tasks list"
                    )
                status = df_filtered["status"].iloc[0]
                logging.info(f"Status: {status}")
                if status == "failed":
                    log_error("Analyze_table request failed, status: FAILED")
                if status == "finished":
                    logging.info("Analyze_table finished.")
                    break
                time.sleep(1)

    except Exception as e:
        if project_id is None:
            log_error("Upload stopped, no project_id available")
        raise log_error(f"Upload aborted: {e}")
