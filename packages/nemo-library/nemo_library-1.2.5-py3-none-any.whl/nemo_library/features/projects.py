import logging
import re
import pandas as pd
import requests
import json

from nemo_library.features.config import Config
from nemo_library.utils.utils import display_name, import_name, internal_name, log_error


def getProjectList(
    config: Config,
):
    """
    Fetches the list of projects from the NEMO API and returns it as a pandas DataFrame.
    Logs an error message if the API request fails.

    Args:
        config (Config): Configuration object containing methods for generating headers
                         and the NEMO API URL.

    Returns:
        pandas.DataFrame: A DataFrame containing the normalized project data.

    Logs:
        Error: If the API request fails (e.g., non-200 status code).
    """

    headers = config.connection_get_headers()

    response = requests.get(
        config.config_get_nemo_url() + "/api/nemo-projects/projects", headers=headers
    )
    if response.status_code != 200:
        log_error(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )
    resultjs = json.loads(response.text)
    df = pd.json_normalize(resultjs)
    return df


def getProjectID(
    config: Config,
    projectname: str,
) -> str:
    """
    Retrieves the unique project ID for a given project name.

    Args:
        config (Config): Configuration object containing connection details.
        projectname (str): The name of the project for which to retrieve the ID.

    Returns:
        str: The unique identifier (ID) of the specified project.

    Raises:
        ValueError: If the project name cannot be uniquely identified in the project list.

    Notes:
        - This function relies on the `getProjectList` function to fetch the full project list.
        - If multiple or no entries match the given project name, an error is logged, and the first matching ID is returned.
    """
    df = getProjectList(config)
    crmproject = df[df["displayName"] == projectname]
    if len(crmproject) != 1:
        log_error(f"could not identify project name {projectname}")
    project_id = crmproject["id"].to_list()[0]
    return project_id


def getProjectProperty(
    config: Config,
    projectname: str,
    propertyname: str,
) -> str:
    """
    Retrieves a specific property value of a given project from the server.

    Args:
        config (Config): Configuration object containing connection details and headers.
        projectname (str): The name of the project for which the property is requested.
        propertyname (str): The name of the property to retrieve.

    Returns:
        str: The value of the specified property, with leading and trailing quotation marks removed.

    Raises:
        RuntimeError: If the request to fetch the project property fails (non-200 status code).

    Notes:
        - This function first fetches the project ID using the `getProjectID` function.
        - Constructs an endpoint URL using the project ID and property name.
        - Sends an HTTP GET request to fetch the property value.
        - Logs an error if the request fails and raises an exception.
    """
    project_id = getProjectID(config, projectname)

    headers = config.connection_get_headers()

    ENDPOINT_URL = (
        config.config_get_nemo_url()
        + "/api/nemo-persistence/ProjectProperty/project/{projectId}/{request}".format(
            projectId=project_id, request=propertyname
        )
    )

    response = requests.get(ENDPOINT_URL, headers=headers)

    if response.status_code != 200:
        log_error(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )

    return response.text[1:-1]  # cut off leading and trailing "


