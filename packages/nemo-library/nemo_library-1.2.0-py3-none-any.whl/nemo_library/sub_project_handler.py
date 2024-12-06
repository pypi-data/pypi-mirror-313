import re
import pandas as pd
import requests
import json

from nemo_library.sub_config_handler import ConfigHandler
from nemo_library.sub_connection_handler import connection_get_headers
from nemo_library.sub_symbols import (
    ENDPOINT_URL_PERSISTENCE_FOCUS_ATTRIBUTETREE_MOVE,
    ENDPOINT_URL_PERSISTENCE_FOCUS_ATTRIBUTETREE_PROJECTS_ATTRIBUTES,
    ENDPOINT_URL_PERSISTENCE_METADATA_CREATE_IMPORTED_COLUMN,
    ENDPOINT_URL_PERSISTENCE_METADATA_IMPORTED_COLUMNS,
    ENDPOINT_URL_PERSISTENCE_PROJECT_PROPERTIES,
    ENDPOINT_URL_PROJECTS_ALL,
    ENDPOINT_URL_PROJECTS_CREATE,
    ENDPOINT_URL_REPORT_CREATE,
    ENDPOINT_URL_REPORT_UPDATE,
    ENDPOINT_URL_REPORTS_LIST,
    ENDPOINT_URL_RULE_CREATE,
    ENDPOINT_URL_RULE_LIST,
    ENDPOINT_URL_RULE_UPDATE,
)


def getProjectList(config: ConfigHandler):
    """
    Retrieves a list of projects from the server and returns it as a DataFrame.

    Args:
        config: Configuration object that contains necessary connection settings.

    Returns:
        pd.DataFrame: DataFrame containing the list of projects.

    Raises:
        Exception: If the request to the server fails.
    """
    headers = connection_get_headers(config)

    response = requests.get(
        config.config_get_nemo_url() + ENDPOINT_URL_PROJECTS_ALL, headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )
    resultjs = json.loads(response.text)
    df = pd.json_normalize(resultjs)
    return df


def getProjectID(config: ConfigHandler, projectname: str):
    """
    Retrieves the project ID for a given project name.

    Args:
        config: Configuration object that contains necessary connection settings.
        projectname (str): The name of the project for which to retrieve the ID.

    Returns:
        str: The ID of the specified project.

    Raises:
        Exception: If the project name is not found or if multiple projects match the given name.
    """
    df = getProjectList(config)
    crmproject = df[df["displayName"] == projectname]
    if len(crmproject) != 1:
        raise Exception(f"could not identify project name {projectname}")
    project_id = crmproject["id"].to_list()[0]
    return project_id


def getProjectProperty(config: ConfigHandler, projectname: str, propertyname: str):
    """
    Retrieves a specified property for a given project from the server.

    Args:
        config: Configuration object that contains necessary connection settings.
        projectname (str): The name of the project for which to retrieve the property.
        propertyname (str): The name of the property to retrieve.

    Returns:
        str: The value of the specified property for the given project.

    Raises:
        Exception: If the request to the server fails.
    """
    headers = connection_get_headers(config)
    project_id = getProjectID(config, projectname)

    ENDPOINT_URL = (
        config.config_get_nemo_url()
        + ENDPOINT_URL_PERSISTENCE_PROJECT_PROPERTIES.format(
            projectId=project_id, request=propertyname
        )
    )

    response = requests.get(ENDPOINT_URL, headers=headers)

    if response.status_code != 200:
        raise Exception(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )

    return response.text[1:-1]  # cut off leading and trailing "


