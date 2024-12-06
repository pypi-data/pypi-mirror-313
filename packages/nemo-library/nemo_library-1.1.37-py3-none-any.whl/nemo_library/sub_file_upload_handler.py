import gzip
import shutil
import os
import time
import json
import requests
import boto3
from botocore.exceptions import NoCredentialsError
import pandas as pd
from nemo_library.sub_config_handler import ConfigHandler
from nemo_library.sub_connection_handler import connection_get_headers
from nemo_library.sub_project_handler import getProjectID
from nemo_library.sub_symbols import (
    ENDPOINT_URL_QUEUE_ANALYZE_TABLE,
    ENDPOINT_URL_QUEUE_INGEST_DATA_V2,
    ENDPOINT_URL_QUEUE_INGEST_DATA_V3,
    ENDPOINT_URL_QUEUE_TASK_RUNS,
    ENDPOINT_URL_TVM_S3_ACCESS,
)


def ReUploadFileIngestion(
    config: ConfigHandler,
    projectname: str,
    filename: str,
    update_project_settings: bool = True,
    datasource_ids: list[dict] = None,
    global_fields_mapping: list[dict] = None,
    version: int = 2,
    trigger_only: bool = False,
) -> None:
    """
    Uploads a file to a project and optionally updates project settings or triggers analyze tasks.

    Args:
        projectname (str): Name of the project.
        filename (str): Name of the file to be uploaded.
        update_project_settings (bool, optional): Whether to update project settings after ingestion. Defaults to True.
        datasource_ids (list[dict], optional): List of datasource identifiers for V3 ingestion. Defaults to None.
        global_fields_mapping (list[dict], optional): Global fields mapping for V3 ingestion. Defaults to None.
        version (int, optional): Version of the ingestion process (2 or 3). Defaults to 2.
        trigger_only (bool, optional): Whether to trigger only without waiting for task completion. Applicable for V3. Defaults to False.
    """

    project_id = None
    headers = None

    try:
        project_id = getProjectID(config, projectname)

        headers = connection_get_headers(config)

        print(f"Upload of file '{filename}' into project '{projectname}' initiated...")

        # Zip the file before uploading
        gzipped_filename = filename + ".gz"
        with open(filename, "rb") as f_in:
            with gzip.open(gzipped_filename, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"File {filename} has been compressed to {gzipped_filename}")

        # Retrieve temporary credentials from NEMO TVM
        response = requests.get(
            config.config_get_nemo_url() + ENDPOINT_URL_TVM_S3_ACCESS,
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
            print(f"File {filename} uploaded successfully to s3 ({s3filename})")
        except FileNotFoundError:
            print(f"The file {filename} was not found.")
        except NoCredentialsError:
            print("Credentials not available or incorrect.")

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
            ENDPOINT_URL_QUEUE_INGEST_DATA_V3
            if version == 3
            else ENDPOINT_URL_QUEUE_INGEST_DATA_V2
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
        print("Ingestion successful")

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
                    config.config_get_nemo_url() + ENDPOINT_URL_QUEUE_TASK_RUNS,
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
                print("Status: ", status)
                if status == "failed":
                    raise Exception("Data ingestion request failed, status: FAILED")
                if status == "finished":
                    if version == 2:
                        records = df_filtered["records"].iloc[0]
                        print(f"Ingestion finished. {records} records loaded")
                    else:
                        print("Ingestion finished.")
                    break
                time.sleep(1 if version == 2 else 5)

        # Trigger Analyze Table Task for version 2 if required
        if version == 2 and update_project_settings:
            data = {
                "project_id": project_id,
            }
            response = requests.post(
                config.config_get_nemo_url() + ENDPOINT_URL_QUEUE_ANALYZE_TABLE,
                headers=headers,
                json=data,
            )
            if response.status_code != 200:
                raise Exception(
                    f"Request failed. Status: {response.status_code}, error: {response.text}"
                )
            print("Analyze_table triggered")

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
                    config.config_get_nemo_url() + ENDPOINT_URL_QUEUE_TASK_RUNS,
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
                print("Status: ", status)
                if status == "failed":
                    raise Exception("Analyze_table request failed, status: FAILED")
                if status == "finished":
                    print("Analyze_table finished.")
                    break
                time.sleep(1)

    except Exception as e:
        if project_id is None:
            raise Exception("Upload stopped, no project_id available")
        raise Exception(f"Upload aborted: {e}")