def LoadReport(
    config: Config,
    projectname: str,
    report_guid: str,
    max_pages=None,
) -> pd.DataFrame:
    """
    Loads a report from a specified project and returns the data as a Pandas DataFrame.

    Args:
        config (Config): Configuration object containing connection details and headers.
        projectname (str): The name of the project from which to load the report.
        report_guid (str): The unique identifier (GUID) of the report to be loaded.
        max_pages (int, optional): Reserved for future use to limit the number of pages in the report.

    Returns:
        pd.DataFrame: The report data as a Pandas DataFrame.

    Raises:
        RuntimeError: If the report initialization or data download fails.
        ValueError: If the downloaded data cannot be processed into a DataFrame.

    Notes:
        - Fetches the project ID using `getProjectID`.
        - Sends an HTTP POST request to initialize the report and retrieve a CSV download URL.
        - Downloads the CSV file and converts it into a Pandas DataFrame.
        - Removes the `_RECORD_COUNT` column if present in the dataset.
        - Logs errors and raises exceptions for failed requests or data processing issues.
    """
    
    project_id = getProjectID(config=config, projectname=projectname)

    logging.info(f"Loading report: {report_guid} from project {projectname}")

    headers = config.connection_get_headers()

    # INIT REPORT PAYLOAD (REQUEST BODY)
    report_params = {"id": report_guid, "project_id": project_id}

    response_report = requests.post(
        config.config_get_nemo_url() + "/api/nemo-report/report_export",
        headers=headers,
        json=report_params,
    )

    if response_report.status_code != 200:
        log_error(
            f"Request failed. Status: {response_report.status_code}, error: {response_report.text}"
        )

    # Extract download URL from response
    csv_url = response_report.text.strip('"')
    logging.info(f"Downloading CSV from: {csv_url}")

    # Download the file into pandas
    try:
        result = pd.read_csv(csv_url)
        if "_RECORD_COUNT" in result.columns:
            result.drop(columns=["_RECORD_COUNT"], inplace=True)
    except Exception as e:
        log_error(f"Download failed. Status: {e}")
    return result


def createProject(
    config: Config,
    projectname: str,
    description: str,
) -> None:
    """
    Creates a new project with the specified name and description in the NEMO system.

    Args:
        config (Config): Configuration object containing connection details and headers.
        projectname (str): The display name for the new project.
        description (str): A brief description of the project.

    Returns:
        None

    Raises:
        RuntimeError: If the HTTP POST request to create the project fails (non-201 status code).

    Notes:
        - Generates a table name for the project by converting the project name to uppercase,
          replacing invalid characters with underscores, and ensuring it starts with "PROJECT_".
        - Sends a POST request to the project creation endpoint with the required metadata.
        - Logs an error if the request fails and raises an exception.
    """
    
    headers = config.connection_get_headers()
    ENDPOINT_URL = (
        config.config_get_nemo_url() + "/api/nemo-persistence/metadata/Project"
    )
    table_name = re.sub(r"[^A-Z0-9_]", "_", projectname.upper()).strip()
    if not table_name.startswith("PROJECT_"):
        table_name = "PROJECT_" + table_name

    data = {
        "autoDataRefresh": True,
        "displayName": projectname,
        "description": description,
        "type": "IndividualData",
        "status": "Active",
        "tableName": table_name,
        "importErrorType": "NoError",
        "id": "",
        "s3DataSourcePath": "",
        "showInitialConfiguration": False,
        "tenant": config.config_get_tenant(),
        "type": "0",
    }

    response = requests.post(ENDPOINT_URL, headers=headers, json=data)

    if response.status_code != 201:
        log_error(
            f"Request failed. Status: {response.status_code}, error: {response.text}"
        )


def setProjectMetaData(
    config: Config,
    projectname: str,
    processid_column: str = None,
    processdate_column: str = None,
    corpcurr_value: str = None,
) -> None:
    """
    Updates metadata for a specific project, including process ID, process date, and corporate currency value.

    Args:
        config (Config): Configuration object containing connection details and headers.
        projectname (str): The name of the project to update metadata for.
        processid_column (str, optional): The column name representing the process ID.
        processdate_column (str, optional): The column name representing the process date.
        corpcurr_value (str, optional): The corporate currency value to set.

    Returns:
        None

    Raises:
        RuntimeError: If the HTTP PUT request to update the metadata fails (non-200 status code).

    Notes:
        - Fetches the project ID using `getProjectID`.
        - Constructs a metadata payload based on the provided parameters.
        - Sends an HTTP PUT request to update the project's business process metadata.
        - Logs an error if the request fails and raises an exception.
    """
    
    headers = config.connection_get_headers()
    projectID = getProjectID(config, projectname)

    data = {}
    if corpcurr_value:
        data["corporateCurrencyValue"] = corpcurr_value
    if processdate_column:
        data["processDateColumnName"] = processdate_column
    if processid_column:
        data["processIdColumnName"] = processid_column

    ENDPOINT_URL = config.config_get_nemo_url() + "/api/nemo-persistence/ProjectProperty/project/{projectId}/BusinessProcessMetadata".format(
        projectId=projectID
    )

    response = requests.put(ENDPOINT_URL, headers=headers, json=data)
    if response.status_code != 200:
        log_error(
            f"Request failed. Status: {response.status_code}, error: {response.text}"
        )
        
