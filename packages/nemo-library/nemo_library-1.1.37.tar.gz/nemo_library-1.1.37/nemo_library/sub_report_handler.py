import requests
import pandas as pd

from nemo_library.sub_config_handler import ConfigHandler
from nemo_library.sub_connection_handler import connection_get_headers
from nemo_library.sub_project_handler import getProjectID
from nemo_library.sub_symbols import ENDPOINT_URL_REPORT_EXPORT


def LoadReport(
    config: ConfigHandler, projectname: str, report_guid: str, max_pages=None
) -> pd.DataFrame:
    """
    Loads a report from a specified project and returns it as a pandas DataFrame.

    Args:
        config (ConfigHandler): Configuration handler object that contains necessary configuration data.
        projectname (str): The name of the project from which the report is to be loaded.
        report_guid (str): The GUID (Globally Unique Identifier) of the report to be loaded.
        max_pages (int, optional): Maximum number of pages to load. Defaults to None.

    Returns:
        pandas.DataFrame: The report data as a DataFrame.

    Raises:
        Exception: If the request to load the report fails or if downloading the CSV fails.

    """
    project_id = getProjectID(config=config, projectname=projectname)

    print(f"Loading report: {report_guid} from project {projectname}")

    headers = connection_get_headers(config)

    # INIT REPORT PAYLOAD (REQUEST BODY)
    report_params = {"id": report_guid, "project_id": project_id}

    response_report = requests.post(
        config.config_get_nemo_url() + ENDPOINT_URL_REPORT_EXPORT,
        headers=headers,
        json=report_params,
    )

    if response_report.status_code != 200:
        raise Exception(
            f"Request failed. Status: {response_report.status_code}, error: {response_report.text}"
        )

    # Extract download URL from response
    csv_url = response_report.text.strip('"')
    print(f"Downloading CSV from: {csv_url}")

    # Download the file into pandas
    try:
        result = pd.read_csv(csv_url)
        if "_RECORD_COUNT" in result.columns:
            result.drop(columns=["_RECORD_COUNT"], inplace=True)
    except Exception as e:
        raise Exception(f"Download failed. Status: {e}")
    return result