def getImportedColumns(config: ConfigHandler, projectname: str) -> pd.DataFrame:
    """
    Fetches and returns the imported columns metadata for a given project in the form of a pandas DataFrame.

    Args:
        config (ConfigHandler): Configuration handler instance to access settings and credentials.
        projectname (str): The name of the project for which the imported columns metadata is requested.

    Returns:
        pd.DataFrame: A DataFrame containing the imported columns metadata.

    Raises:
        Exception: If the project ID cannot be retrieved or the HTTP request fails.

    Process:
        1. Initializes request headers using `connection_get_headers`.
        2. Retrieves the project ID using `getProjectID`.
        3. Sends an HTTP GET request to the configured NEMO API endpoint for imported columns.
        4. Parses the JSON response and normalizes it into a pandas DataFrame.
        5. Handles errors such as missing project ID or failed requests.
    """
    try:

        # initialize reqeust
        headers = connection_get_headers(config)
        project_id = getProjectID(config, projectname)
        response = requests.get(
            config.config_get_nemo_url()
            + ENDPOINT_URL_PERSISTENCE_METADATA_IMPORTED_COLUMNS.format(
                projectId=project_id
            ),
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception(
                f"request failed. Status: {response.status_code}, error: {response.text}"
            )
        resultjs = json.loads(response.text)
        df = pd.json_normalize(resultjs)
        return df

    except Exception as e:
        if project_id == None:
            raise Exception("process stopped, no project_id available")
        raise Exception("process aborted")


def createProject(config: ConfigHandler, projectname: str, description: str):
    """
    Creates a new project using the specified configuration and project name.

    This function sends a POST request to the NEMO API to create a project with
    the given name. The project is initialized with default settings and a
    specific structure, ready for further processing.

    Args:
        config (ConfigHandler): An object that provides the necessary configuration
                                for connecting to the NEMO API, such as headers and URL.
        projectname (str): The name of the project to be created.

    Raises:
        Exception: If the request to create the project fails, an exception is raised
                   with the HTTP status code and error details.

    Returns:
        None: The function does not return any value. If the project is created
              successfully, it completes without errors.

    Example:
        config = ConfigHandler()  # Assume this is initialized with necessary details
        createProject(config, "MyProject")
    """
    headers = connection_get_headers(config)
    ENDPOINT_URL = config.config_get_nemo_url() + ENDPOINT_URL_PROJECTS_CREATE
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
        "showInitialConfiguration": True,
        "tenant": config.config_get_tenant(),
        "type": "0",
    }

    response = requests.post(ENDPOINT_URL, headers=headers, json=data)

    if response.status_code != 201:
        raise Exception(
            f"Request failed. Status: {response.status_code}, error: {response.text}"
        )


def createImportedColumn(
    config: ConfigHandler,
    projectname: str,
    displayName: str,
    dataType: str,
    importName: str = None,
    internalName: str = None,
    description: str = None,
) -> None:
    """
    Creates an imported column in the specified project within the system.

    This function constructs a new imported column using provided metadata
    and posts it to the appropriate endpoint for persistence. If `importName`
    or `internalName` is not provided, it generates them based on the `displayName`.

    Args:
        config (ConfigHandler): Configuration handler containing system-specific details.
        projectname (str): The name of the project where the column will be created.
        displayName (str): The display name of the column.
        dataType (str): The data type of the column (e.g., "string", "integer").
        importName (str, optional): The import name for the column. Defaults to a sanitized version of `displayName`.
        internalName (str, optional): The internal name for the column. Defaults to a sanitized version of `displayName`.
        description (str, optional): A brief description of the column's purpose or content.

    Raises:
        Exception: If the HTTP request to create the column fails, an exception is raised with status code and error details.

    Returns:
        None: The function does not return a value; it creates the column via a POST request.
    """
    headers = connection_get_headers(config)
    project_id = getProjectID(config, projectname)

    if not importName:
        importName = re.sub(r"[^a-z0-9_]", "_", displayName.lower()).strip()
    if not internalName:
        internalName = re.sub(r"[^a-z0-9_]", "_", displayName.lower()).strip()

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
        config.config_get_nemo_url()
        + ENDPOINT_URL_PERSISTENCE_METADATA_CREATE_IMPORTED_COLUMN,
        headers=headers,
        json=data,
    )
    if response.status_code != 201:
        raise Exception(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )


def createOrUpdateReport(
    config: ConfigHandler,
    projectname: str,
    displayName: str,
    querySyntax: str,
    internalName: str = None,
    description: str = None,
) -> None:
    """
    Creates a new report in the NEMO platform for a specified project.

    Args:
        config (ConfigHandler): The configuration handler containing authentication
                                and API endpoint details.
        projectname (str): The name of the project where the report will be created.
        displayName (str): The human-readable name of the report to be displayed.
        querySyntax (str): The query syntax defining the report logic or content.
        internalName (str, optional): An internal, system-friendly name for the report.
                                      Defaults to a sanitized version of `displayName`.
        description (str, optional): A detailed description of the report. Defaults to None.

    Raises:
        Exception: If the API request to create the report fails, an exception is raised
                   with the response status code and error message.

    Notes:
        - The `internalName` will be auto-generated by sanitizing `displayName` if not provided.
        - The function relies on the `ConfigHandler` to manage authentication headers and
          endpoint configurations.
    """
    headers = connection_get_headers(config)
    project_id = getProjectID(config, projectname)

    if not internalName:
        internalName = re.sub(r"[^a-z0-9_]", "_", displayName.lower()).strip()

    # load list of reports first
    response = requests.get(
        config.config_get_nemo_url()
        + ENDPOINT_URL_REPORTS_LIST.format(projectId=project_id),
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
            + ENDPOINT_URL_REPORT_UPDATE.format(id=df_filtered["id"]),
            headers=headers,
            json=data,
        )

        if response.status_code != 200:
            raise Exception(
                f"Request failed. Status: {response.status_code}, error: {response.text}"
            )

    else:
        response = requests.post(
            config.config_get_nemo_url() + ENDPOINT_URL_REPORT_CREATE,
            headers=headers,
            json=data,
        )

        if response.status_code != 201:
            raise Exception(
                f"Request failed. Status: {response.status_code}, error: {response.text}"
            )