def deleteProject(config: Config, projectname: str) -> None:
    """
    Deletes a specified project from the NEMO system.

    Args:
        config (Config): Configuration object containing connection details and headers.
        projectname (str): The name of the project to delete.

    Returns:
        None

    Raises:
        RuntimeError: If the HTTP DELETE request to delete the project fails (non-204 status code).

    Notes:
        - Fetches the project ID using `getProjectID`.
        - Sends an HTTP DELETE request to the endpoint associated with the project's metadata.
        - Logs an error if the request fails and raises an exception.
    """
    
    headers = config.connection_get_headers()
    projectID = getProjectID(config, projectname)
    ENDPOINT_URL = (
        config.config_get_nemo_url()
        + "/api/nemo-persistence/metadata/Project/{id}".format(id=projectID)
    )
    response = requests.delete(ENDPOINT_URL, headers=headers)

    if response.status_code != 204:
        log_error(
            f"Request failed. Status: {response.status_code}, error: {response.text}"
        )


def getImportedColumns(
    config: Config,
    projectname: str,
) -> pd.DataFrame:
    """
    Retrieves the imported columns for a specified project and returns them as a Pandas DataFrame.

    Args:
        config (Config): Configuration object containing connection details and headers.
        projectname (str): The name of the project for which to retrieve imported columns.

    Returns:
        pd.DataFrame: A DataFrame containing metadata about the imported columns.

    Raises:
        RuntimeError: If the HTTP GET request to fetch the columns fails (non-200 status code).

    Notes:
        - Fetches the project ID using `getProjectID`.
        - Sends an HTTP GET request to retrieve column metadata for the specified project.
        - Parses the JSON response and converts it into a normalized Pandas DataFrame.
        - Logs errors and raises exceptions for failed requests or invalid responses.
    """
    
    # initialize reqeust
    headers = config.connection_get_headers()
    project_id = getProjectID(config, projectname)
    response = requests.get(
        config.config_get_nemo_url()
        + "/api/nemo-persistence/metadata/Columns/project/{projectId}/exported".format(
            projectId=project_id
        ),
        headers=headers,
    )
    if response.status_code != 200:
        log_error(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )
    resultjs = json.loads(response.text)
    df = pd.json_normalize(resultjs)
    return df


def createImportedColumn(
    config: Config,
    projectname: str,
    displayName: str,
    dataType: str,
    importName: str = None,
    internalName: str = None,
    description: str = None,
) -> None:
    """
    Creates a new imported column for a specified project in the NEMO system.

    Args:
        config (Config): Configuration object containing connection details and headers.
        projectname (str): The name of the project to which the column will be added.
        displayName (str): The display name of the column.
        dataType (str): The data type of the column (e.g., "String", "Integer").
        importName (str, optional): The name used for importing data into the column. Defaults to a sanitized version of `displayName`.
        internalName (str, optional): The internal system name of the column. Defaults to a sanitized version of `displayName`.
        description (str, optional): A description of the column. Defaults to an empty string.

    Returns:
        None

    Raises:
        RuntimeError: If the HTTP POST request to create the column fails (non-201 status code).

    Notes:
        - Generates `importName` and `internalName` from `displayName` if not explicitly provided.
        - Sends an HTTP POST request to the appropriate endpoint with metadata for the new column.
        - Logs and raises an exception if the request fails.
    """
    # initialize reqeust
    headers = config.connection_get_headers()
    project_id = getProjectID(config, projectname)

    if not importName:
        importName = re.sub(r"[^a-z0-9_]", "_", displayName.lower()).strip()
    if not internalName:
        internalName = re.sub(r"[^a-z0-9_]", "_", displayName.lower()).strip()
    if not description:
        description = ""

    data = {
        "categorialType": True,
        "columnType": "ExportedColumn",
        "containsSensitiveData": False,
        "dataType": dataType,
        "description": description,
        "displayName": displayName,
        "importName": importName,
        "internalName": internalName,
        "id": "",
        "unit": "",
        "tenant": config.config_get_tenant(),
        "projectId": project_id,
    }

    response = requests.post(
        config.config_get_nemo_url() + "/api/nemo-persistence/metadata/Columns",
        headers=headers,
        json=data,
    )
    if response.status_code != 201:
        raise Exception(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )


def createOrUpdateReport(
    config: Config,
    projectname: str,
    displayName: str,
    querySyntax: str,
    internalName: str = None,
    description: str = None,
) -> None:
    """
    Creates or updates a report in the specified project within the NEMO system.

    Args:
        config (Config): Configuration object containing connection details and headers.
        projectname (str): The name of the project where the report will be created or updated.
        displayName (str): The display name of the report.
        querySyntax (str): The query syntax that defines the report's data.
        internalName (str, optional): The internal system name of the report. Defaults to a sanitized version of `displayName`.
        description (str, optional): A description of the report. Defaults to an empty string.

    Returns:
        None

    Raises:
        RuntimeError: If any HTTP request fails (non-200/201 status code).

    Notes:
        - Fetches the project ID using `getProjectID`.
        - Retrieves the list of existing reports in the project to check if the report already exists.
        - If the report exists, updates it with the new data using a PUT request.
        - If the report does not exist, creates a new report using a POST request.
        - Logs errors and raises exceptions for failed requests.
    """
    headers = config.connection_get_headers()
    project_id = getProjectID(config, projectname)

    if not internalName:
        internalName = re.sub(r"[^a-z0-9_]", "_", displayName.lower()).strip()

    # load list of reports first
    response = requests.get(
        config.config_get_nemo_url()
        + "/api/nemo-persistence/metadata/Reports/project/{projectId}/reports".format(
            projectId=project_id
        ),
        headers=headers,
    )
    resultjs = json.loads(response.text)
    df = pd.json_normalize(resultjs)
    df = pd.json_normalize(resultjs)
    if df.empty:
        internalNames = []
    else:
        internalNames = df["internalName"].to_list()
    report_exist = internalName in internalNames

    data = {
        "projectId": project_id,
        "displayName": displayName,
        "internalName": internalName,
        "querySyntax": querySyntax,
        "description": description if description else "",
        "tenant": config.config_get_tenant(),
    }

    if report_exist:
        df_filtered = df[df["internalName"] == internalName].iloc[0]
        data["id"] = df_filtered["id"]
        response = requests.put(
            config.config_get_nemo_url()
            + "/api/nemo-persistence/metadata/Reports/{id}".format(
                id=df_filtered["id"]
            ),
            headers=headers,
            json=data,
        )

        if response.status_code != 200:
            log_error(
                f"Request failed. Status: {response.status_code}, error: {response.text}"
            )

    else:
        response = requests.post(
            config.config_get_nemo_url() + "/api/nemo-persistence/metadata/Reports",
            headers=headers,
            json=data,
        )

        if response.status_code != 201:
            log_error(
                f"Request failed. Status: {response.status_code}, error: {response.text}"
            )