def createOrUpdateRule(
    config: ConfigHandler,
    projectname: str,
    displayName: str,
    ruleSourceInternalName: str,
    internalName: str = None,
    ruleGroup: str = None,
    description: str = None,
) -> None:
    """
    Creates a new rule in the NEMO system.

    Args:
        config (ConfigHandler): An instance of ConfigHandler containing the configuration and authentication details.
        projectname (str): The name of the project where the rule will be created.
        displayName (str): The human-readable name for the rule.
        ruleSourceInternalName (str): The internal name of the rule's source.
        internalName (str, optional): A unique internal identifier for the rule. If not provided, it will be generated
                                      from the `displayName` by replacing non-alphanumeric characters with underscores.
        ruleGroup (str, optional): The group to which the rule belongs. Defaults to None.
        description (str, optional): A brief description of the rule. Defaults to None.

    Returns:
        None

    Raises:
        Exception: If the rule creation request fails (i.e., the API response status code is not 201).

    Example:
        >>> createRule(config, "ProjectA", "New Rule", "Source_Internal_Name")

    Notes:
        - The `internalName` is sanitized to ensure it only contains lowercase alphanumeric characters and underscores.
        - A valid project ID is fetched using the `getProjectID` function.
        - The function sends a POST request to the NEMO API to create the rule.
    """
    headers = connection_get_headers(config)
    project_id = getProjectID(config, projectname)

    if not internalName:
        internalName = re.sub(r"[^a-z0-9_]", "_", displayName.lower()).strip()

    # load list of reports first
    response = requests.get(
        config.config_get_nemo_url()
        + ENDPOINT_URL_RULE_LIST.format(projectId=project_id),
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
            + ENDPOINT_URL_RULE_UPDATE.format(id=df_filtered["id"]),
            headers=headers,
            json=data,
        )
        if response.status_code != 200:
            raise Exception(
                f"Request failed. Status: {response.status_code}, error: {response.text}"
            )
    else:
        response = requests.post(
            config.config_get_nemo_url() + ENDPOINT_URL_RULE_CREATE,
            headers=headers,
            json=data,
        )
        if response.status_code != 201:
            raise Exception(
                f"Request failed. Status: {response.status_code}, error: {response.text}"
            )


def focusMoveAttributeBefore(
    config: ConfigHandler,
    projectname: str,
    sourceDisplayName: str,
    targetDisplayName: str = None,
) -> None:
    """
    Moves an attribute within the attribute tree of a project in the NEMO system.

    This function interacts with the NEMO API to reposition an attribute by specifying 
    a source attribute and an optional target attribute within a project's attribute tree.

    Args:
        config (ConfigHandler): Configuration handler object to manage API connections.
        projectname (str): The name of the project in which the attribute resides.
        sourceDisplayName (str): The display name of the source attribute to be moved.
        targetDisplayName (str, optional): The display name of the target attribute. 
            If not specified, the source attribute is moved to the top of the attribute tree.

    Raises:
        Exception: If the API requests to fetch the attribute tree or move the attribute fail.

    Details:
        1. Fetches the project ID corresponding to the given project name.
        2. Retrieves the attribute tree for the project from the NEMO API.
        3. Identifies the IDs of the source and target attributes using their display names.
        4. Sends a PUT request to the NEMO API to move the source attribute before the target.
    """
    headers = connection_get_headers(config)
    project_id = getProjectID(config, projectname)

    # load attribute tree
    response = requests.get(
        config.config_get_nemo_url()
        + ENDPOINT_URL_PERSISTENCE_FOCUS_ATTRIBUTETREE_PROJECTS_ATTRIBUTES.format(
            projectId=project_id
        ),
        headers=headers,
    )
    if response.status_code != 200:
        raise Exception(
            f"Request failed. Status: {response.status_code}, error: {response.text}"
        )
    
    resultjs = json.loads(response.text)
    df = pd.json_normalize(resultjs)

    # locate source and target object
    sourceid = df[df["label"] == sourceDisplayName].iloc[0]["id"]
    targetid = (
        df[df["label"] == targetDisplayName].iloc[0]["id"]
        if targetDisplayName
        else None
    )

    # now move the attribute
    data = {
        "sourceAttributes": [sourceid],
        "targetPreviousElementId": targetid,
        # "groupInternalName": "",
    }

    response = requests.put(
        config.config_get_nemo_url()
        + ENDPOINT_URL_PERSISTENCE_FOCUS_ATTRIBUTETREE_MOVE.format(
            projectId=project_id
        ),
        headers=headers,
        json=data,
    )

    if response.status_code != 204:
        raise Exception(
            f"Request failed. Status: {response.status_code}, error: {response.text}"
        )