def createOrUpdateRule(
    config: Config,
    projectname: str,
    displayName: str,
    ruleSourceInternalName: str,
    internalName: str = None,
    ruleGroup: str = None,
    description: str = None,
) -> None:
    """
    Creates or updates a rule in the specified project within the NEMO system.

    Args:
        config (Config): Configuration object containing connection details and headers.
        projectname (str): The name of the project where the rule will be created or updated.
        displayName (str): The display name of the rule.
        ruleSourceInternalName (str): The internal name of the rule source that the rule depends on.
        internalName (str, optional): The internal system name of the rule. Defaults to a sanitized version of `displayName`.
        ruleGroup (str, optional): The group to which the rule belongs. Defaults to None.
        description (str, optional): A description of the rule. Defaults to an empty string.

    Returns:
        None

    Raises:
        RuntimeError: If any HTTP request fails (non-200/201 status code).

    Notes:
        - Fetches the project ID using `getProjectID`.
        - Retrieves the list of existing rules in the project to check if the rule already exists.
        - If the rule exists, updates it with the new data using a PUT request.
        - If the rule does not exist, creates a new rule using a POST request.
        - Logs errors and raises exceptions for failed requests.
    """
    headers = config.connection_get_headers()
    project_id = getProjectID(config, projectname)

    if not internalName:
        internalName = re.sub(r"[^a-z0-9_]", "_", displayName.lower()).strip()

    # load list of reports first
    response = requests.get(
        config.config_get_nemo_url()
        + "/api/nemo-persistence/metadata/Rule/project/{projectId}/rules".format(
            projectId=project_id
        ),
        headers=headers,
    )
    resultjs = json.loads(response.text)
    df = pd.json_normalize(resultjs)
    if df.empty:
        internalNames = []
    else:
        internalNames = df["internalName"].to_list()
    rule_exist = internalName in internalNames

    data = {
        "active": True,
        "projectId": project_id,
        "displayName": displayName,
        "internalName": internalName,
        "tenant": config.config_get_tenant(),
        "description": description if description else "",
        "ruleGroup": ruleGroup,
        "ruleSourceInternalName": ruleSourceInternalName,
    }

    if rule_exist:
        df_filtered = df[df["internalName"] == internalName].iloc[0]
        data["id"] = df_filtered["id"]
        response = requests.put(
            config.config_get_nemo_url()
            + "/api/nemo-persistence/metadata/Rule/{id}".format(id=df_filtered["id"]),
            headers=headers,
            json=data,
        )
        if response.status_code != 200:
            log_error(
                f"Request failed. Status: {response.status_code}, error: {response.text}"
            )
    else:
        response = requests.post(
            config.config_get_nemo_url() + "/api/nemo-persistence/metadata/Rule",
            headers=headers,
            json=data,
        )
        if response.status_code != 201:
            log_error(
                f"Request failed. Status: {response.status_code}, error: {response.text}"
            )


def synchronizeCsvColsAndImportedColumns(
    config: Config,
    projectname: str,
    filename: str,
) -> None:
    """
    Synchronizes the columns from a CSV file with the imported columns in a specified project.

    Args:
        config (Config): Configuration object containing connection details and headers.
        projectname (str): The name of the project where the synchronization will occur.
        filename (str): The path to the CSV file to synchronize.

    Returns:
        None

    Raises:
        RuntimeError: If there are issues retrieving imported columns or reading the CSV file.

    Notes:
        - Retrieves the existing imported columns in the project using `getImportedColumns`.
        - Reads the first line of the CSV file to get column names.
        - Compares the column names from the CSV file with the imported columns.
        - Creates new imported columns in the project for any CSV column names not already present.
        - Uses utility functions `display_name`, `internal_name`, and `import_name` to format column names.
    """
    df = getImportedColumns(config, projectname)
    importedColumns = df["internalName"].to_list() if not df.empty else []

    importedColumns = getImportedColumns(config, projectname)["internalName"].to_list()

    # Read the first line of the CSV file to get column names
    with open(filename, "r") as file:
        first_line = file.readline().strip()

    # Split the first line into a list of column names
    csv_display_names = first_line.split(";")
    csv_display_names = [x.strip('"') for x in csv_display_names]

    # Check if a record exists in the DataFrame for each column
    for column_name in csv_display_names:
        displayName = display_name(column_name)
        internalName = internal_name(column_name)
        importName = import_name(column_name)

        # Check if the record with internal_name equal to the column name exists
        if internalName in importedColumns:
            logging.info(f"Record found for column '{column_name}' in the DataFrame.")
        else:
            logging.info(
                f"******************************No record found for column '{column_name}' in the DataFrame."
            )
            createImportedColumn(
                config=config,
                projectname=projectname,
                displayName=displayName,
                dataType="string",
                importName=importName,
                internalName=internalName,
                description="",
            )
